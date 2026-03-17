# 🤖 B2B Fleet Aggregator API

**Author:** Sandesh Hegde

**Architecture:** Headless FastAPI Microservice (B2B Aggregator)

**Status:** 🟢 Live in Production / Active Development

**Live API Documentation:** [Interactive Swagger UI](https://b2b-fleet-api.onrender.com/docs) *(Note: Hosted on Render Free Tier. Please allow 30s for cold start.)*

## 🎯 The Purpose: What is this?

The **B2B Fleet Aggregator API** is a high-performance middleware designed to bridge the gap between demand-side strategic planning and supply-side physical assets.

While the [LSP Digital Capacity Twin](https://github.com/sandesh-s-hegde/digital_capacity_optimizer) serves as the **Macro-Strategic Layer** (forecasting shortfalls and volume surges), this API acts as the **Tactical Execution Engine**. It aggregates commercial vehicle availability from multiple third-party suppliers (e.g., Enterprise, Ryder, Hertz) into a unified, searchable interface for seamless capacity fulfillment.

## 🧠 The Motivation: Why are we doing this?

In the travel and logistics tech sectors, the "Integration Gap" is a multi-million dollar problem. A strategic model might identify a need for additional vans in Europe, but the execution fails if:

1. **Fragmentation:** Suppliers use different API standards, making real-time comparison impossible.
2. **Static Data:** Availability is often outdated, leading to failed bookings and lost revenue.
3. **Environment Impact:** Legacy systems fail to prioritize low-emission or EV options during the search phase.

**This API solves the "Macro-Micro Gap."** By providing a standardized, stateful microservice that tracks supplier inventory, calculates dynamic surge pricing, sorts by carbon telemetry, and manages the complete booking lifecycle, we transform theoretical capacity needs into real-world, executable bookings.

## 🔮 Planned Outcomes: Where is this going?

The ultimate goal is a **Bidirectional, Closed-Loop Ecosystem**:

1. **Standardized Aggregation:** Creating a single source of truth for commercial fleet inventory across multiple global suppliers.
2. **Algorithmic Selection:** Utilizing weighted optimization (Price vs. CO2 emissions) to present the most valuable fleet options to the partner.
3. **Real-Time Telemetry:** Once a booking is completed, the API feeds actual cost, utilization rates, and performance data back to the Digital Twin to refine future forecasting models.

---

## 🏗️ System Architecture

The project follows a "Clean Architecture" pattern to ensure high scalability and ease of integration:

* `main.py`: RESTful Routing, Exception Handling, Business Logic, and OpenAPI documentation.
* `database.py`: PostgreSQL engine management with SQLAlchemy Session Pooling.
* `models.py`: Relational schema definitions for Vehicles, Suppliers, and Bookings.
* `schemas.py`: Pydantic v2 data contracts for strict request/response validation.
* `docker-compose.yml`: Infrastructure-as-Code (IaC) for rapid local database orchestration.
* `postman_collection.json`: Automated Behavior-Driven Development (BDD) test suite.
* `start.bat` / `stop.bat`: Windows automation scripts for one-click environment orchestration.

### 📍 Core Endpoints

**System & Analytics**
* `GET /api/v1/health` - Deep system health check (API + Database Ping). *Used for automated Uptime telemetry.*
* `GET /api/v1/fleet/utilization` - Real-time fleet utilization metrics.
* `GET /api/v1/fleet/revenue` - Aggregates financial telemetry from confirmed B2B bookings.

**Fleet Management & Aggregation**
* `GET /api/v1/vehicles` - Live Supplier Catalog retrieval.
* `POST /api/v1/vehicles` - Register new supplier inventory.
* `POST /api/v1/vehicles/batch` - Ingest bulk payloads for high-volume supplier syncs.
* `DELETE /api/v1/vehicles/{vehicle_id}` - Safely retire inventory (validates active bookings).
* `POST /api/v1/fleet/search` - Multi-criteria search engine (Filters availability, sorts by lowest CO2 emissions and daily rate).

**Stateful Booking Engine** *(Secured via API Key)*
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

## 🗺️ Development Roadmap

* [x] **Phase 1: API Core.** Bootstrapped FastAPI framework with OpenAPI 3.1 docs and health telemetry.
* [x] **Phase 2: Data Persistence.** Designed PostgreSQL schema and SQLAlchemy ORM for complex supplier relationships.
* [x] **Phase 3: Booking Engine.** Implemented stateful lifecycle management (Search -> Book -> Cancel) with inventory locking.
* [x] **Phase 4: Search Algorithm.** Engineered multi-criteria aggregation sorting by emission KPIs and pricing.
* [x] **Phase 5: Advanced Logic.** Shipped API Key auth, dynamic surge pricing, and financial revenue endpoints.
* [x] **Phase 6: DX & QA.** Integrated Docker orchestration, local `.bat` automation, and a stateful Postman BDD test suite.
* [ ] **Phase 7: Digital Twin Integration.** Building the closed-loop bridge to trigger automatic fleet searches based on predictive capacity shortfalls.