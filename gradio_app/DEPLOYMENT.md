# 🚀 Deployment Guide

This guide covers multiple deployment options for the 3D Anime Chatbot.

## 📦 Hugging Face Spaces (Recommended)

### Prerequisites
- Hugging Face account
- Git installed locally

### Steps

1. **Create a new Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose a name (e.g., `3d-anime-chatbot`)
   - Select SDK: **Gradio**
   - Choose visibility (Public/Private)

2. **Clone your Space**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/3d-anime-chatbot
   cd 3d-anime-chatbot
   ```

3. **Copy files**
   ```bash
   cp /path/to/gradio_app/* .
   ```

4. **Push to Hugging Face**
   ```bash
   git add .
   git commit -m "Initial commit: 3D Anime Chatbot"
   git push
   ```

5. **Wait for build**
   - Your Space will automatically build and deploy
   - Visit your Space URL to see it live!

### Configuration

The `README.md` file contains metadata for Hugging Face:

```yaml
---
title: 3D Anime Chatbot
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---
```

---

## 🐳 Docker Deployment

### Local Docker

1. **Build the image**
   ```bash
   docker build -t 3d-anime-chatbot .
   ```

2. **Run the container**
   ```bash
   docker run -p 7860:7860 3d-anime-chatbot
   ```

3. **Access the app**
   - Open http://localhost:7860

### Docker Compose

1. **Start the service**
   ```bash
   docker-compose up -d
   ```

2. **View logs**
   ```bash
   docker-compose logs -f
   ```

3. **Stop the service**
   ```bash
   docker-compose down
   ```

---

## ☁️ Cloud Platforms

### AWS

#### Using EC2

1. Launch an EC2 instance (t2.medium or larger)
2. Install Docker:
   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo service docker start
   ```
3. Clone and run:
   ```bash
   git clone https://github.com/ruslanmv/gpt-anime.git
   cd gpt-anime/gradio_app
   docker-compose up -d
   ```

#### Using ECS (Elastic Container Service)

1. Push image to ECR
2. Create ECS cluster
3. Define task with our image
4. Create service with Application Load Balancer

### Google Cloud Platform

#### Using Cloud Run

1. **Build and push image**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/3d-anime-chatbot
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy 3d-anime-chatbot \
     --image gcr.io/PROJECT_ID/3d-anime-chatbot \
     --platform managed \
     --port 7860 \
     --allow-unauthenticated
   ```

### Azure

#### Using Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name 3d-anime-chatbot \
  --image YOUR_DOCKER_IMAGE \
  --dns-name-label 3d-anime-chatbot \
  --ports 7860
```

---

## 🖥️ VPS Deployment

### General Steps

1. **SSH into your VPS**
   ```bash
   ssh user@your-server-ip
   ```

2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git -y
   ```

3. **Clone repository**
   ```bash
   git clone https://github.com/ruslanmv/gpt-anime.git
   cd gpt-anime/gradio_app
   ```

4. **Install requirements**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run with systemd (for production)**

Create `/etc/systemd/system/chatbot.service`:

```ini
[Unit]
Description=3D Anime Chatbot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/gradio_app
ExecStart=/usr/bin/python3 /path/to/gradio_app/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable chatbot
sudo systemctl start chatbot
```

6. **Setup reverse proxy (Nginx)**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## 🔒 Security Considerations

### For Production Deployments

1. **HTTPS/SSL**
   - Use Let's Encrypt for free SSL certificates
   - Configure Nginx/Apache with SSL

2. **Environment Variables**
   - Never commit API keys
   - Use `.env` files (add to `.gitignore`)
   - Use platform secret managers

3. **Rate Limiting**
   - Implement rate limiting to prevent abuse
   - Use Gradio's built-in queue system

4. **Authentication**
   - Add authentication if needed:
   ```python
   demo.launch(auth=("username", "password"))
   ```

---

## 📊 Monitoring

### Recommended Tools

- **Gradio Analytics**: Built-in usage analytics
- **Prometheus + Grafana**: For detailed metrics
- **Sentry**: For error tracking
- **Uptime Robot**: For uptime monitoring

### Example Prometheus Setup

Add to `app.py`:
```python
from prometheus_client import start_http_server, Counter

# Start metrics server
start_http_server(8000)

# Track requests
request_counter = Counter('chatbot_requests', 'Total requests')
```

---

## 🔄 CI/CD

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Hugging Face

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Push to Hugging Face
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          git remote add hf https://huggingface.co/spaces/USERNAME/SPACE
          git push hf main
```

---

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in app.py
   demo.launch(server_port=7861)
   ```

2. **Memory issues**
   - Increase Docker memory limit
   - Use a larger instance type

3. **Slow loading**
   - Enable caching
   - Use CDN for static assets
   - Optimize 3D model size

---

## 📞 Support

If you encounter issues:
- Check [GitHub Issues](https://github.com/ruslanmv/gpt-anime/issues)
- Join our [Discord community](#)
- Email: support@gpt-anime.com

---

**Happy Deploying! 🚀**
