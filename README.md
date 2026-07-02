# Marka – Grade Ledger & DevOps Playground

Marka is a minimalist grade calculation application that automatically tallies category-weighted scores into a final academic mark[cite: 1, 3]. While functional as a grade tracking utility, this repository is primarily designed as a sandbox for **testing, configuring, and experimenting with CI/CD pipelines, automated testing, and DevOps infrastructure.**

---

## 🛠️ DevOps & CI/CD Focus

This project serves as a practical implementation playground for modern DevOps methodologies. It is deliberately split into a decoupled frontend and backend to mirror production enterprise setups:

* **Automated Quality Gates:** Integrated linting tools, type checkers, and test runners ensure code health before any deployment step triggers.
* **Continuous Integration (CI):** Every push or pull request automatically kicks off Python unit tests via `pytest` to guarantee calculation logic remains accurate.
* **Continuous Deployment (CD):** Validated builds are securely built and shipped straight to production domains (`karloalano.site`) via automated deployment workflows[cite: 1, 3].

---

## 🏗️ Project Architecture

The repository is structured around a standard modern web architecture:

* **Backend (`/app`):** Built with **FastAPI** (Python), exposing performance-optimized validation endpoints using Pydantic schemas[cite: 1].
* **Frontend (`/src`):** A responsive, single-page UI built using **Vue 3 (TypeScript)** and styled with **PrimeVue / Tailwind CSS**[cite: 3].
* **Tests (`/tests`):** Automated regression endpoints and math validation suites powered by **Pytest**[cite: 2].

---
