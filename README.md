# 🤖 LSP Workforce & Dispatch API

**Author:** Sandesh Hegde  
**Architecture:** Headless FastAPI Microservice  
**Status:** 🚧 Active Development

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=for-the-badge)

## 🎯 The Purpose: What is this?


The **LSP Workforce & Dispatch API** is the micro-tactical execution engine of the Logistics Service Provider (LSP) ecosystem. 

While the [LSP Digital Capacity Twin](https://github.com/sandesh-s-hegde/digital_capacity_optimizer) handles the **Macro-Strategic layer** (e.g., forecasting global container volumes, routing through international borders, calculating carbon emissions), this FastAPI microservice handles the **Micro-Tactical layer** (e.g., executing the actual work on the warehouse floor). It ingests daily pallet volume forecasts and dynamically allocates warehouse tasks between **Human Workers** and **Automated Guided Vehicles (AGVs)**.

## 🧠 The Motivation: Why are we doing this?
In modern logistics research, there is a massive disconnect between strategic planning and physical execution. A macro-level Digital Twin might calculate that a warehouse needs to process 5,000 pallets today to minimize stockout risk. However, the theoretical model fails in reality if:
1. The human workforce reaches maximum fatigue levels.
2. The automated AGV fleet runs out of battery and is stuck at charging stations.
3. The shift scheduling is mathematically inefficient.

**We are building this API to bridge the "Macro-Micro Gap."** By creating a dedicated, stateful microservice that tracks physical constraints (fatigue scores, battery degradation, shift availability), we transform abstract supply chain strategy into mathematically optimized, real-world task execution.

## 🔮 Planned Outcomes: Where is this going?
The ultimate goal of this research artifact is a **Bidirectional Closed-Loop System**:
1. **Automated Ingestion:** The API will expose `POST` webhooks to automatically catch daily volume targets sent directly from the Macro Digital Twin.
2. **Algorithmic Dispatching:** It will utilize an optimization algorithm (e.g., Knapsack or Linear Programming) to assign the incoming pallets. It will route heavy, repetitive tasks to AGVs (until batteries hit 20%) and complex, dexterous tasks to Humans (monitoring fatigue accumulation).
3. **Telemetry Feedback:** Once the shift is simulated, this API will send the *actual* execution cost and time back up to the Macro Twin, allowing the overarching stochastic models to correct themselves based on ground-floor realities.

---

## 🏗️ System Architecture


The project follows a strict "Separation of Concerns" microservice architecture:
* `main.py`: FastAPI application routing and interactive Swagger UI.
* `database.py`: PostgreSQL engine and session management.
* `models.py`: SQLAlchemy ORM entities (The Database Layer).
* `schemas.py`: Pydantic v2 payload validation (The Ingestion Layer).

### 📍 Current Endpoints
* `GET /` - System health check.
* `GET /api/v1/workforce/roster` - Fetches the live availability of Human Workers and the AGV Fleet.

---

## 🚀 Local Installation & Setup

### 1. Clone & Environment
```bash
git clone https://github.com/sandesh-s-hegde/lsp-workforce-api.git
cd lsp-workforce-api
python -m venv venv

# Activate (Windows):
venv\Scripts\activate
# Activate (Mac/Linux):
source venv/bin/activate

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Environment Variables

Create a `.env` file in the root directory to connect your database:

```env
DATABASE_URL="postgresql://postgres:password@localhost:5432/workforce_db"

```

### 4. Boot the Server

```bash
uvicorn main:app --reload

```

*Access the auto-generated interactive Swagger UI documentation at: `http://127.0.0.1:8000/docs*`

---

## 🗺️ Development Roadmap

* [x] **Phase 1: API Bootstrap & Core Routing.** Initializing the headless FastAPI architecture, enterprise Swagger UI metadata injection, and health check endpoints.
* [x] **Phase 2: Stateful Database Architecture.** Dockerized PostgreSQL integration, SQLAlchemy ORM entity mapping (Workers/AGVs), and schema initialization.
* [ ] **Phase 3: Data Ingestion & Entity Webhooks.** Building `POST` endpoints with strict Pydantic v2 payload validation to dynamically register human workers and autonomous fleet units via API testing tools (Postman).
* [ ] **Phase 4: Algorithmic Task Dispatching.** Implementing the core optimization logic (e.g., Linear Programming) to route heavy tasks to AGVs (tracking battery decay) and complex tasks to humans (tracking physical fatigue accumulation).
* [ ] **Phase 5: Digital Twin Telemetry Integration.** Closing the "Macro-Micro Gap" by feeding real-world shift execution costs and time delays back into the overarching stochastic Capacity Twin.