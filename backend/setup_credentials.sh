#!/bin/bash

# Google Cloud Credentials Setup Script for AI Sahayak

echo "🔐 Setting up Google Cloud Credentials for Vertex AI..."

# Check if credentials directory exists
CREDS_DIR="$HOME/.config/gcloud"
PROJECT_CREDS_DIR="/Users/rama.nayudu/sahayak-ai/backend/credentials"

# Create credentials directory if it doesn't exist
mkdir -p "$PROJECT_CREDS_DIR"

echo "📋 Choose your setup method:"
echo "1. Use existing service account key file"
echo "2. Set up Application Default Credentials (ADC)"
echo "3. Use environment variable"

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "📁 Place your service account JSON file in: $PROJECT_CREDS_DIR/"
        echo "📝 Then update your .env file with the path"
        echo ""
        echo "Example .env entry:"
        echo "GOOGLE_APPLICATION_CREDENTIALS=$PROJECT_CREDS_DIR/service-account-key.json"
        ;;
    2)
        echo "🔧 Setting up Application Default Credentials..."
        echo "Run: gcloud auth application-default login"
        echo "This will authenticate your local development environment"
        ;;
    3)
        echo "📝 Add to your .env file:"
        echo "FIREBASE_SERVICE_ACCOUNT_KEY='{\"type\":\"service_account\",\"project_id\":\"your-project\",...}'"
        echo "Replace with your complete service account JSON as a string"
        ;;
esac

echo ""
echo "✅ After setup, restart your FastAPI server to use the new credentials"
