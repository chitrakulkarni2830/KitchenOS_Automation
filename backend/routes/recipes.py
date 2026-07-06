import json
import logging
from backend.utils.helpers import error_response, standard_response

logger = logging.getLogger("kitchen_os")

def handle_recipe_routes(method, path, body, services, headers):
    """Processes recipes and costing API routes."""
    
    if method == "GET" and path == "/api/v1/recipes":
        recipes = services.list_recipes()
        # Enforce cost recalculation for each recipe
        for r in recipes:
            r["calculated_cost"] = services.calculate_recipe_cost(r["id"])
        return standard_response(data=recipes, status_code=200), 200
        
    elif method == "GET" and path.startswith("/api/v1/recipes/"):
        parts = path.split("/")
        # Path: /api/v1/recipes/{id}/cost
        if len(parts) >= 6 and parts[-1] == "cost":
            try:
                recipe_id = int(parts[4])
            except ValueError:
                return error_response("INVALID_ID", "Recipe ID must be numeric.", status_code=400)
                
            cost = services.calculate_recipe_cost(recipe_id)
            return standard_response(data={"recipe_id": recipe_id, "calculated_cost": cost}, status_code=200), 200
            
    return error_response("ROUTE_NOT_FOUND", f"Route {method} {path} not found in Recipes scope.", status_code=404)
