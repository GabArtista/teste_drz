#!/bin/bash
set -e

BASE="$(cd "$(dirname "$0")" && pwd)"

echo "=== DRZ Chat — Iniciando serviços ==="

# Ollama
if ! curl -s http://localhost:11434 > /dev/null 2>&1; then
  echo "[1/3] Iniciando Ollama..."
  ollama serve > /tmp/ollama.log 2>&1 &
  sleep 3
fi

# Verifica modelo
MODEL="qwen2.5:1.5b"
if ! ollama list | grep -q "$MODEL"; then
  echo "[1/3] Baixando modelo $MODEL (pode demorar ~1min)..."
  ollama pull "$MODEL"
fi
echo "[1/3] Ollama OK — modelo $MODEL pronto"

# Backend
echo "[2/3] Iniciando backend (porta 8000)..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
cd "$BASE/backend"
nohup .venv/bin/python3 -m uvicorn main:app --port 8000 > /tmp/backend.log 2>&1 &
sleep 4
curl -sf http://localhost:8000/health > /dev/null && echo "[2/3] Backend OK"

# Frontend
echo "[3/3] Iniciando frontend (porta 5173)..."
lsof -ti:5173 | xargs kill -9 2>/dev/null || true
cd "$BASE/frontend"
nohup npx vite --port 5173 > /tmp/frontend.log 2>&1 &
sleep 4
curl -sf http://localhost:5173 > /dev/null && echo "[3/3] Frontend OK"

echo ""
echo "=================================="
echo "  Tudo pronto!"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo "=================================="
