@echo off
echo ===================================================
echo  B2B Fleet Aggregator - Teardown Sequence
echo ===================================================

echo [1/1] Stopping and removing Docker containers...
docker compose down

echo Environment safely spun down.