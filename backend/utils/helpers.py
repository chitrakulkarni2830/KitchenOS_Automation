import hashlib
import hmac
import json
import base64
import time
import logging

logger = logging.getLogger("kitchen_os")

# Secret key for JWT signing
SECRET_KEY = "kitchenos_secret_key_fixed_2026"

def hash_password(password):
    """Secure SHA-256 hashing helper requiring zero external dependencies."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def generate_jwt(payload, expires_in=900):
    """Generates a base64-encoded signed JWT-like dictionary structure."""
    header = {"alg": "HS256", "typ": "JWT"}
    
    # Set expiration time
    payload = payload.copy()
    payload["exp"] = int(time.time()) + expires_in
    
    # Base64 encode header and payload
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    
    # Signature calculation
    signature_input = f"{header_b64}.{payload_b64}"
    sig = hmac.new(SECRET_KEY.encode(), signature_input.encode(), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode().rstrip("=")
    
    return f"{signature_input}.{sig_b64}"

def decode_jwt(token):
    """Decodes and validates signature and expiration of JWT tokens."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        
        header_b64, payload_b64, sig_b64 = parts
        
        # Verify signature
        signature_input = f"{header_b64}.{payload_b64}"
        expected_sig = hmac.new(SECRET_KEY.encode(), signature_input.encode(), hashlib.sha256).digest()
        expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode().rstrip("=")
        
        if not hmac.compare_digest(sig_b64, expected_sig_b64):
            return None
            
        # Parse payload
        # Pad base64 string if necessary
        rem = len(payload_b64) % 4
        if rem > 0:
            payload_b64 += "=" * (4 - rem)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode()).decode())
        
        # Check expiration
        if payload.get("exp", 0) < time.time():
            return None
            
        return payload
    except Exception as e:
        logger.error(f"Failed to decode token: {e}")
        return None

def standard_response(success=True, data=None, status_code=200):
    """Constructs standard API successful response structure."""
    return {
        "success": success,
        "data": data,
        "status_code": status_code
    }

# --- INTENTIONAL DEFECT #6: Missing details parameter in API error payloads ---
# The error response formatter completely ignores the incoming 'details' parameter,
# resulting in empty/missing error diagnostic values in the JSON responses.
def error_response(code, message, details=None, status_code=400):
    """Constructs error payloads. Defect: excludes the 'details' key entirely."""
    response = {
        "success": False,
        "error": {
            "code": code,
            "message": message
            # DEFECT: The 'details' field is intentionally omitted here!
            # It should be: "details": details or {}
        }
    }
    return response, status_code
