import json
import logging
import urllib.parse
from backend.utils.helpers import error_response, standard_response

logger = logging.getLogger("kitchen_os")

def handle_inventory_routes(method, path, body, services, headers, query_params):
    """Processes ingredient catalog and pantry inventory API routes."""
    
    # --- INGREDIENT ENDPOINTS ---
    if method == "GET" and path == "/api/v1/ingredients":
        search = query_params.get("search", [None])[0]
        if search:
            search = urllib.parse.unquote(search)
        data = services.list_ingredients(search_query=search)
        return standard_response(data=data, status_code=200), 200

    elif method == "POST" and path == "/api/v1/ingredients":
        name = body.get("name")
        unit = body.get("unit")
        cost_per_unit = body.get("cost_per_unit")
        category = body.get("category")
        
        # --- INTENTIONAL DEFECT #1: Validation Bypass ---
        # The validation logic checks if 'name' is None or not provided, but
        # fails to verify if it is an empty or whitespace string (e.g. "   ").
        # This allows duplicate, empty, or unreadable ingredient listings.
        if name is None or not unit or cost_per_unit is None or not category:
            return error_response(
                "INVALID_INPUT", 
                "All parameters (name, unit, cost_per_unit, category) are required.",
                details={"provided": body},
                status_code=400
            )
            
        try:
            cost = float(cost_per_unit)
            if cost < 0:
                return error_response("INVALID_COST", "Cost per unit must be non-negative.", status_code=400)
        except ValueError:
            return error_response("INVALID_COST", "Cost must be a numerical representation.", status_code=400)
            
        # Check if database has it
        existing = services.db.fetch_one("SELECT * FROM ingredients WHERE LOWER(name) = LOWER(?);", (name,))
        if existing:
            return error_response("INGREDIENT_EXISTS", f"Ingredient '{name}' already exists in database.", status_code=409)
            
        new_ingredient = services.create_ingredient(name, unit, cost, category)
        return standard_response(data=new_ingredient.to_dict(), status_code=201), 201

    elif method == "PUT" and path.startswith("/api/v1/ingredients/"):
        try:
            ing_id = int(path.split("/")[-1])
        except ValueError:
            return error_response("INVALID_ID", "Ingredient ID must be numeric.", status_code=400)
            
        name = body.get("name")
        unit = body.get("unit")
        cost_per_unit = body.get("cost_per_unit")
        category = body.get("category")
        
        if not name or not unit or cost_per_unit is None or not category:
            return error_response("INVALID_INPUT", "All parameters are required for update.", status_code=400)
            
        try:
            cost = float(cost_per_unit)
        except ValueError:
            return error_response("INVALID_COST", "Cost must be numeric.", status_code=400)
            
        try:
            updated = services.update_ingredient(ing_id, name, unit, cost, category)
            if not updated:
                return error_response("NOT_FOUND", "Ingredient not found.", status_code=404)
            return standard_response(data=updated.to_dict(), status_code=200), 200
        except ValueError as e:
            return error_response("DUPLICATE_NAME", str(e), status_code=400)

    elif method == "DELETE" and path.startswith("/api/v1/ingredients/"):
        try:
            ing_id = int(path.split("/")[-1])
        except ValueError:
            return error_response("INVALID_ID", "Ingredient ID must be numeric.", status_code=400)
            
        try:
            services.delete_ingredient(ing_id)
            return standard_response(data={"message": "Ingredient deleted successfully."}, status_code=200), 200
        except ValueError as e:
            return error_response("DELETION_BLOCKED", str(e), status_code=400)

    # --- PANTRY ENDPOINTS ---
    elif method == "GET" and path == "/api/v1/pantry":
        data = services.list_pantry_items()
        return standard_response(data=data, status_code=200), 200

    elif method == "POST" and path == "/api/v1/pantry":
        ingredient_id = body.get("ingredient_id")
        quantity = body.get("quantity")
        expiry_date = body.get("expiry_date")
        status = body.get("status", "fresh")
        
        if ingredient_id is None or quantity is None or not expiry_date:
            return error_response("INVALID_INPUT", "ingredient_id, quantity, and expiry_date are required.", status_code=400)
            
        try:
            ing_id = int(ingredient_id)
            qty = float(quantity)
        except ValueError:
            return error_response("INVALID_NUMERIC", "IDs and quantities must be numeric values.", status_code=400)
            
        # Check ingredient existence
        ingredient = services.get_ingredient_by_id(ing_id)
        if not ingredient:
            return error_response("INGREDIENT_NOT_FOUND", "No ingredient matching this ID exists.", status_code=404)
            
        try:
            new_item = services.add_to_pantry(ing_id, qty, expiry_date, status)
            return standard_response(data=new_item.to_dict(), status_code=201), 201
        except ValueError as e:
            return error_response("VAL_ERROR", str(e), status_code=400)

    elif method == "PUT" and path.startswith("/api/v1/pantry/"):
        # Expecting path `/api/v1/pantry/{id}/status`
        parts = path.split("/")
        if len(parts) < 6 or parts[-1] != "status":
            return error_response("ROUTE_NOT_FOUND", "Endpoint path format must be /api/v1/pantry/{id}/status", status_code=404)
            
        try:
            item_id = int(parts[4])
        except ValueError:
            return error_response("INVALID_ID", "Pantry item ID must be numeric.", status_code=400)
            
        status = body.get("status")
        if not status:
            return error_response("INVALID_INPUT", "Status parameter is required.", status_code=400)
            
        try:
            updated = services.update_pantry_status(item_id, status)
            if not updated:
                return error_response("NOT_FOUND", "Pantry item not found.", status_code=404)
            return standard_response(data=updated.to_dict(), status_code=200), 200
        except ValueError as e:
            return error_response("VAL_ERROR", str(e), status_code=400)

    return error_response("ROUTE_NOT_FOUND", f"Route {method} {path} not found in Inventory scope.", status_code=404)
