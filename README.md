# 🤖 B2B Fleet Aggregator API

**Author:** Sandesh Hegde  
**Architecture:** Headless FastAPI Microservice (B2B Aggregator)  
**Status:** 🟢 Live in Production / Stable (v1.0.0)

**Live API Documentation:** [Interactive Swagger UI](https://b2b-fleet-api.onrender.com/docs) *(Note: Hosted on Render Free Tier. Please allow 30s for cold start.)*

---

## 📖 Executive Summary

The **B2B Fleet Aggregator API** is a high-performance middleware designed to bridge the gap between demand-side strategic supply chain planning and supply-side physical assets.

While the **[LSP Digital Capacity Twin](https://github.com/sandesh-s-hegde/digital_capacity_optimizer)** serves as the Macro-Strategic Layer (forecasting shortfalls and volume surges), this API acts as the **Tactical Execution Engine**. It aggregates commercial vehicle availability from multiple third-party suppliers (e.g., Enterprise, Ryder, Hertz) into a unified, searchable, and actionable interface for seamless capacity fulfillment.

---

## 🎯 The Business Problem

In the travel and logistics tech sectors, the "Integration Gap" is a multi-million dollar problem. A strategic AI model might successfully identify a need for 50 additional vans in Europe, but the physical execution fails because:
1. **Fragmentation:** Suppliers use entirely different API standards and data schemas, making real-time comparison impossible.
2. **Static Data:** Supplier availability is often outdated in legacy systems, leading to failed bookings and lost revenue.
3. **ESG Blindspots:** Legacy procurement systems fail to prioritize low-emission or EV options during the search phase, hindering corporate sustainability goals.

**This API solves the "Macro-Micro Gap."** By providing a standardized, stateful microservice that tracks inventory, calculates dynamic surge pricing, sorts by carbon telemetry, and manages the complete lifecycle, we transform theoretical capacity needs into real-world, executable bookings.

---

## 🛠️ Technology Stack

* **Language:** Python 3.11+
* **Framework:** FastAPI (RESTful routing and OpenAPI 3.1 generation)
* **Database:** PostgreSQL (via SQLAlchemy ORM & Session Pooling)
* **Validation:** Pydantic v2 (Strict data contracts)
* **DevOps:** Docker Compose (IaC) & Windows DX Scripts (`.bat`)
* **Testing:** Postman Behavior-Driven Development (BDD) automated suites

---

## 🏗️ System Architecture & Core Endpoints

The project follows a strict "Clean Architecture" pattern to ensure high scalability:

### 📊 System & Analytics
* `GET /api/v1/health` - Deep system health check (API + Database Ping). *Used for automated Uptime telemetry.*
* `GET /api/v1/fleet/utilization` - Real-time fleet utilization metrics.
* `GET /api/v1/fleet/revenue` - Aggregates financial telemetry from confirmed B2B bookings.

### 🚛 Fleet Management & Aggregation
* `GET /api/v1/vehicles` - Live Supplier Catalog retrieval.
* `POST /api/v1/vehicles` - Register new supplier inventory.
* `POST /api/v1/vehicles/batch` - Ingest bulk payloads for high-volume supplier syncs.
* `DELETE /api/v1/vehicles/{vehicle_id}` - Safely retire inventory (validates active bookings).
* `POST /api/v1/fleet/search` - Multi-criteria search engine (Filters availability, sorts by lowest CO2 emissions and daily rate).

### 🔒 Stateful Booking Engine *(Secured via API Key)*
* `POST /api/v1/bookings` - Execute secure B2B booking with dynamic surge pricing.
* `GET /api/v1/bookings/{partner_id}` - Retrieve active partner itineraries.
* `PATCH /api/v1/bookings/{booking_reference}/cancel` - Cancel booking and dynamically release inventory back to the market.

---

## 🚀 Local Installation & Setup

### 1. Clone & Environment

```bash
git clone https://github.com/sandesh-s-hegde/b2b-fleet-aggregator-api.git
cd b2b-fleet-aggregator-api
python -m venv venv

# Activate (Windows):
.\venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Copy the provided template to configure your local secure credentials:

```bash
cp .env.example .env
```

### 4. Automated Boot Sequence (Windows)
The project includes Developer Experience (DX) scripts to automatically orchestrate the Docker database and FastAPI server.

To boot the entire environment:
```bash
.\start.bat
```
*Access the interactive Swagger UI at: `http://localhost:8000/docs`*

To safely spin down the infrastructure when finished:
```bash
.\stop.bat
```

---

## 📄 Citation

If you reference this aggregator pattern in your research or architecture, please cite it as follows:

**Harvard Style:**
> Hegde, S.S. (2026). B2B Fleet Aggregator API: Tactical Execution Engine (Version 1.0.0) [Software]. Available at: https://github.com/sandesh-s-hegde/b2b-fleet-aggregator-api

**BibTeX:**
```bibtex
@software{Hegde_B2B_Fleet_API_2026,
  author = {Hegde, Sandesh Subramanya},
  month = apr,
  title = {B2B Fleet Aggregator API: Tactical Execution Engine},
  url = {[https://github.com/sandesh-s-hegde/b2b-fleet-aggregator-api](https://github.com/sandesh-s-hegde/b2b-fleet-aggregator-api)},
  version = {1.0.0},
  year = {2026}
}
```

---

## 🗺️ Development Roadmap

*This repository has reached its planned maturity and serves as the finalized modern integration layer of the supply chain architecture.*

* [x] **Phase 1: API Core.** Bootstrapped FastAPI framework with OpenAPI 3.1 docs and health telemetry.
* [x] **Phase 2: Data Persistence.** Designed PostgreSQL schema and SQLAlchemy ORM for complex supplier relationships.
* [x] **Phase 3: Booking Engine.** Implemented stateful lifecycle management (Search -> Book -> Cancel) with inventory locking.
* [x] **Phase 4: Search Algorithm.** Engineered multi-criteria aggregation sorting by emission KPIs and pricing.
* [x] **Phase 5: Advanced Logic.** Shipped API Key auth, dynamic surge pricing, and financial revenue endpoints.
* [x] **Phase 6: DevOps & Governance.** Established Docker orchestration, CI/CD pipelines, Postman BDD test suites, and strict repository governance.
* [x] **Phase 7: Ecosystem Integration.** Successfully linked with upstream demand-side capacity models.

---

> ➡️ **Next Evolution:** While this API successfully handles modern, connected fleet suppliers, a massive segment of global logistics still relies on legacy portals. The ecosystem has now expanded into the **[RPA Legacy Freight Bridge](https://github.com/sandesh-s-hegde/rpa-freight-bridge)**. This hyperautomation microservice bridges the final gap, translating digital capacity requests into simulated UI keystrokes via UiPath Unattended Robots for non-API regional carriers.