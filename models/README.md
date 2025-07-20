# Sahayak AI Models

Local AI models setup for offline mode using Ollama.

## Overview

This directory contains scripts and configurations for setting up quantized Gemma models for offline inference using Ollama.

## Models

### Gemma 2B (Quantized)
- **Size**: ~1.7GB
- **Speed**: Fast inference
- **Use case**: Quick responses, basic lesson planning
- **Memory**: ~4GB RAM required

### Gemma 7B (Quantized)
- **Size**: ~4.8GB  
- **Speed**: Moderate inference
- **Use case**: Detailed lesson plans, complex content generation
- **Memory**: ~8GB RAM required

## Setup

1. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Manual installation**
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama service
   ollama serve
   
   # Pull models
   ollama pull gemma:2b
   ollama pull gemma:7b
   ```

## Usage

### Start Ollama Server
```bash
ollama serve
```
Server will be available at: http://localhost:11434

### Test Models
```bash
# Test Gemma 2B
ollama run gemma:2b "Create a simple math lesson for grade 2"

# Test Gemma 7B
ollama run gemma:7b "Generate a comprehensive science lesson plan"
```

### API Usage
```bash
# Generate text via API
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma:7b",
    "prompt": "Create a lesson plan for teaching fractions to grade 4 students",
    "stream": false
  }'
```

## Configuration

### Model Selection
- **Rural/Low-resource**: Use Gemma 2B for faster responses
- **Urban/High-resource**: Use Gemma 7B for better quality
- **Auto-switching**: Backend can switch based on system resources

### Performance Tuning
```bash
# Set Ollama environment variables
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=2
```

## Integration

The backend automatically connects to Ollama when running in offline mode:

```python
# Backend configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=gemma:7b
```

## Troubleshooting

### Common Issues

1. **Ollama not starting**
   ```bash
   # Check if port is in use
   lsof -i :11434
   
   # Kill existing process
   pkill ollama
   ollama serve
   ```

2. **Model not found**
   ```bash
   # List available models
   ollama list
   
   # Pull missing model
   ollama pull gemma:7b
   ```

3. **Memory issues**
   ```bash
   # Check system memory
   free -h
   
   # Use smaller model
   ollama pull gemma:2b
   ```

### Performance Monitoring
```bash
# Check model loading status
curl http://localhost:11434/api/ps

# Monitor system resources
htop
```

## Docker Setup (Optional)

```dockerfile
FROM ollama/ollama:latest

# Copy models (if pre-downloaded)
COPY models/ /root/.ollama/models/

# Expose port
EXPOSE 11434

# Start Ollama
CMD ["ollama", "serve"]
```

## Model Customization

### Fine-tuning (Advanced)
```bash
# Create Modelfile for custom fine-tuning
cat > Modelfile << EOF
FROM gemma:7b

# Custom system prompt for educational content
SYSTEM You are Sahayak, an AI assistant specialized in helping rural Indian teachers create educational content for multi-grade classrooms.

# Custom parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.8
PARAMETER top_k 40
EOF

# Build custom model
ollama create sahayak-edu -f Modelfile
```

## System Requirements

### Minimum
- RAM: 4GB (for Gemma 2B)
- Storage: 5GB free space
- CPU: 2+ cores

### Recommended
- RAM: 8GB+ (for Gemma 7B)
- Storage: 10GB+ free space
- CPU: 4+ cores
- GPU: Optional, for faster inference

## License

Models are subject to their respective licenses:
- Gemma: Google's Gemma License
