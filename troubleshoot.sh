#!/bin/bash

echo "🔧 AI Sahayak Troubleshooting Script"
echo "===================================="

echo "📍 Current directory: $(pwd)"
echo "🌐 Checking network connectivity..."
curl -s http://httpbin.org/ip > /dev/null && echo "✅ Internet works" || echo "❌ Internet issue"

echo "🔍 Checking local servers..."
echo "Backend (port 8000):"
curl -s http://localhost:8000/health > /dev/null && echo "✅ Backend responding" || echo "❌ Backend not responding"

echo "Frontend server (port 8080):"
curl -s http://localhost:8080/ > /dev/null && echo "✅ Frontend server responding" || echo "❌ Frontend server not responding"

echo "📂 Checking files..."
ls -la /Users/rama.nayudu/sahayak-ai/frontend/test.html && echo "✅ Test HTML exists" || echo "❌ Test HTML missing"

echo "🔧 System info:"
echo "OS: $(uname -s)"
echo "Python: $(python3 --version)"
echo "Node: $(node --version)"

echo "💡 Suggested URLs to try:"
echo "- Backend: http://localhost:8000/test"
echo "- Simple HTML: http://localhost:8080/test.html"
echo "- Backend API: http://localhost:8000/docs"
