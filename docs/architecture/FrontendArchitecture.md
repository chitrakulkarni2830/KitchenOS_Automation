# Frontend Architecture Specification

**Purpose**: Standards, folder architectures, state conventions, and layouts for the HTML5 / Tailwind / Vanilla JavaScript client application.  
**Version**: 1.0.0  
**Author**: KitchenOS Core Engineering Team  
**Last Updated**: July 6, 2026  

---

## Table of Contents
1. [Core Presentation & Layout Decisions](#1-core-presentation--layout-decisions)
2. [State Management & Local Cache Model](#2-state-management--local-cache-model)
3. [Design System & Tailwind CSS Strategy](#3-design-system--tailwind-css-strategy)
4. [API Orchestration & Client Requests](#4-api-orchestration--client-requests)
5. [Client-Side Routing & View Transitions](#5-client-side-routing--view-transitions)
6. [Performance Optimization Targets](#6-performance-optimization-targets)

---

## 1. Core Presentation & Layout Decisions

KitchenOS frontend is built using **HTML5 semantic tags**, styled with **Tailwind CSS**, and powered by **Vanilla JavaScript (ES6+)**. The application is designed as a modular, framework-free single page application (SPA).

### Key Features
*   **Semantic Structure**: Heavy reliance on structural tags (`<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>`) to ensure accessibility and clear page divisions.
*   **No Virtual DOM**: Uses standard Web APIs (e.g. `document.getElementById()`, `querySelector()`, `addEventListener()`) to update the DOM.
*   **Modular Scripts**: JavaScript is split into functional modules using native import/export statements (`<script type="module" src="js/app.js">`).

---

## 2. State Management & Local Cache Model

Without component frameworks, state is managed in memory and persisted in the browser storage:

```
[ Client UI Events ]
         │
         ├── (Local DOM Transitions) ───► [ Local Variable Objects / DOM state ]
         │
         ├── (User Sessions Context) ───► [ LocalStorage / SessionStorage ]
         │
         └── (DB API Request Cache) ────► [ In-memory JS cache dictionary ]
```

1.  **Session Cache (`localStorage` / `sessionStorage`)**:
    *   `localStorage` retains user-selected dashboard preferences (e.g. sidebar toggle configurations).
    *   `sessionStorage` tracks session data, including user access scopes and usernames.
2.  **API Client Cache (In-Memory)**:
    *   A simple JavaScript cache dictionary stores temporary data (e.g., active supplier catalogs) with expiration timestamps, preventing redundant API requests during page navigation.

---

## 3. Design System & Tailwind CSS Strategy

We use **Tailwind CSS** for layout styling.

### Configuration (`tailwind.config.js`)
```javascript
module.exports = {
  content: ["./frontend/**/*.html", "./frontend/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        'kitchen-bg-dark': '#0B0F19',
        'kitchen-bg-card': '#161B26',
        'kitchen-accent': '#22C55E', // Safe green
        'kitchen-danger': '#EF4444', // Warning red
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
```

---

## 4. API Orchestration & Client Requests

*   **HTTP Client**: Built using the native browser `fetch()` API.
*   **Request Interceptor**: A wrapper function automatically appends the JWT access token to request headers and handles `401 Unauthorized` responses by redirecting the user to the login screen.

---

## 5. Client-Side Routing & View Transitions

We use a simple hash-based router (`#/recipes`, `#/inventory`) to manage client-side routing:

```javascript
// frontend/js/app.js
const routes = {
  '#/dashboard': showDashboard,
  '#/recipes': showRecipes,
  '#/inventory': showInventory
};

function handleRouting() {
  const hash = window.location.hash || '#/dashboard';
  const renderFunction = routes[hash];
  
  if (renderFunction) {
    renderFunction();
  } else {
    showErrorPage();
  }
}

window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);
```

---

## 6. Performance Optimization Targets

*   **First Contentful Paint (FCP)**: < 0.8s (made possible by framework-free rendering).
*   **Asset Bundling**: CSS files are built and optimized using the Tailwind CLI compilation process.
*   **Code Splitting**: JavaScript modules are loaded dynamically (`import()`) when navigating to specific routes.
