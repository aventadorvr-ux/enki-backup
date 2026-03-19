#!/data/data/com.termux/files/usr/bin/bash
# Nemo EC2 Agent Restore Script
# Restarts all agents on the NZ Real Estate AI EC2 instance

EC2_IP="3.25.170.226"
SSH_KEY="$HOME/.ssh/id_rsa_nemoclaw"

echo "🔄 Reloading Nemo EC2 Agents..."
echo "================================"
echo ""

# Check SSH connectivity
echo "📡 Checking EC2 connectivity..."
if ! ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i "$SSH_KEY" "ubuntu@$EC2_IP" "echo 'Connected'" 2>/dev/null; then
    echo "❌ Cannot connect to EC2 instance"
    exit 1
fi
echo "✅ EC2 instance reachable"
echo ""

# Check API health
echo "🔍 Checking API health..."
HEALTH=$(ssh -i "$SSH_KEY" "ubuntu@$EC2_IP" "curl -s http://localhost:8000/health" 2>/dev/null)
if echo "$HEALTH" | grep -q '"status":"healthy"'; then
    echo "✅ Backend API: Healthy"
else
    echo "⚠️ Backend API: Not responding, restarting..."
    ssh -i "$SSH_KEY" "ubuntu@$EC2_IP" "cd ~/nz-realestate-ai && pkill -f uvicorn; sleep 2; nohup ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &"
    sleep 3
fi

# Check frontend
echo "🔍 Checking frontend..."
FRONTEND=$(ssh -i "$SSH_KEY" "ubuntu@$EC2_IP" "curl -s -o /dev/null -w '%{http_code}' http://localhost:3000" 2>/dev/null)
if [ "$FRONTEND" = "200" ]; then
    echo "✅ Frontend: Running (HTTP 200)"
else
    echo "⚠️ Frontend: Not responding, restarting..."
    ssh -i "$SSH_KEY" "ubuntu@$EC2_IP" "pkill -f 'http.server 3000'; sleep 2; cd ~/nz-realestate-ai/frontend && nohup python3 -m http.server 3000 > frontend.log 2>&1 &"
    sleep 2
fi

echo ""
echo "📊 Agent Status Summary"
echo "======================="

# Get agent status from API
AGENTS=$(ssh -i "$SSH_KEY" "ubuntu@$EC2_IP" "curl -s http://localhost:8000/api/v1/agents" 2>/dev/null)
echo "Agents: $AGENTS"

echo ""
echo "🌐 Endpoints"
echo "============"
echo "Backend API:  http://$EC2_IP:8000"
echo "Health Check: http://$EC2_IP:8000/health"
echo "API Docs:     http://$EC2_IP:8000/docs"
echo "Dashboard:    http://$EC2_IP:3000"
echo ""
echo "✅ All agents reloaded and operational!"
