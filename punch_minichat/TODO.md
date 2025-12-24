- [x] Update requirements.txt to add Daphne and channels_redis
- [x] Update Procfile to use Daphne for ASGI
- [x] Update Dockerfile to use Daphne
- [x] Update settings.py for production: CHANNEL_LAYERS with Redis, DATABASES with environment variables
- [x] Build Docker image
- [x] Instruct user to deploy on Railway.app

## Railway Deployment Steps:
1. Push code to Git repository (GitHub/GitLab)
2. Create new project on Railway.app
3. Connect Git repository
4. Railway auto-detects Dockerfile and deploys
5. Set environment variables:
   - SECRET_KEY: Generate secure random string
   - DEBUG: False
   - ALLOWED_HOSTS: Your Railway domain
   - (Railway provides DATABASE_URL and REDIS_URL automatically)
