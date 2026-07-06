import json
import logging
from backend.utils.helpers import error_response, standard_response

logger = logging.getLogger("kitchen_os")

def handle_pos_routes(method, path, body, services, headers):
    """Processes POS checkouts webhook endpoints."""
    
    if method == "POST" and path == "/api/v1/pos/webhook":
        menu_item_name = body.get("menu_item")
        sale_qty = body.get("quantity", 1)
        
        if not menu_item_name:
            return error_response("INVALID_INPUT", "menu_item is a required parameter.", status_code=400)
            
        try:
            sale_qty = int(sale_qty)
            if sale_qty <= 0:
                raise ValueError()
        except ValueError:
            return error_response("INVALID_QUANTITY", "quantity must be a positive integer.", status_code=400)
            
        # Find recipe matching menu item name
        recipe_row = services.db.fetch_one("SELECT * FROM recipes WHERE LOWER(name) = LOWER(?);", (menu_item_name,))
        if not recipe_row:
            return error_response("RECIPE_NOT_FOUND", f"No active recipe found matching item '{menu_item_name}'.", status_code=404)
            
        recipe_id = recipe_row["id"]
        
        # Get recipe ingredients requirements
        reqs = services.db.fetch_all("SELECT * FROM recipe_ingredients WHERE recipe_id = ?;", (recipe_id,))
        
        # Verify and deduct using FIFO rules from pantry
        conn = services.db.get_connection()
        cursor = conn.cursor()
        try:
            deductions = []
            for req in reqs:
                ing_id = req["ingredient_id"]
                req_qty_total = req["quantity"] * sale_qty
                
                # Fetch available pantry stock (ordered by expiry_date ASC - FIFO)
                stocks = cursor.execute(
                    "SELECT * FROM pantry_items WHERE ingredient_id = ? AND quantity > 0 ORDER BY expiry_date ASC;",
                    (ing_id,)
                ).fetchall()
                
                total_avail = sum(s["quantity"] for s in stocks)
                if total_avail < req_qty_total:
                    # Rolling back
                    conn.rollback()
                    return error_response(
                        "INSUFFICIENT_STOCK",
                        f"Insufficient stock for ingredient ID {ing_id} to fulfill sale.",
                        details={"required": req_qty_total, "available": total_avail},
                        status_code=400
                    )
                
                # Process deduction
                remaining_to_deduct = req_qty_total
                for stock in stocks:
                    if remaining_to_deduct <= 0:
                        break
                    
                    stock_id = stock["id"]
                    stock_qty = stock["quantity"]
                    
                    if stock_qty <= remaining_to_deduct:
                        cursor.execute("UPDATE pantry_items SET quantity = 0.0 WHERE id = ?;", (stock_id,))
                        remaining_to_deduct -= stock_qty
                        deductions.append((stock_id, 0.0))
                    else:
                        new_qty = stock_qty - remaining_to_deduct
                        cursor.execute("UPDATE pantry_items SET quantity = ? WHERE id = ?;", (new_qty, stock_id))
                        remaining_to_deduct = 0.0
                        deductions.append((stock_id, new_qty))
                        
            conn.commit()
            return standard_response(data={
                "message": f"Deductions executed successfully for {sale_qty} portions of {menu_item_name}.",
                "deductions_count": len(deductions)
            }, status_code=200), 200
        except Exception as e:
            conn.rollback()
            logger.error(f"Error executing POS deductions: {e}")
            return error_response("POS_DEDUCTION_ERROR", f"An internal transaction failure occurred: {str(e)}", status_code=500)
        finally:
            cursor.close()
            conn.close()

    return error_response("ROUTE_NOT_FOUND", f"Route {method} {path} not found in POS scope.", status_code=404)
