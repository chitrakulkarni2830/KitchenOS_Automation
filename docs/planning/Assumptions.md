# Project Assumptions & Constraints

**Purpose**: Critical assumptions, baseline requirements, and environmental boundaries.  
**Version**: 1.0.0  
**Author**: KitchenOS Core Engineering Team  
**Last Updated**: July 6, 2026  

---

## Table of Contents
1. [Engineering Team Capabilities](#1-engineering-team-capabilities)
2. [Infrastructure & Environment Assumptions](#2-infrastructure--environment-assumptions)
3. [Third-Party Integrations & APIs](#3-third-party-integrations--apis)
4. [Regulatory & Standard Compliance Constraints](#4-regulatory--standard-compliance-constraints)

---

## 1. Engineering Team Capabilities

*   **Python Proficiency**: Developers possess experience in modular Python REST APIs, routing frameworks, and database connectors.
*   **Vanilla JS & Tailwind CSS**: UI engineers are familiar with Tailwind utility configurations and writing native ES6 JavaScript modules without component frameworks.
*   **Playwright (JavaScript)**: QA engineers have experience writing automated E2E tests in JavaScript.
*   **Postman Collection testing**: Team members can create and run Postman test assertions using Newman.

---

## 2. Infrastructure & Environment Assumptions

*   **Local Environments**: Developers can run Docker and docker-compose locally, using at least 16GB of RAM.
*   **Database Isolation**: Local databases run SQLite in development and PostgreSQL in staging and production.
*   **SMTP Services**: We assume the availability of SMTP services for user invitations and email notifications.

---

## 3. Third-Party Integrations & APIs

*   **POS Webhooks**: POS platforms support standard webhook structures and send transaction payloads via HTTPS POST requests.
*   **Network Latency**: We assume the network latency between the KitchenOS backend and external supplier endpoints remains under 200ms.

---

## 4. Regulatory & Standard Compliance Constraints

*   **HACCP Regulations**: System logs must align with FDA standards for food storage temperature monitoring.
*   **Local Time Zones**: The system must store timestamps in UTC, and convert them to local time zones in the frontend.
*   **Audit Trail Compliance**: Users cannot delete or modify log entries, ensuring audit integrity.
