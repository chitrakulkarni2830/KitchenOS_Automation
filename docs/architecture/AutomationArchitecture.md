# Automation Testing Architecture Specification

**Purpose**: Test runners layout, E2E browser tests, Postman API collections verification, and CI pipeline gates.  
**Version**: 1.0.0  
**Author**: KitchenOS Core Engineering Team  
**Last Updated**: July 6, 2026  

---

## Table of Contents
1. [Test Framework Selection](#1-test-framework-selection)
2. [E2E Testing Layout & Page Objects (POM)](#2-e2e-testing-layout--page-objects-pom)
3. [Postman API Automation Testing](#3-postman-api-automation-testing)
4. [E2E Execution Lifecycles](#4-e2e-execution-lifecycles)
5. [Cross-Browser & Responsive Sizing Testing](#5-cross-browser--responsive-sizing-testing)
6. [CI/CD Pipeline Integration Gates](#6-ci-cd-pipeline-integration-gates)

---

## 1. Test Framework Selection

We use a two-tier automation testing architecture:
1.  **API Verification (Postman & Newman)**: Postman collections and environment variables define integration tests for all REST endpoints, executed via Newman CLI.
2.  **E2E UI Verification (Playwright JS)**: Node Playwright written in JavaScript handles functional UI validation.

---

## 2. E2E Testing Layout & Page Objects (POM)

E2E testing assets are isolated inside the `automation/` folder:

```
automation/
├── tests/
│   ├── auth.spec.js          # Playwright test scripts (JavaScript)
│   └── inventory.spec.js     # Inventory adjustment scripts (JavaScript)
├── fixtures/
│   └── page-objects/         # Page Object Model (POM) files
│       ├── login.page.js     # Login selectors helper
│       └── inventory.page.js # Inventory elements helper
├── playwright.config.js      # Playwright configurations
└── package.json              # E2E dependencies configuration
```

---

## 3. Postman API Automation Testing

*   **Collections**: API endpoints are organized into Postman Collections (`postman/KitchenOS.postman_collection.json`).
*   **Environment Variables**: Dynamic variables (e.g. host URLs, access tokens) are stored in environment profiles (`postman/Dev.postman_environment.json`).
*   **Automated Tests**: Postman test scripts verify response codes, schema validations, and response payload structures:

```javascript
// Postman API test snippet example
pm.test("Status code is 200 OK", function () {
    pm.response.to.have.status(200);
});

pm.test("Response returns a valid JWT token", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property("access_token");
});
```

---

## 4. E2E Execution Lifecycles

Playwright tests use JavaScript module files. Page Object Models encapsulate selectors and actions:

```javascript
// automation/fixtures/page-objects/login.page.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('#email-input');
    this.passwordInput = page.locator('#password-input');
    this.loginButton = page.locator('#login-button');
  }

  async login(email, secret) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(secret);
    await this.loginButton.click();
  }
}
module.exports = { LoginPage };
```

---

## 5. Cross-Browser & Responsive Sizing Testing

*   **Browsers**: Playwright executes tests across Chromium, WebKit, and Firefox.
*   **Responsive Viewports**:
    *   *Desktop*: 1280x720.
    *   *Mobile*: Portrait viewports (e.g., iPhone 13 profile at 390x844) to verify responsive sidebar collapsible menu behaviors.

---

## 6. CI/CD Pipeline Integration Gates

*   ** Newman Execution**:
    ```bash
    newman run postman/KitchenOS.postman_collection.json -e postman/Dev.postman_environment.json --reporters cli,junit --reporter-junit-export reports/test-results/api-report.xml
    ```
*   **Playwright Execution**:
    ```bash
    npx playwright test --config=automation/playwright.config.js --reporter=html
    ```
*   **Reports**: Test outputs are compiled in HTML format under `reports/test-results/`, detailing pass rates and execution traces.
