#!/usr/bin/env bash
# Start the API and the web app together, and shut both down on Ctrl-C.
set -euo pipefail
cd "$(dirname "$0")"

API_PORT=${API_PORT:-8000}
WEB_PORT=${WEB_PORT:-5173}

command -v python3 >/dev/null || { echo "python3 not found"; exit 1; }
command -v npm     >/dev/null || { echo "npm not found";     exit 1; }
[ -d frontend/node_modules ] || { echo "-> installing frontend deps"; (cd frontend && npm install); }

cleanup() { echo; echo "shutting down…"; kill 0 2>/dev/null || true; }
trap cleanup EXIT INT TERM

echo "API  → http://127.0.0.1:$API_PORT"
(cd backend && python3 -m uvicorn app.main:app --reload --port "$API_PORT") &

sleep 2
echo "APP  → http://localhost:$WEB_PORT"
(cd frontend && npm run dev -- --port "$WEB_PORT") &

wait
