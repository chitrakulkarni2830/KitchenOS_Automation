# Functional Requirements Specification

**Purpose**: System actors, detailed user stories, functional modules, and business logic requirements.  
**Version**: 1.0.0  
**Author**: KitchenOS Core Engineering Team  
**Last Updated**: July 6, 2026  

---

## Table of Contents
1. [Actors & Roles Reference](#1-actors--roles-reference)
2. [Functional Modules Overview](#2-functional-modules-overview)
3. [User Stories Map](#3-user-stories-map)
4. [Detailed Use Cases](#4-detailed-use-cases)
5. [Data Flow Diagrams](#5-data-flow-diagrams)

---

## 1. Actors & Roles Reference

We define three key user roles:

| Actor Role | Core System Access Permissions | Primary Responsibility |
| :--- | :--- | :--- |
| **System Admin** | Global configuration settings, access logs, user permissions, backup schedules. | Maintain application access controls and platform health. |
| **Executive Chef / Manager** | Full access to recipes, supplier catalogs, procurement logs, inventory sheets, reporting dashboards. | Oversee kitchen margins, purchase cycles, and recipe costing. |
| **Prep / Line Cook** | Read-only access to recipe database, write access to HACCP temperature logs, update prep sheets. | Manage day-to-day culinary operations and compliance tracking. |

---

## 2. Functional Modules Overview

```
                   ┌───────────────────────────────┐
                   │    KitchenOS Backend Core     │
                   └───────┬─────────┬─────────┬───┘
                           │         │         │
       ┌───────────────────▼┐  ┌─────▼──────┐  │ ┌──────────────────┐
       │   Recipe Module    │  │ Inventory  │  └─►   HACCP Logs     │
       └────────────────────┘  └────────────┘    └──────────────────┘
```

---

## 3. User Stories Map

### Epoch A: Recipe Management & Cost Calculation
*   **User Story REC-01**: *As an Executive Chef, I want to create, edit, and delete recipes, specifying ingredients, quantities, prep steps, and yield portions, so that kitchen teams have a standardized reference.*
*   **User Story REC-02**: *As an Executive Chef, I want the system to automatically calculate the total cost of a recipe based on active supplier catalogs, so that I can maintain recipe profit margins.*

### Epoch B: Inventory & Supplier PO Orchestration
*   **User Story INV-01**: *As a Kitchen Manager, I want to define reorder thresholds for ingredients, so that the system automatically flags low-stock items.*
*   **User Story INV-02**: *As a Kitchen Manager, I want to generate and email purchase orders directly to suppliers, reducing manual order entry times.*

### Epoch C: HACCP Compliance & Safety Records
*   **User Story HAC-01**: *As a Cook, I want to log storage room temperatures on my mobile dashboard, so that we comply with health safety regulations.*
*   **User Story HAC-02**: *As an Executive Chef, I want to receive immediate alerts when a temperature check fails, so that we can take corrective action before food spoils.*

---

## 4. Detailed Use Cases

### Use Case: Add Recipe & Auto-Calculate Cost

*   **Primary Actor**: Executive Chef
*   **Pre-conditions**: Supplier ingredients and pricing catalog are configured.
*   **Main Flow**:
    1.  Chef navigates to the Recipe Dashboard and clicks "Create Recipe".
    2.  Chef enters recipe details (name, prep time, portions) and adds ingredients by selecting them from the inventory list, specifying quantities and units.
    3.  The system queries the active supplier catalog for the unit cost of each ingredient.
    4.  The system calculates the total cost and per-portion cost of the recipe.
    5.  Chef clicks "Save Recipe", and the recipe details are saved to the database.
*   **Post-conditions**: The recipe is saved, and its cost updates dynamically if supplier ingredient prices change.

---

## 5. Data Flow Diagrams

### Recipe Cost Aggregation Flow:
```mermaid
graph TD
    Chef([Chef UI - HTML/Vanilla JS]) --> |Create Recipe| API[Python REST API]
    API --> |Query unit prices| DB[(SQLite / PostgreSQL)]
    DB -->> API: Return ingredient costs
    API --> |Apply calculations| API
    API --> |Save recipe metadata & aggregated cost| DB
    API -->> Chef: Return recipe details with calculated cost
```
