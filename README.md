# 🤖 B2B Fleet Aggregator API

**Author:** Sandesh Hegde

**Architecture:** Headless FastAPI Microservice (B2B Aggregator)

**Status:** 🚧 Active Development

## 🎯 The Purpose: What is this?

The **B2B Fleet Aggregator API** is a high-performance middleware designed to bridge the gap between demand-side strategic planning and supply-side physical assets.

While the [LSP Digital Capacity Twin](https://github.com/sandesh-s-hegde/digital_capacity_optimizer) serves as the **Macro-Strategic Layer** (forecasting shortfalls and volume surges), this API acts as the **Tactical Execution Engine**. It aggregates commercial vehicle availability from multiple third-party suppliers (e.g., Enterprise, Ryder, Hertz) into a unified, searchable interface for seamless capacity fulfillment.

## 🧠 The Motivation: Why are we doing this?

In the travel and logistics tech sectors, the "Integration Gap" is a multi-million dollar problem. A strategic model might identify a need for 50 additional vans in Dublin, but the execution fails if:

1. **Fragmentation:** Suppliers use different API standards, making real-time comparison impossible.
2. **Static Data:** Availability is often outdated, leading to failed bookings and lost revenue.
3. **Environment Impact:** Legacy systems fail to prioritize low-emission or EV options during the search phase.

**This API solves the "Macro-Micro Gap."** By providing a standardized, stateful microservice that tracks supplier inventory, rates, and carbon telemetry, we transform theoretical capacity needs into real-world, executable bookings.

## 🔮 Planned Outcomes: Where is this going?

The ultimate goal is a **Bidirectional, Closed-Loop Ecosystem**:

1. **Standardized Aggregation:** Creating a single source of truth for commercial fleet inventory across multiple global suppliers.
2. **Algorithmic Selection:** Utilizing weighted optimization (Price vs. CO2 vs. Reliability) to present the most valuable fleet options to the partner.
3. **Real-Time Telemetry:** Once a booking is completed, the API feeds actual cost and performance data back to the Digital Twin to refine future forecasting models.

---

## 🏗️ System Architecture

The project follows a "Clean Architecture" pattern to ensure high scalability and ease of integration:

* `main.py`: RESTful Routing, Exception Handling, and Interactive Swagger (OpenAPI) documentation.
* `database.py`: PostgreSQL engine management with SQLAlchemy Session Pooling.
* `models.py`: Relational schema definitions for Vehicles, Suppliers, and Bookings.
* `schemas.py`: Pydantic v2 data contracts for strict request/response validation.

### 📍 Current Endpoints

* `GET /` - System Health & Versioning.
* `GET /api/v1/vehicles` - Live Supplier Catalog retrieval.
* `POST /api/v1/fleet/search` - The core search engine for aggregating available fleet capacity.

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

Create a `.env` file in the root directory:

```env
DATABASE_URL="postgresql://postgres:password@localhost:5432/fleet_db"

```

### 4. Boot the Server

```bash
uvicorn main:app --reload

```

---

## 🗺️ Development Roadmap

* [x] **Phase 1: Aggregator Core & API Architecture.** Bootstrapping the FastAPI headless framework with automated OpenAPI 3.1 documentation and system health checks.
* [x] **Phase 2: Relational Data Persistence.** Designing the PostgreSQL schema using SQLAlchemy ORM to manage complex "Vehicle-to-Supplier" relationships.
* [ ] **Phase 3: Partner Ingestion & Webhooks.** Implementing `POST` endpoints for dynamic inventory updates and supplier onboarding via Postman/automated telemetry.
* [ ] **Phase 4: Multi-Criteria Search Algorithm.** Building the core aggregation logic to sort results based on partner-specific KPIs (Lowest Price, Greenest Fleet, or Highest Availability).
* [ ] **Phase 5: Digital Twin Synchronization.** Developing the closed-loop bridge to automatically trigger fleet searches based on "Capacity Shortfall" signals from the Digital Twin frontend.