$ErrorActionPreference = "Stop"
python -m pip install -e ".[dev]"
python -m pytest -q
docker compose up -d --build
Write-Host "ForgePulse release endpoint: http://localhost:8080/release"
