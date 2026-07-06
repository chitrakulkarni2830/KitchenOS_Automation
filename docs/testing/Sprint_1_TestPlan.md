# Manual Test Plan & Test Cases - Sprint 1

**Purpose**: Test strategies, validation scenarios, and detailed test cases for KitchenOS Sprint 1.  
**Version**: 1.0.0  
**Author**: KitchenOS QA Core Team  
**Last Updated**: July 6, 2026  

---

## Table of Contents
1. [Sprint 1 Test Plan](#1-sprint-1-test-plan)
2. [Test Scenarios Matrix](#2-test-scenarios-matrix)
3. [Detailed Test Cases Catalog](#3-detailed-test-cases-catalog)

---

## 1. Sprint 1 Test Plan

### 1.1. Introduction & Objectives
The target of Sprint 1 is validating the application foundation, core Python REST APIs, and client-side Vanilla JavaScript modules. Testing is entirely manual.

### 1.2. Scope
*   **In Scope**: API health status checks, user authorization operations, ingredient database CRUD operations, pantry transactions (FIFO), recipe cost calculation adjustments, and POS webhook deductions.
*   **Out of Scope**: Automated Playwright verification, security scanning, load testing, and graphical user interfaces validation.

### 1.3. Testing Strategy
Endpoints are triggered using Postman Collection request payloads, validating status codes and returned JSON objects. JS modules are verified in isolation using test scripts.

---

## 2. Test Scenarios Matrix

| Scenario ID | Functional Module | High-Level Test Scenario |
| :--- | :--- | :--- |
| **TS-01** | System Health | Check that the backend health endpoint accurately returns status codes. |
| **TS-02** | User Identity | Verify user logins, registration check constraints, and JWT payload configurations. |
| **TS-03** | Ingredient Catalog | Verify adding, querying, updating, and soft-deleting ingredients. |
| **TS-04** | Pantry Inventory | Verify inventory levels tracking, adjustments, and expired status triggers. |
| **TS-05** | Recipes Costing | Verify dynamic ingredient pricing checks and recipe scaling calculators. |
| **TS-06** | POS Webhook Ingestion | Verify POS checkout triggers, FIFO sorting, and ingredient stock deductions. |

---

## 3. Detailed Test Cases Catalog

### 3.1. Health Check & Identity

#### Test Case: TC-SYS-01
*   **Module**: System Health
*   **Requirement**: SYS-REQ-01
*   **Objective**: Verify health check endpoint returns 200 OK and healthy status.
*   **Preconditions**: Backend server is running.
*   **Test Data**: None
*   **Test Steps**:
    1. Send a `GET` request to `http://localhost:8000/api/v1/health`.
*   **Expected Result**: Response code is `200 OK` and JSON response body is `{"success": true, "data": {"status": "healthy"}, "status_code": 200}`.
*   **Actual Result**: Matches expected.
*   **Priority**: High
*   **Status**: Passed

#### Test Case: TC-AUTH-01
*   **Module**: User Identity
*   **Requirement**: AUTH-REQ-01
*   **Objective**: Verify user registration with valid credentials.
*   **Preconditions**: Database is initialized.
*   **Test Data**: `{"email": "newuser@kitchenos.com", "password": "SecurePassword123", "role": "cook"}`
*   **Test Steps**:
    1. Send a `POST` request to `/api/v1/auth/register` with test body.
*   **Expected Result**: Response code is `201 Created`, user is saved with a hashed password, and a JWT token is returned.
*   **Actual Result**: User registration completes successfully.
*   **Priority**: High
*   **Status**: Passed

#### Test Case: TC-AUTH-02
*   **Module**: User Identity
*   **Requirement**: AUTH-REQ-02
*   **Objective**: Verify registration fails when registering an email that already exists.
*   **Preconditions**: User "admin@kitchenos.com" is already registered.
*   **Test Data**: `{"email": "admin@kitchenos.com", "password": "NewPassword123"}`
*   **Test Steps**:
    1. Send a `POST` request to `/api/v1/auth/register` with duplicate credentials.
*   **Expected Result**: Response code is `409 Conflict` (Conflict) with code `USER_EXISTS`.
*   **Actual Result**: Returns `400 Bad Request` with code `USER_EXISTS` (Defect #9).
*   **Priority**: High
*   **Status**: Failed (Defect Seeded)

---

### 3.2. Ingredient Catalog

#### Test Case: TC-ING-01
*   **Module**: Ingredient Catalog
*   **Requirement**: ING-REQ-01
*   **Objective**: Verify adding an ingredient with valid parameters.
*   **Preconditions**: User is logged in with valid JWT token.
*   **Test Data**: `{"name": "Garlic", "unit": "g", "cost_per_unit": 0.35, "category": "spices"}`
*   **Test Steps**:
    1. Send a `POST` request to `/api/v1/ingredients` with JWT in header.
*   **Expected Result**: Response code is `201 Created` with ingredient metadata.
*   **Actual Result**: Matches expected.
*   **Priority**: High
*   **Status**: Passed

#### Test Case: TC-ING-02
*   **Module**: Ingredient Catalog
*   **Requirement**: ING-REQ-02
*   **Objective**: Verify validation rejects empty or whitespace-only names.
*   **Preconditions**: User is logged in.
*   **Test Data**: `{"name": "   ", "unit": "g", "cost_per_unit": 0.10, "category": "spices"}`
*   **Test Steps**:
    1. Send a `POST` request to `/api/v1/ingredients` with whitespace name.
*   **Expected Result**: Response code is `400 Bad Request` indicating validation error.
*   **Actual Result**: Returns `201 Created` and saves ingredient with name "   " (Defect #1).
*   **Priority**: Medium
*   **Status**: Failed (Defect Seeded)

---

### 3.3. Pantry Inventory & POS webhooks

#### Test Case: TC-PAN-01
*   **Module**: Pantry Inventory
*   **Requirement**: PAN-REQ-01
*   **Objective**: Verify system flags quantity updates containing zero value.
*   **Preconditions**: User is logged in.
*   **Test Data**: `{"ingredient_id": 1, "quantity": 0, "expiry_date": "2026-12-31"}`
*   **Test Steps**:
    1. Send a `POST` request to `/api/v1/pantry` with quantity set to 0.
*   **Expected Result**: Response code is `400 Bad Request` with error explaining quantity must be positive.
*   **Actual Result**: Returns `201 Created` and adds item with 0 quantity (Defect #3).
*   **Priority**: Medium
*   **Status**: Failed (Defect Seeded)

#### Test Case: TC-POS-01
*   **Module**: POS Webhook Ingestion
*   **Requirement**: POS-REQ-01
*   **Objective**: Verify POS webhook sale successfully deducts ingredients from pantry.
*   **Preconditions**: User is logged in, "Jeera Rice" recipe is seeded, pantry has sufficient ingredients.
*   **Test Data**: `{"menu_item": "Jeera Rice", "quantity": 1}`
*   **Test Steps**:
    1. Fetch pantry stock levels for Basmati Rice (Ingredient ID 1) and Ghee (Ingredient ID 4).
    2. Send a `POST` request to `/api/v1/pos/webhook` with test data.
    3. Re-query pantry stock levels.
*   **Expected Result**: Response code is `200 OK`, and ingredient quantities are decreased based on recipe requirements.
*   **Actual Result**: Matches expected.
*   **Priority**: High
*   **Status**: Passed
