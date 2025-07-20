#!/bin/bash

# Sahayak AI - Ollama Model Setup Script
# This script sets up the local AI models for offline mode

echo "🚀 Setting up Sahayak AI Offline Models..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "📦 Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    
    # Start Ollama service
    echo "🔧 Starting Ollama service..."
    ollama serve &
    sleep 5
else
    echo "✅ Ollama is already installed"
fi

# Pull required models
echo "⬇️ Downloading Gemma models for offline use..."

# Gemma 2B - Faster, good for basic tasks
echo "📥 Pulling Gemma 2B (quantized)..."
ollama pull gemma:2b

# Gemma 7B - Better quality, slower
echo "📥 Pulling Gemma 7B (quantized)..."
ollama pull gemma:7b

# Optional: Pull other useful models
# echo "📥 Pulling additional models..."
# ollama pull llama2:7b
# ollama pull codellama:7b

echo "🎉 Model setup complete!"

# Test the models
echo "🧪 Testing models..."

echo "Testing Gemma 2B:"
ollama run gemma:2b "Hello, I am a teacher. Can you help me create a simple math lesson?"

echo ""
echo "Testing Gemma 7B:"
ollama run gemma:7b "Create a brief science lesson plan for grade 3 students about plants."

echo ""
echo "✅ All models are ready for use!"
echo ""
echo "📋 Available models:"
ollama list

echo ""
echo "💡 Usage:"
echo "- Start Ollama: ollama serve"
echo "- Use Gemma 2B: ollama run gemma:2b"
echo "- Use Gemma 7B: ollama run gemma:7b"
echo "- API endpoint: http://localhost:11434"
