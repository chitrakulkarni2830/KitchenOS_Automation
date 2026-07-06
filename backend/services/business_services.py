import logging
from backend.database.db_manager import DatabaseManager
from backend.models.entities import User, Ingredient, PantryItem, Recipe

logger = logging.getLogger("kitchen_os")

class BusinessServices:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    # --- USER SERVICES ---
    def register_user(self, email, password_hash, role):
        # Database check for duplicate email is done in controller/routes
        query = "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?);"
        user_id = self.db.execute_query(query, (email, password_hash, role))
        return self.get_user_by_id(user_id)

    def get_user_by_id(self, user_id):
        row = self.db.fetch_one("SELECT * FROM users WHERE id = ?;", (user_id,))
        return User(**row) if row else None

    def authenticate_user(self, email, password_hash):
        row = self.db.fetch_one("SELECT * FROM users WHERE email = ? AND password_hash = ?;", (email, password_hash))
        return User(**row) if row else None

    # --- INGREDIENT SERVICES ---
    # --- INTENTIONAL DEFECT #2: Incorrect Sorting ---
    # When searching ingredients, the SQL query sorts by name DESC instead of ASC.
    # This violates the UI design requirement of displaying catalog listings alphabetically (A-Z).
    def list_ingredients(self, search_query=None):
        if search_query:
            query = "SELECT * FROM ingredients WHERE name LIKE ? ORDER BY name DESC;" # DEFECT: DESC instead of ASC
            params = (f"%{search_query}%",)
        else:
            query = "SELECT * FROM ingredients ORDER BY name ASC;"
            params = ()
        rows = self.db.fetch_all(query, params)
        return [Ingredient(**row).to_dict() for row in rows]

    def create_ingredient(self, name, unit, cost_per_unit, category):
        query = "INSERT INTO ingredients (name, unit, cost_per_unit, category) VALUES (?, ?, ?, ?);"
        ingredient_id = self.db.execute_query(query, (name, unit, cost_per_unit, category))
        return self.get_ingredient_by_id(ingredient_id)

    # --- INTENTIONAL DEFECT #7: Case-Insensitive Duplicate Name Update Bypass ---
    # Ingredient update lets the user rename an item to a name that matches an existing name in a different case.
    # For example, renaming "Toor Dal" to "onion" succeeds even if "Onion" already exists, bypassing the unique constraint validation.
    def update_ingredient(self, ingredient_id, name, unit, cost_per_unit, category):
        # Validate unique name (case-insensitive check)
        existing = self.db.fetch_one("SELECT * FROM ingredients WHERE LOWER(name) = LOWER(?) AND id != ?;", (name, ingredient_id))
        
        # DEFECT: If existing has a different case, we skip throwing an error and let it proceed!
        # It should raise an exception on duplicate name.
        if existing and existing['name'] == name:
            raise ValueError("An ingredient with this name already exists.")

        query = "UPDATE ingredients SET name = ?, unit = ?, cost_per_unit = ?, category = ? WHERE id = ?;"
        self.db.execute_query(query, (name, unit, cost_per_unit, category, ingredient_id))
        return self.get_ingredient_by_id(ingredient_id)

    # --- INTENTIONAL DEFECT #10: Soft Deletion Query Logic Flaw ---
    # When an ingredient is soft-deleted, we set its cost to 0.0 or remove it from the DB.
    # However, if we delete it, we do not check if it is active or we flag it as deleted but listing ignores it.
    # Let's say we mark the ingredient name prefix with "[DELETED]" but keep it in the list,
    # or the soft delete operation sets a flag but list_ingredients retrieves it anyway unless we pass a filter.
    def delete_ingredient(self, ingredient_id):
        # Check if the ingredient is used in recipes
        usage = self.db.fetch_one("SELECT COUNT(*) as count FROM recipe_ingredients WHERE ingredient_id = ?;", (ingredient_id,))
        if usage and usage['count'] > 0:
            raise ValueError("Cannot delete ingredient because it is currently used in active recipes.")
        
        # Soft delete by prefixing name, but DEFECT: list_ingredients will still retrieve it because we didn't remove it or filter it!
        query = "UPDATE ingredients SET name = '[DELETED] ' || name WHERE id = ?;"
        self.db.execute_query(query, (ingredient_id,))
        return True

    def get_ingredient_by_id(self, ingredient_id):
        row = self.db.fetch_one("SELECT * FROM ingredients WHERE id = ?;", (ingredient_id,))
        return Ingredient(**row) if row else None

    # --- PANTRY SERVICES ---
    def list_pantry_items(self):
        query = """
            SELECT p.*, i.name as ingredient_name, i.unit 
            FROM pantry_items p 
            JOIN ingredients i ON p.ingredient_id = i.id
            ORDER BY p.expiry_date ASC;
        """
        rows = self.db.fetch_all(query)
        return [PantryItem(**row).to_dict() for row in rows]

    # --- INTENTIONAL DEFECT #3: Boundary Limit Error ---
    # The pantry item quantity checker allows adding or updating exactly 0 items.
    # In specifications, quantity updates must be strictly positive values (> 0).
    def add_to_pantry(self, ingredient_id, quantity, expiry_date, status):
        # DEFECT: Allows 0 value checks
        if quantity < 0: # Should be quantity <= 0
            raise ValueError("Quantity must be a positive value.")
        
        query = "INSERT INTO pantry_items (ingredient_id, quantity, expiry_date, status) VALUES (?, ?, ?, ?);"
        item_id = self.db.execute_query(query, (ingredient_id, quantity, expiry_date, status))
        return self.get_pantry_item_by_id(item_id)

    # --- INTENTIONAL DEFECT #5: State Logic Slip ---
    # If the pantry status is updated to "expired", the quantity is forced to 1.0, overwriting the original value.
    def update_pantry_status(self, item_id, status):
        valid_statuses = ['fresh', 'warning', 'expired']
        if status not in valid_statuses:
            raise ValueError(f"Invalid status: {status}")
        
        # DEFECT: State transition bug
        if status == 'expired':
            query = "UPDATE pantry_items SET status = ?, quantity = 1.0 WHERE id = ?;" # Quantity reset defect
        else:
            query = "UPDATE pantry_items SET status = ? WHERE id = ?;"
            
        self.db.execute_query(query, (status, item_id))
        return self.get_pantry_item_by_id(item_id)

    def get_pantry_item_by_id(self, item_id):
        query = """
            SELECT p.*, i.name as ingredient_name, i.unit 
            FROM pantry_items p 
            JOIN ingredients i ON p.ingredient_id = i.id
            WHERE p.id = ?;
        """
        row = self.db.fetch_one(query, (item_id,))
        return PantryItem(**row) if row else None

    # --- RECIPE SERVICES ---
    def list_recipes(self):
        rows = self.db.fetch_all("SELECT * FROM recipes ORDER BY name ASC;")
        recipes = []
        for row in rows:
            recipe = Recipe(**row)
            # Fetch mapped ingredients
            ing_rows = self.db.fetch_all("""
                SELECT ri.quantity, i.name, i.unit, i.cost_per_unit
                FROM recipe_ingredients ri
                JOIN ingredients i ON ri.ingredient_id = i.id
                WHERE ri.recipe_id = ?;
            """, (recipe.id,))
            recipe.ingredients = ing_rows
            recipes.append(recipe.to_dict())
        return recipes

    # --- INTENTIONAL DEFECT #4: Off-by-One Calculation Error ---
    # The total cost calculation loops through the ingredient array but stops short,
    # ignoring the last ingredient in the list. This leads to under-budgeted recipe totals.
    def calculate_recipe_cost(self, recipe_id):
        ing_rows = self.db.fetch_all("""
            SELECT ri.quantity, i.cost_per_unit
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
            WHERE ri.recipe_id = ?;
        """, (recipe_id,))
        
        if not ing_rows:
            return 0.0
            
        total_cost = 0.0
        # DEFECT: Off-by-one loop limit (ing_rows[:-1] ignores the last element)
        for row in ing_rows[:-1]:
            total_cost += row['quantity'] * row['cost_per_unit']
            
        return round(total_cost, 2)
