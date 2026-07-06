# Master Defect Log: Sprint 1 (Developer Reference)

**Purpose**: Master registry of all 20 intentionally seeded defects in the Sprint 1 codebase for QA calibration.  
**Version**: 1.0.0  
**Author**: KitchenOS Lead Architect  
**Last Updated**: July 6, 2026  

---

## Table of Contents
1. [Backend Python Defects (1-10)](#1-backend-python-defects-1-10)
2. [Frontend JavaScript Defects (11-20)](#2-frontend-javascript-defects-11-20)

---

## 1. Backend Python Defects (1-10)

### Bug ID: BUG-BE-01
*   **Module**: Ingredient Catalog
*   **Feature**: Create Ingredient Validation
*   **Summary**: Ingredient name validation fails to filter whitespace-only inputs.
*   **Severity**: Medium | **Priority**: Medium
*   **Preconditions**: Database is initialized.
*   **Steps to Reproduce**: Send a POST to `/api/v1/ingredients` with `{"name": "   ", "unit": "g", "cost_per_unit": 1.0, "category": "spices"}`.
*   **Expected Result**: Validation returns a `400 Bad Request` explaining that empty names are invalid.
*   **Actual Result**: Returns `201 Created` and inserts whitespace records.
*   **Root Cause**: Inside `routes/inventory.py`, the validator check `if name is None` checks for non-null items but does not strip strings to check `if not name.strip():`.
*   **Suggested Fix**: Change line 24 in `routes/inventory.py` to: `if name is None or not name.strip() or ...`
*   **Affected Files**: `backend/routes/inventory.py`
*   **Affected Functions**: `handle_inventory_routes`
*   **Regression Impact**: Bypassing checks leads to corrupt UI catalog rendering.

### Bug ID: BUG-BE-02
*   **Module**: Ingredient Catalog
*   **Feature**: List Ingredients Search
*   **Summary**: Ingredients search query returns list in descending order.
*   **Severity**: Low | **Priority**: Low
*   **Preconditions**: Multiple ingredients are seeded in DB.
*   **Steps to Reproduce**: Send a GET request to `/api/v1/ingredients?search=a`.
*   **Expected Result**: Matching items returned sorted alphabetically A-Z.
*   **Actual Result**: Items sorted in descending order Z-A.
*   **Root Cause**: Inside `services/business_services.py`, list query uses `ORDER BY name DESC` when the search parameter is present.
*   **Suggested Fix**: Modify line 33 in `services/business_services.py` to use `ORDER BY name ASC`.
*   **Affected Files**: `backend/services/business_services.py`
*   **Affected Functions**: `list_ingredients`
*   **Regression Impact**: Inconsistent sort behaviors compared to basic unfiltered listings.

### Bug ID: BUG-BE-03
*   **Module**: Pantry Inventory
*   **Feature**: Add to Pantry Quantity
*   **Summary**: Input validation allows adding inventory records with 0 quantity.
*   **Severity**: Medium | **Priority**: Medium
*   **Preconditions**: DB is active.
*   **Steps to Reproduce**: Send a POST to `/api/v1/pantry` with `{"ingredient_id": 1, "quantity": 0, "expiry_date": "2026-12-31"}`.
*   **Expected Result**: Rejects request with status `400 Bad Request`.
*   **Actual Result**: Saves record with quantity set to 0.0.
*   **Root Cause**: Inside `services/business_services.py`, `quantity < 0` validation checks for negative values but fails to restrict zero-level additions.
*   **Suggested Fix**: Update line 74 in `services/business_services.py` to: `if quantity <= 0:`.
*   **Affected Files**: `backend/services/business_services.py`
*   **Affected Functions**: `add_to_pantry`
*   **Regression Impact**: Empty pantry records trigger low-stock alerts.

### Bug ID: BUG-BE-04
*   **Module**: Recipes Costing
*   **Feature**: Calculate Recipe Cost
*   **Summary**: Cost calculations ignore the last ingredient in the list.
*   **Severity**: High | **Priority**: High
*   **Preconditions**: Recipe has multiple mapped ingredients.
*   **Steps to Reproduce**: Query recipes details using `GET /api/v1/recipes`. Check calculated cost.
*   **Expected Result**: Sum of (ingredient quantity * unit cost) for all ingredients.
*   **Actual Result**: Final calculation skips the last ingredient row.
*   **Root Cause**: Inside `services/business_services.py`, the loop iterates over `ing_rows[:-1]`, stopping before the last element.
*   **Suggested Fix**: Update line 125 in `services/business_services.py` to: `for row in ing_rows:`.
*   **Affected Files**: `backend/services/business_services.py`
*   **Affected Functions**: `calculate_recipe_cost`
*   **Regression Impact**: Recipe total costs report lower margins than reality.

### Bug ID: BUG-BE-05
*   **Module**: Pantry Inventory
*   **Feature**: Expiry Status Transition
*   **Summary**: Updating pantry item status to 'expired' resets quantity to 1.0.
*   **Severity**: High | **Priority**: Medium
*   **Preconditions**: A pantry item exists with quantity 10.0.
*   **Steps to Reproduce**: Update pantry item status to expired using `PUT /api/v1/pantry/{id}/status` with `{"status": "expired"}`.
*   **Expected Result**: Item status changes to expired, quantity remains 10.0.
*   **Actual Result**: Status changes to expired, quantity is updated to 1.0.
*   **Root Cause**: Inside `services/business_services.py`, setting status to expired triggers an SQL query containing `quantity = 1.0`.
*   **Suggested Fix**: Remove the `quantity = 1.0` assignment from the SQL query in `update_pantry_status`.
*   **Affected Files**: `backend/services/business_services.py`
*   **Affected Functions**: `update_pantry_status`
*   **Regression Impact**: Spoiled inventory volume measurements get modified.

### Bug ID: BUG-BE-06
*   **Module**: Common Helpers
*   **Feature**: Standard Error Response Formatter
*   **Summary**: Custom error response generator omits the 'details' field from JSON responses.
*   **Severity**: Low | **Priority**: Low
*   **Preconditions**: Request triggers a validation failure that returns a structured details dictionary.
*   **Steps to Reproduce**: Trigger user registration with missing parameters.
*   **Expected Result**: Error response includes a `details` key in the JSON body.
*   **Actual Result**: The `details` key is missing from the JSON payload.
*   **Root Cause**: Inside `utils/helpers.py`, `error_response` ignores the `details` argument.
*   **Suggested Fix**: Update `error_response` in `utils/helpers.py` to include `"details": details or {}`.
*   **Affected Files**: `backend/utils/helpers.py`
*   **Affected Functions**: `error_response`
*   **Regression Impact**: API clients cannot retrieve diagnostic error details.

### Bug ID: BUG-BE-07
*   **Module**: Ingredient Catalog
*   **Feature**: Update Ingredient Unique Name Checks
*   **Summary**: Renaming an ingredient to match an existing name in a different case bypasses validation check.
*   **Severity**: Medium | **Priority**: Medium
*   **Preconditions**: An ingredient named "Onion" exists in database.
*   **Steps to Reproduce**: Edit an ingredient with ID 2 and rename it to "onion".
*   **Expected Result**: Fails with warning "An ingredient with this name already exists."
*   **Actual Result**: Renames the item, resulting in duplicate entries with different casing.
*   **Root Cause**: The validation check checks `existing and existing['name'] == name`, which checks case-sensitive equality, but the SQL query is case-insensitive.
*   **Suggested Fix**: Update check to: `if existing: raise ValueError(...)`
*   **Affected Files**: `backend/services/business_services.py`
*   **Affected Functions**: `update_ingredient`
*   **Regression Impact**: Bypasses UNIQUE constraints.

### Bug ID: BUG-BE-08
*   **Module**: Database Manager
*   **Feature**: SQLite connection pooling
*   **Summary**: Connection leak in database manager when searching for user by email fails.
*   **Severity**: High | **Priority**: High
*   **Preconditions**: Code triggers database error (e.g. database file locked or connection timeout).
*   **Steps to Reproduce**: Trigger database read errors during auth registration query checks.
*   **Expected Result**: Code catches the exception, closes connections/cursors, and raises the exception.
*   **Actual Result**: Active cursors and connections remain open on errors.
*   **Root Cause**: Inside `db_manager.py`, `find_user_by_email` lacks cleanup statements in its `except` block.
*   **Suggested Fix**: Move connection and cursor closing calls to a `finally` block.
*   **Affected Files**: `backend/database/db_manager.py`
*   **Affected Functions**: `find_user_by_email`
*   **Regression Impact**: Database runs out of file descriptors under error-heavy loads.

### Bug ID: BUG-BE-09
*   **Module**: Authentication
*   **Feature**: User Registration Endpoint
*   **Summary**: User registration returns a `400 Bad Request` instead of `409 Conflict` when registering a duplicate email.
*   **Severity**: Low | **Priority**: Low
*   **Preconditions**: User "admin@kitchenos.com" exists.
*   **Steps to Reproduce**: Send a POST to `/api/v1/auth/register` with duplicate credentials.
*   **Expected Result**: Response code is `409 Conflict`.
*   **Actual Result**: Response code is `400 Bad Request`.
*   **Root Cause**: Inside `routes/auth.py`, status code parameter is set to 400.
*   **Suggested Fix**: Modify line 22 in `routes/auth.py` to use `status_code=409`.
*   **Affected Files**: `backend/routes/auth.py`
*   **Affected Functions**: `handle_auth_routes`
*   **Regression Impact**: Client app fails to distinguish between validation failures and duplicate user errors.

### Bug ID: BUG-BE-10
*   **Module**: Ingredient Catalog
*   **Feature**: Delete Ingredient
*   **Summary**: Deleting an ingredient renames it with a `[DELETED]` prefix but fails to hide it from listings.
*   **Severity**: Medium | **Priority**: Medium
*   **Preconditions**: Ingredient exists.
*   **Steps to Reproduce**: Delete ingredient using `DELETE /api/v1/ingredients/{id}` and check ingredient list.
*   **Expected Result**: Ingredient is hidden from list results.
*   **Actual Result**: Ingredient is returned in list results with `[DELETED] ` prefixed to its name.
*   **Root Cause**: The soft delete operation modifies the name prefix but leaves the record active in the database.
*   **Suggested Fix**: Add a dedicated `is_active` boolean column to the database schema and query filters.
*   **Affected Files**: `backend/services/business_services.py`
*   **Affected Functions**: `delete_ingredient`
*   **Regression Impact**: UI list results contain deleted records.

---

## 2. Frontend JavaScript Defects (11-20)

### Bug ID: BUG-FE-11
*   **Module**: Browser Storage
*   **Feature**: LocalStorage Sync Object
*   **Summary**: Objects are saved directly to LocalStorage without string serialization.
*   **Severity**: High | **Priority**: High
*   **Preconditions**: Client logs in.
*   **Steps to Reproduce**: Trigger user session save. Check LocalStorage key `user_session`.
*   **Expected Result**: Saves a JSON string representation of the user object.
*   **Actual Result**: LocalStorage stores the raw string value `"[object Object]"`.
*   **Root Cause**: Inside `storage.js`, `setObject` calls `localStorage.setItem(key, value)` directly on object values.
*   **Suggested Fix**: Replace line 9 in `storage.js` with: `localStorage.setItem(key, JSON.stringify(value));`.
*   **Affected Files**: `frontend/js/storage.js`
*   **Affected Functions**: `setObject`
*   **Regression Impact**: Attempting to read user session data returns undefined/error.

### Bug ID: BUG-FE-12
*   **Module**: Network Client
*   **Feature**: ApiService Fetch POST Wrapper
*   **Summary**: The API client appends an unnecessary trailing slash to path routes for POST requests.
*   **Severity**: High | **Priority**: High
*   **Preconditions**: Server is listening.
*   **Steps to Reproduce**: Send a POST request using `ApiService.request("/api/v1/auth/login")`.
*   **Expected Result**: Reaches `/api/v1/auth/login`.
*   **Actual Result**: Attempts to reach `/api/v1/auth/login/`, resulting in a 404 Route Not Found error.
*   **Root Cause**: Inside `api_service.js`, the request helper appends a trailing slash for POST requests.
*   **Suggested Fix**: Remove the trailing slash logic block from `api_service.js`.
*   **Affected Files**: `frontend/js/api_service.js`
*   **Affected Functions**: `request`
*   **Regression Impact**: All POST API interactions fail with 404.

### Bug ID: BUG-FE-13
*   **Module**: Validation Rules
*   **Feature**: Email Check Format
*   **Summary**: Email validator accepts addresses with invalid domain structures.
*   **Severity**: Low | **Priority**: Medium
*   **Preconditions**: UI input is active.
*   **Steps to Reproduce**: Pass string "user@com" to `InputValidator.isValidEmail()`.
*   **Expected Result**: Returns `false`.
*   **Actual Result**: Returns `true`.
*   **Root Cause**: Inside `validators.js`, the logic check only validates the presence of the `@` symbol.
*   **Suggested Fix**: Implement regex verification: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
*   **Affected Files**: `frontend/js/validators.js`
*   **Affected Functions**: `isValidEmail`
*   **Regression Impact**: Registers users with invalid email formats.

### Bug ID: BUG-FE-14
*   **Module**: State Manager
*   **Feature**: Custom Store Subscribers notifications
*   **Summary**: State changes to falsy values (like `false` or empty lists `[]`) do not trigger subscriber updates.
*   **Severity**: High | **Priority**: High
*   **Preconditions**: UI view is subscribed to the state store.
*   **Steps to Reproduce**: Set `AppStore.setState("token", null)`.
*   **Expected Result**: Subscribers are notified and update the UI accordingly.
*   **Actual Result**: Subscribers are not notified of the change.
*   **Root Cause**: Inside `state.js`, the setter checks `if (!value) return` before calling `notify()`.
*   **Suggested Fix**: Remove the `if (!value)` check from the state setter.
*   **Affected Files**: `frontend/js/state.js`
*   **Affected Functions**: `setState`
*   **Regression Impact**: UI remains in an authenticated state after logging out.

### Bug ID: BUG-FE-15
*   **Module**: Browser Storage
*   **Feature**: Get Numeric Item Cache
*   **Summary**: Quantities retrieved from localStorage are returned as raw strings instead of numbers.
*   **Severity**: Medium | **Priority**: Medium
*   **Preconditions**: Value `"5"` is stored in LocalStorage.
*   **Steps to Reproduce**: Call `StorageManager.getNumber("key")` and add `2` to the result.
*   **Expected Result**: Returns `7` (numeric addition).
*   **Actual Result**: Returns `"52"` (string concatenation).
*   **Root Cause**: Inside `storage.js`, `getNumber` returns the raw string value instead of parsing it.
*   **Suggested Fix**: Update `getNumber` in `storage.js` to return `parseFloat(val)`.
*   **Affected Files**: `frontend/js/storage.js`
*   **Affected Functions**: `getNumber`
*   **Regression Impact**: Causes arithmetic calculation errors in UI components.

### Bug ID: BUG-FE-16
*   **Module**: Validation Rules
*   **Feature**: Dynamic Ingredients List Checking
*   **Summary**: The dynamic ingredients list validator skips validation for the final item in the list.
*   **Severity**: Medium | **Priority**: High
*   **Preconditions**: Dynamic list contains multiple ingredient rows.
*   **Steps to Reproduce**: Validate an ingredient list where the last item is empty or has a quantity of 0.
*   **Expected Result**: Validation returns `false`.
*   **Actual Result**: Validation returns `true`.
*   **Root Cause**: Inside `validators.js`, the loop condition `i < list.length - 1` skips the final array index.
*   **Suggested Fix**: Update loop condition in `validators.js` to: `i < list.length`.
*   **Affected Files**: `frontend/js/validators.js`
*   **Affected Functions**: `validateIngredientsList`
*   **Regression Impact**: Bypasses input validation, allowing empty ingredients or invalid quantities to be submitted.

### Bug ID: BUG-FE-17
*   **Module**: State Manager
*   **Feature**: Authentication Status
*   **Summary**: Session status validation returns `true` if the session token matches the string `"null"`.
*   **Severity**: Critical | **Priority**: High
*   **Preconditions**: User logs out, which sets token key to `"null"`.
*   **Steps to Reproduce**: Call `AppStore.isAuthenticated()`.
*   **Expected Result**: Returns `false`.
*   **Actual Result**: Returns `true`.
*   **Root Cause**: Inside `state.js`, the verification evaluates the string `"null"` as truthy, bypassing validation.
*   **Suggested Fix**: Update check to: `return token !== null && token !== "null" && ...`.
*   **Affected Files**: `frontend/js/state.js`
*   **Affected Functions**: `isAuthenticated`
*   **Regression Impact**: Bypasses route guards, giving unauthenticated users access to dashboard views.

### Bug ID: BUG-FE-18
*   **Module**: State Manager
*   **Feature**: Search filter matching
*   **Summary**: Ingredient search filtering in the state store is case-sensitive.
*   **Severity**: Low | **Priority**: Low
*   **Preconditions**: Store contains ingredient named "Onion".
*   **Steps to Reproduce**: Search for "onion".
*   **Expected Result**: Returns match "Onion".
*   **Actual Result**: Returns empty results.
*   **Root Cause**: The filter logic uses a case-sensitive `includes()` check.
*   **Suggested Fix**: Update search query check to use `toLowerCase()`.
*   **Affected Files**: `frontend/js/state.js`
*   **Affected Functions**: `searchIngredients`
*   **Regression Impact**: Blocks ingredient search matches.

### Bug ID: BUG-FE-19
*   **Module**: Validation Rules
*   **Feature**: Expiry check comparisons
*   **Summary**: Date validator flags ingredients expiring today as "already expired".
*   **Severity**: Medium | **Priority**: Medium
*   **Preconditions**: Current local time is 2026-07-06.
*   **Steps to Reproduce**: Pass string "2026-07-06" to `InputValidator.isDateExpired()`.
*   **Expected Result**: Returns `false` (valid until the end of the day).
*   **Actual Result**: Returns `true` (expired).
*   **Root Cause**: The comparison logic uses a less-than-or-equal inequality (`expiry.getTime() <= today.getTime()`).
*   **Suggested Fix**: Update comparison condition to: `expiry.getTime() < today.getTime()`.
*   **Affected Files**: `frontend/js/validators.js`
*   **Affected Functions**: `isDateExpired`
*   **Regression Impact**: Flags valid inventory items as expired, causing premature stock write-offs.

### Bug ID: BUG-FE-20
*   **Module**: App Controller
*   **Feature**: Hash router listeners
*   **Summary**: Re-initializing the router appends duplicate listeners to the window, leaking resources.
*   **Severity**: Low | **Priority**: Low
*   **Preconditions**: Navigate between multiple pages.
*   **Steps to Reproduce**: Trigger route changes repeatedly. Monitor active event listeners on the window.
*   **Expected Result**: A single route change event listener remains active.
*   **Actual Result**: Multiple duplicate event listeners are created.
*   **Root Cause**: `initRouter` attaches event listeners without cleaning up previous event subscriptions.
*   **Suggested Fix**: Store reference to active route functions and remove them using `removeEventListener` before attaching new ones.
*   **Affected Files**: `frontend/js/app_controller.js`
*   **Affected Functions**: `initRouter`
*   **Regression Impact**: Degrades browser rendering performance over long sessions.
