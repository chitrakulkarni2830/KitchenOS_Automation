import json
import logging
from backend.utils.helpers import generate_jwt, verify_password, hash_password, error_response, standard_response

logger = logging.getLogger("kitchen_os")

def handle_auth_routes(method, path, body, services, headers):
    """Processes authentication and session API routes."""
    
    if method == "POST" and path == "/api/v1/auth/register":
        email = body.get("email")
        password = body.get("password")
        role = body.get("role", "cook")
        
        if not email or not password:
            return error_response("MISSING_CREDENTIALS", "Email and password are required.", status_code=400)
            
        # Check if email exists
        # In a custom DB leak scenario (Defect #8), this executes the leaky function
        existing_user = services.db.find_user_by_email(email)
        
        # --- INTENTIONAL DEFECT #9: Wrong HTTP Status Code ---
        # When an email already exists in the system, we return '400 Bad Request'
        # instead of the standard RESTful status '409 Conflict'.
        if existing_user:
            return error_response(
                "USER_EXISTS", 
                "A user with this email already exists.", 
                details={"email": email}, 
                status_code=400 # DEFECT: Should be 409 Conflict
            )
            
        hashed_pwd = hash_password(password)
        new_user = services.register_user(email, hashed_pwd, role)
        
        token = generate_jwt({"user_id": new_user.id, "email": new_user.email, "role": new_user.role})
        
        res = standard_response(data={
            "user": new_user.to_dict(),
            "token": token
        }, status_code=201)
        return res, 201

    elif method == "POST" and path == "/api/v1/auth/login":
        email = body.get("email")
        password = body.get("password")
        
        if not email or not password:
            return error_response("MISSING_CREDENTIALS", "Email and password are required.", status_code=400)
            
        user = services.db.find_user_by_email(email)
        if not user or not verify_password(password, user["password_hash"]):
            return error_response("INVALID_CREDENTIALS", "Invalid email or password credentials.", status_code=401)
            
        token = generate_jwt({"user_id": user["id"], "email": user["email"], "role": user["role"]})
        
        res = standard_response(data={
            "user": {
                "id": user["id"],
                "email": user["email"],
                "role": user["role"]
            },
            "token": token
        }, status_code=200)
        return res, 200
        
    return error_response("ROUTE_NOT_FOUND", f"Route {method} {path} not found in Auth scope.", status_code=404)
