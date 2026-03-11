#!/bin/bash
# Kill old servers
kill -9 $(lsof -t -i:8000 -i:8001) 2>/dev/null || true
ps aux | grep "uvicorn app.main:app" | grep -v grep | awk '{print $2}' | xargs -r kill -9

# Start backend
cd /mnt/d/Projetos/bankBot/backend
uv run uvicorn app.main:app --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!

# Start agent
cd /mnt/d/Projetos/bankBot/agent
uv run uvicorn app.main:app --port 8001 > agent.log 2>&1 &
AGENT_PID=$!

echo "Waiting for backend on port 8000..."
while ! curl -s http://localhost:8000/ > /dev/null; do sleep 1; done
echo "Backend ready."

echo "Waiting for agent on port 8001..."
while ! curl -s http://localhost:8001/ > /dev/null; do sleep 1; done
echo "Agent ready."

echo "Running PIX test..."
cd /mnt/d/Projetos/bankBot/agent
uv run python test_progressive_pix.py
TEST_EXIT=$?

kill -9 $BACKEND_PID $AGENT_PID 2>/dev/null || true
exit $TEST_EXIT
