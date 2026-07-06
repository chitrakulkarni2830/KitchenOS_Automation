# Project Scope Statement

**Purpose**: High-level system boundaries, target markets, in-scope features, and exclusions.  
**Version**: 1.0.0  
**Author**: KitchenOS Core Engineering Team  
**Last Updated**: July 6, 2026  

---

## Table of Contents
1. [Target Market & Segments](#1-target-market--segments)
2. [Product Boundaries & Context](#2-product-boundaries--context)
3. [In-Scope Features (v1.0.0 Release)](#3-in-scope-features-v100-release)
4. [Out-of-Scope Modules (Future Roadmap)](#4-out-of-scope-modules-future-roadmap)
5. [Constraints & Compliance Requirements](#5-constraints--compliance-requirements)

---

## 1. Target Market & Segments

KitchenOS is designed to support the following business models:
*   **Single-location Fine Dining**: Focuses on recipe costing accuracy and supplier purchasing integration.
*   **Multi-unit Restaurant Groups**: Focuses on centralized menu configuration, supplier catalogs, and cross-site analytical reporting.
*   **Ghost Kitchens / Dark Kitchens**: Focuses on automated integration with high-volume online ordering systems and POS platforms.

---

## 2. Product Boundaries & Context

KitchenOS sits at the intersection of supply procurement, culinary operations, and sales tracking.

```
       [ Procurement / Suppliers ]
                   ▲
                   │
                   ▼
  [ POS Systems ] ◄──► [ KitchenOS Dashboard ] ◄──► [ Prep Stations / Line Cooks ]
```

KitchenOS coordinates data between external systems:
*   **Upstream**: Integrates with POS platforms to deduct inventory levels as sales occur.
*   **Downstream**: Formats procurement orders and tracks supplier catalog pricing updates.

---

## 3. In-Scope Features (v1.0.0 Release)

### 3.1. Identity & Access Management (IAM)
*   OAuth2 token validation, password hashing, and role-based permissions (`Admin`, `Chef`, `Cook`).

### 3.2. Recipe Management & Scaling Engine
*   Recipe database support.
*   Multi-unit scaling (e.g. converting a recipe from 10 portions to 150 portions).
*   Automatic recipe costing updates based on changing supplier ingredient costs.

### 3.3. Inventory & Procurement Logistics
*   Real-time stock level tracking with FIFO support.
*   Automated purchase order generation when stock levels drop below reorder margins.
*   Supplier catalog price management.

### 3.4. HACCP Compliance Management
*   Digital food storage temperature logs.
*   Sanitizer checklist tracking.
*   SMS/Email alerts when a critical threshold is breached.

### 3.5. POS Sales Integration Gateway
*   Webhook listeners to process sales logs and automatically deduct raw material counts from active inventory.

---

## 4. Out-of-Scope Modules (Future Roadmap)

These modules are excluded from the v1.0.0 release:
*   **Automated IoT Monitoring**: Direct Bluetooth/WiFi links to hardware kitchen thermometers (simulated in v1.0.0 via manual inputs).
*   **AI demand planning**: Predictive inventory ordering based on seasonal demand forecasting (scheduled for v2.0.0).
*   **Multi-tenant Franchise billing**: Complex inter-company financial invoicing.

---

## 5. Constraints & Compliance Requirements

*   **HACCP Compliance**: Data schemas must match FDA food storage standards.
*   **Data Integrity**: Inventory transactions must be processed sequentially to prevent stock allocation conflicts.
*   **Audit Logging**: Core configurations (e.g., changes to recipe ingredients or supplier pricing) must generate audit logs containing the username and timestamp of the modification.
