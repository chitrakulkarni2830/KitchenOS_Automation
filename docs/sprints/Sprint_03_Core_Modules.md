# Sprint 3: Core Module - Recipe Management & Costing Engine

**Purpose**: Recipe management, database entity structures, scaling calculations, and recipe costing.  
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
Implement the Recipe Management Module, allowing users to create recipes, add ingredients, scale portions, and calculate recipe costs.

### Sprint Objective
Ensure the UI renders a recipe detail page with scaled quantities and calculated total costs.

---

## 2. User Stories Map

*   **Story REC-01 (Creation)**: *As an Executive Chef, I want to create recipes, specify ingredients, quantities, prep steps, and portions, so that kitchen teams have a standardized reference.*
*   **Story REC-02 (Costing)**: *As an Executive Chef, I want the system to calculate the total cost of a recipe based on active supplier catalogs, so that I can maintain recipe profit margins.*

---

## 3. Task Breakdown

### Backend & API Tasks
*   Implement API endpoints: `GET /api/v1/recipes`, `POST /api/v1/recipes`, `GET /api/v1/recipes/{id}`, `PUT /api/v1/recipes/{id}`, `DELETE /api/v1/recipes/{id}`.
*   Implement recipe cost calculation service logic in Python.
*   Create a schema validation utility.

### UI & Frontend Tasks
*   Design the Recipe Listing dashboard using Tailwind CSS grid layouts.
*   Create the Recipe Editor and detail view screens in HTML.
*   Implement Vanilla JS recipe scaling and calculation modules.

### Database Tasks
*   Define the `recipes` and `recipe_ingredients` SQLite database tables.
*   Create seed files containing sample recipes and ingredients.

### QA & Automation Tasks
*   Write Postman collections to verify the recipe management REST endpoints.
*   Write E2E test scripts in Playwright JS verifying recipe creation and scaling flows.

---

## 4. E2E Testing & Acceptance Criteria

### Acceptance Criteria
1.  Creating a recipe adds its ingredients, quantities, and prep steps to the database.
2.  Recipe costs update automatically if supplier ingredient prices change.
3.  Adjusting the portion size scaling factor updates the ingredient quantities dynamically.

---

## 5. Sprint Controls & Release Planning

*   **Estimated Complexity**: 13 Story Points
*   **Suggested Git Branches**: `feature/sprint-03-recipes`
*   **Expected Release Version**: `v0.2.0-beta`
*   **Definition of Done (DoD)**:
    *   Recipe listing and editor screens function correctly.
    *   Postman API collection test checks report zero failures.
    *   Playwright JS recipe tests pass successfully.
