# Sprint 4: Data Management - Inventory & Procurement Log

**Purpose**: Inventory levels tracking, FIFO storage queues, auto reorders thresholds, and PO generation.  
**Version**: 1.0.0  
**Author**: KitchenOS Core Engineering Team  
**Last Updated**: July 6, 2026  

---

## Table of Contents
1. [Sprint Overview](#1-sprint-overview)
2. [User Stories Map](#2-user-stories-map)
3. [Task Breakdown](#3-task-breakdown)
4. [E2E Testing & Acceptance Criteria](#4-e2e-testing--acceptance-criteria)
5. [Sprint Controls & Release Planning](#5-sprint-controls--release-planning)

---

## 1. Sprint Overview

### Sprint Goal
Implement the Inventory and Procurement Module, allowing users to track stock levels, define reorder thresholds, and generate purchase orders.

### Sprint Objective
Ensure the UI renders an inventory dashboard, alerts users when stock levels are low, and supports manual or automated purchase order generation.

---

## 2. User Stories Map

*   **Story INV-01 (Inventory Logs)**: *As a Kitchen Manager, I want to view my inventory stock levels, so that I can see what ingredients we have on hand.*
*   **Story INV-02 (Reorder Alerts)**: *As a Kitchen Manager, I want the system to alert me when an ingredient drops below its reorder threshold, so that I can prevent stockouts.*

---

## 3. Task Breakdown

### Backend & API Tasks
*   Implement API endpoints: `GET /api/v1/inventory`, `POST /api/v1/inventory/adjust`, `GET /api/v1/purchase-orders`, `POST /api/v1/purchase-orders`.
*   Implement FIFO stock deduction service logic in Python.
*   Configure the background worker (Celery) to generate and email purchase orders.

### UI & Frontend Tasks
*   Design the Inventory Dashboard and stock levels table using Tailwind CSS tables.
*   Create HTML forms to adjust inventory levels manually, handled using Vanilla JavaScript DOM listeners.
*   Create the Purchase Order details screen.

### Database Tasks
*   Define the `inventory_levels` and `purchase_orders` SQLite database tables.
*   Create seed files containing sample inventory data.

### QA & Automation Tasks
*   Define Postman Collections checking inventory adjustments and PO generation.
*   Write E2E test scripts in Playwright JS verifying inventory adjustments.

---

## 4. E2E Testing & Acceptance Criteria

### Acceptance Criteria
1.  Adjusting stock levels manually records the transaction and updates inventory counts.
2.  Stock level alerts are displayed on the dashboard when items drop below reorder thresholds.
3.  Generating a purchase order changes its status to "Pending" and sends an email request to the supplier.

---

## 5. Sprint Controls & Release Planning

*   **Estimated Complexity**: 13 Story Points
*   **Suggested Git Branches**: `feature/sprint-04-inventory`
*   **Expected Release Version**: `v0.3.0`
*   **Definition of Done (DoD)**:
    *   Inventory level calculations are accurate.
    *   Purchase orders are generated and formatted correctly.
    *   Postman API collection verifies inventory flows.
    *   Playwright JS inventory E2E tests pass.
