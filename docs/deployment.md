# Deployment Guide - Project Sahayak

## Overview

This guide covers deployment options for both online (Vertex AI) and offline (Ollama) modes of Sahayak AI.

## Prerequisites

- Google Cloud Account with billing enabled
- Firebase project setup
- Domain name (optional, for custom hosting)
- Server or cloud instance for backend

## Frontend Deployment

### Firebase Hosting (Recommended)

1. **Build the application**
   ```bash
   cd frontend
   npm run build
   ```

2. **Install Firebase CLI**
   ```bash
   npm install -g firebase-tools
   firebase login
   ```

3. **Initialize Firebase hosting**
   ```bash
   firebase init hosting
   # Select your Firebase project
   # Set public directory to 'dist'
   # Configure as SPA (Single Page App)
   ```

4. **Deploy**
   ```bash
   firebase deploy --only hosting
   ```

### Alternative: Netlify/Vercel

1. **Connect repository** to Netlify or Vercel
2. **Set build command**: `npm run build`
3. **Set publish directory**: `dist`
4. **Configure environment variables**

## Backend Deployment

### Google Cloud Run (Recommended for online mode)

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
   ```

2. **Deploy to Cloud Run**
   ```bash
   cd backend
   gcloud run deploy sahayak-backend \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars="GOOGLE_CLOUD_PROJECT=your-project-id"
   ```

### Docker Deployment

1. **Build and run**
   ```bash
   cd backend
   docker build -t sahayak-backend .
   docker run -p 8000:8000 \
     -e GOOGLE_CLOUD_PROJECT=your-project \
     sahayak-backend
   ```

### VPS/Dedicated Server

1. **Setup environment**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   
   # Install Python dependencies
   cd backend
   pip3 install -r requirements.txt
   ```

2. **Setup systemd service**
   ```bash
   sudo nano /etc/systemd/system/sahayak.service
   ```
   
   ```ini
   [Unit]
   Description=Sahayak AI Backend
   After=network.target
   
   [Service]
   User=www-data
   WorkingDirectory=/path/to/sahayak-ai/backend
   Environment="PATH=/path/to/venv/bin"
   ExecStart=/path/to/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **Setup Nginx reverse proxy**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location /api/ {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Offline Mode Deployment

### Local School Server Setup

1. **Hardware Requirements**
   - Minimum: 4GB RAM, 50GB storage
   - Recommended: 8GB RAM, 100GB storage
   - Raspberry Pi 4 (8GB) or mini PC

2. **Install Ollama**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull models
   ollama pull gemma:2b
   ollama pull gemma:7b
   ```

3. **Setup local network**
   - Configure WiFi hotspot
   - Set static IP address
   - Enable local DNS resolution

4. **Deploy backend locally**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Set environment for offline mode
   export OLLAMA_BASE_URL=http://localhost:11434
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Database Setup

### Firebase Firestore (Online Mode)

1. **Enable Firestore** in Firebase Console
2. **Set up security rules**
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /lesson_plans/{document} {
         allow read, write: if request.auth != null;
       }
       match /user_preferences/{userId} {
         allow read, write: if request.auth != null && request.auth.uid == userId;
       }
     }
   }
   ```

### SQLite (Offline Mode)

1. **Initialize database**
   ```bash
   cd backend
   python -c "
   import sqlite3
   conn = sqlite3.connect('sahayak_offline.db')
   # Create tables as needed
   conn.close()
   "
   ```

## Environment Configuration

### Production Environment Variables

```bash
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Firebase
FIREBASE_SERVICE_ACCOUNT_KEY={"type": "service_account"...}

# API
PORT=8080
DEBUG=false
CORS_ORIGINS=https://your-domain.com

# Ollama (for offline deployment)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=gemma:7b
```

## SSL/HTTPS Setup

### Using Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Using Cloudflare (Free)

1. Point domain to Cloudflare
2. Enable SSL/TLS encryption
3. Set up page rules for caching

## Monitoring and Logging

### Google Cloud Monitoring

1. **Enable Cloud Logging** in GCP Console
2. **Set up alerts** for errors and performance
3. **Configure dashboards** for key metrics

### Self-hosted Monitoring

```bash
# Install monitoring tools
docker run -d --name=grafana -p 3000:3000 grafana/grafana
docker run -d --name=prometheus -p 9090:9090 prom/prometheus
```

## Backup Strategy

### Firebase Backup

```bash
# Export Firestore data
gcloud firestore export gs://your-backup-bucket
```

### Local Backup

```bash
# Backup SQLite database
cp sahayak_offline.db backups/sahayak_$(date +%Y%m%d).db

# Backup user data
tar -czf backups/user_data_$(date +%Y%m%d).tar.gz user_data/
```

## Scaling Considerations

### Horizontal Scaling

1. **Load balancer** setup with multiple backend instances
2. **Database replication** for read operations
3. **CDN** for static content delivery

### Performance Optimization

1. **Caching** with Redis for frequent requests
2. **Database indexing** for query optimization
3. **Compression** for API responses
4. **Image optimization** for visual content

## Troubleshooting

### Common Issues

1. **Firebase connection errors**
   - Check service account permissions
   - Verify environment variables
   - Confirm Firestore rules

2. **Ollama model loading**
   - Ensure sufficient RAM
   - Check model availability
   - Verify Ollama service status

3. **CORS errors**
   - Update CORS_ORIGINS in backend
   - Check frontend API endpoint URLs
   - Verify HTTPS configuration

### Health Checks

```bash
# Backend health
curl https://your-api-domain.com/api/health

# Ollama health
curl http://localhost:11434/api/tags

# Frontend accessibility
curl https://your-frontend-domain.com
```

## Security Checklist

- [ ] HTTPS enabled everywhere
- [ ] Environment variables secured
- [ ] Firebase security rules configured
- [ ] API rate limiting implemented
- [ ] User authentication working
- [ ] Data encryption at rest
- [ ] Regular security updates
- [ ] Backup and recovery tested
