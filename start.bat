@echo off
echo ===================================================
echo  B2B Fleet Aggregator - Local Development Server
echo ===================================================

echo [1/2] Starting PostgreSQL Database Container...
docker compose up -d

echo [WAIT] Allowing database connections to open...
timeout /t 3 /nobreak > NUL

echo [2/2] Booting FastAPI Application...
uvicorn main:app --reload