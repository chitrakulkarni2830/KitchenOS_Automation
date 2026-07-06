# Backend Architecture Specification

**Purpose**: Technical standards, request flows, database interaction patterns, and performance limits for the Python modular REST API application.  
**Version**: 1.0.0  
**Author**: KitchenOS Core Engineering Team  
**Last Updated**: July 6, 2026  

---

## Table of Contents
1. [Core Design Architecture](#1-core-design-architecture)
2. [API Design & Routing Conventions](#2-api-design--routing-conventions)
3. [Asynchronous Task Architecture](#3-asynchronous-task-architecture)
4. [Request Lifecycle & Middleware](#4-request-lifecycle--middleware)
5. [Error Handling & Response Standardization](#5-error-handling--response-standardization)
6. [Security & Authentication Specs](#6-security--authentication-specs)

---

## 1. Core Design Architecture

KitchenOS adopts a **Python Modular REST API** structure. Rather than relying on a heavy framework, the application utilizes a modular design that decouples:
*   **Routes**: URL controllers that handle requests and map inputs.
*   **Services**: Core business logic and validations.
*   **Models**: Entities that map database schemas onto classes.
*   **Utilities**: Common helpers (database connections, cryptology helpers).

---

## 2. API Design & Routing Conventions

All APIs comply with RESTful standards and output JSON payloads.

### Versioning:
All routes must use version prefixes: `/api/v1/[resource]`.

### Route Mapping Examples:
*   `GET /api/v1/recipes` — Retrieve recipe listings (query parameters supported: `page`, `limit`, `search`).
*   `POST /api/v1/recipes` — Create a new recipe.
*   `GET /api/v1/recipes/{id}` — Fetch details for a specific recipe.
*   `PUT /api/v1/recipes/{id}` — Update a recipe.
*   `DELETE /api/v1/recipes/{id}` — Mark a recipe as inactive.

---

## 3. Asynchronous Task Architecture

Operations that exceed **100ms** processing duration must run out of the request-response thread via Celery workers:

```
[ Python App ] --> (Publish Task Payload) --> [ Redis Queue ]
                                                   │
                                                   ▼
[ Database Store ] <-- (Update Database) <-- [ Celery Worker Pod ]
```

### Async Offloading Candidates:
1.  **PDF/CSV Generation**: Generating monthly purchase orders and cost analysis reports.
2.  **External Integrations**: Sending webhook payloads to supplier inventory networks.
3.  **Real-Time Notifications**: Broadcasting high-temperature alert messages when a HACCP check fails.

---

## 4. Request Lifecycle & Middleware

Requests process through the following pipeline:

```
[ Incoming Request ]
         │
         ▼
[ CORS Validation ] ─────────► (Validates allowed domain access origins)
         │
         ▼
[ Logging / Request-ID ] ────► (Registers unique Request-ID, path, and duration metrics)
         │
         ▼
[ Authentication Guard ] ───► (Decodes JWT token, checks role access in Database)
         │
         ▼
[ Router Controller ] ───────► (Calls business services & database transactions)
         │
         ▼
[ Response Serialization ]
```

---

## 5. Error Handling & Response Standardization

We use standard response schemas for successful operations and errors to ensure consistent handling on the frontend.

### Error Payload Format:
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "Stock level for Ingredient ID 203 cannot drop below zero.",
    "details": {
      "requested_deduction": 50,
      "current_stock": 20
    }
  }
}
```

### Custom Exception Handler:
```python
class BusinessRuleViolation(Exception):
    def __init__(self, code: str, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}

def error_response(exc: BusinessRuleViolation):
    return {
        "success": False,
        "error": {
            "code": exc.code,
            "message": exc.message,
            "details": exc.details
        }
    }
```

---

## 6. Security & Authentication Specs

*   **OAuth2 / Bearer Token**: Standard configuration utilizing JWT tokens.
*   **Token Expiration**: Access Tokens expire in 15 minutes. Refresh Tokens expire in 7 days and are stored as HTTP-only secure cookies.
*   **Hashing Engine**: Passwords are hashed using BCrypt.
*   **Rate Limiting**: IP-based rate limiting on sensitive login/registration endpoints (max 5 login attempts per minute).
