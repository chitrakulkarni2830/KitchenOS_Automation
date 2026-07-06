class User:
    def __init__(self, id, email, password_hash, role, created_at=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at
        }

class Ingredient:
    def __init__(self, id, name, unit, cost_per_unit, category, created_at=None):
        self.id = id
        self.name = name
        self.unit = unit
        self.cost_per_unit = cost_per_unit
        self.category = category
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
            "cost_per_unit": self.cost_per_unit,
            "category": self.category,
            "created_at": self.created_at
        }

class PantryItem:
    def __init__(self, id, ingredient_id, quantity, expiry_date, status, created_at=None, ingredient_name=None, unit=None):
        self.id = id
        self.ingredient_id = ingredient_id
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.status = status
        self.created_at = created_at
        # Joined parameters
        self.ingredient_name = ingredient_name
        self.unit = unit

    def to_dict(self):
        res = {
            "id": self.id,
            "ingredient_id": self.ingredient_id,
            "quantity": self.quantity,
            "expiry_date": self.expiry_date,
            "status": self.status,
            "created_at": self.created_at
        }
        if self.ingredient_name:
            res["ingredient_name"] = self.ingredient_name
        if self.unit:
            res["unit"] = self.unit
        return res

class Recipe:
    def __init__(self, id, name, servings, prep_time, instructions, created_at=None, ingredients=None):
        self.id = id
        self.name = name
        self.servings = servings
        self.prep_time = prep_time
        self.instructions = instructions
        self.created_at = created_at
        self.ingredients = ingredients or []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "servings": self.servings,
            "prep_time": self.prep_time,
            "instructions": self.instructions,
            "created_at": self.created_at,
            "ingredients": self.ingredients
        }
