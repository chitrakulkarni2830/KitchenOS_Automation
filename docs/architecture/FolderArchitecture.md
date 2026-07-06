# Folder Architecture & Layering Guidelines

**Purpose**: Standards, constraints, and architecture pattern mappings for directories and file structures inside the repository.  
**Version**: 1.0.0  
**Author**: KitchenOS Core Engineering Team  
**Last Updated**: July 6, 2026  

---

## Table of Contents
1. [Architectural Style: Modular Layered Architecture](#1-architectural-style-modular-layered-architecture)
2. [Backend Folder Architecture Guidelines](#2-backend-folder-architecture-guidelines)
3. [Frontend Folder Architecture Guidelines](#3-frontend-folder-architecture-guidelines)
4. [Import Boundary Rules (Dependency Rule)](#4-import-boundary-rules-dependency-rule)
5. [Enforcement Mechanisms](#5-enforcement-mechanisms)

---

## 1. Architectural Style: Modular Layered Architecture

KitchenOS codebase follows a **Modular Layered Monolith** pattern. This separates routing controllers, core business logic services, database entities, and common utility modules.

```
       ┌─────────────────────────────────────┐
       │     Presentation (HTML5/Tailwind)   │
       └──────────────────┬──────────────────┘
                          ▼
       ┌─────────────────────────────────────┐
       │          API Routes Layer           │
       └──────────────────┬──────────────────┘
                          ▼
       ┌─────────────────────────────────────┐
       │     Business Services Layer         │
       └──────────────────┬──────────────────┘
                          ▼
       ┌─────────────────────────────────────┐
       │       Entities / Models Layer       │
       └─────────────────────────────────────┘
```

---

## 2. Backend Folder Architecture Guidelines

The Python application structure implements clean separation of concerns:

```
backend/
├── routes/          # API Controllers: Map HTTP verbs to business services endpoints
├── services/        # Service Core: Business rules execution, validations, calculations
├── models/          # Entity Layer: Maps database schemas onto Python classes
└── utils/           # Utilities: Database connection pools, JWT token generators, hashing helpers
```

### Folder Responsibilities:
*   **`routes/`**: Parses incoming HTTP requests, validates query strings, and calls business services. **No direct business logic or SQL queries should reside here**.
*   **`services/`**: The core driver. Processes calculations, adjusts inventory counts, and initiates background events.
*   **`models/`**: Maps database schemas, constraints, and validation rules to objects.
*   **`utils/`**: Reusable modules for database execution context, token validation, and encryption.

---

## 3. Frontend Folder Architecture Guidelines

The Vanilla frontend relies on standard CSS, HTML markup, Tailwind utility classes, and Vanilla JS modules:

```
frontend/
├── css/             # Stylesheets directory containing Tailwind configs and global imports
├── js/              # Vanilla Javascript module code files
│   ├── app.js       # App entry point, handles navigation routing & state
│   ├── auth.js      # Auth forms events & token cookies operations
│   └── inventory.js # DOM integrations for stock boards
├── index.html       # Single Page Application entry template
└── tailwind.config.js # Tailwind CSS configuration
```

### Folder Guidelines:
1.  **`index.html`**: Contains the semantic layout, linking to the stylesheet and importing modules (using `<script type="module" src="js/app.js">`).
2.  **`css/`**: Houses Tailwind directives (`@tailwind base;`, `@tailwind components;`, `@tailwind utilities;`) compiled to standard CSS.
3.  **`js/`**: Explicit ES6 modules. Direct DOM manipulations are localized inside respective views JS modules (e.g. `inventory.js`).

---

## 4. Import Boundary Rules (Dependency Rule)

To prevent spaghetti dependencies and maintain codebase testability:

### Backend Import Rules
*   **`services`** can import from **`models`** and **`utils`**, but never from **`routes`**.
*   **`routes`** can import from **`services`** and **`utils`**, but never directly run SQL queries or bypass the service layer.
*   No service module may cross-import other services. Shared features should be grouped in utility classes or triggered using event handlers.

### Frontend Import Rules
*   JavaScript views modules (like `inventory.js`) should focus on DOM manipulations and UI events, routing HTTP requests through utility modules.
*   Avoid inline `<script>` tags in `index.html`. All logic must be contained in the `/js/` directory.

---

## 5. Enforcement Mechanisms

*   **ESLint/Pylint Checkers**: Validates code conventions on every PR build.
*   **Import Audits**: Static analysis checks fail the pipeline if circular dependencies are detected in backend or frontend modules.
*   **Tailwind Audits**: Tailwind CLI verifies that compiled assets don't include unreferenced classes.
