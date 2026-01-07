# 🚀 Deployment Guide - Render

Complete guide to deploy the SPAM & PHISHING Detector to Render in 15 minutes.

---

## 📋 Prerequisites

- [x] GitHub account
- [x] Render account (sign up at https://render.com - **FREE**)
- [x] Repository pushed to GitHub

---

## 🎯 Deployment Architecture

```
┌────────────────────────────────────────┐
│         Render Platform                │
│                                        │
│  ┌──────────────────────────────┐     │
│  │  Backend API (Web Service)   │     │
│  │  Docker: FastAPI + ML Models │     │
│  │  URL: *-api.onrender.com     │     │
│  └──────────────────────────────┘     │
│                                        │
│  ┌──────────────────────────────┐     │
│  │  Frontend (Static Site)      │     │
│  │  React + Vite Build          │     │
│  │  URL: *.onrender.com         │     │
│  └──────────────────────────────┘     │
└────────────────────────────────────────┘
```

---

## 🚀 Step-by-Step Deployment

### **STEP 1: Create Render Account (2 minutes)**

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

---

### **STEP 2: Deploy Backend API (5 minutes)**

1. **In Render Dashboard:**
   - Click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Select: `ML-Spam-Phising-Detector`
   - Click **"Connect"**

3. **Configure Service:**
   ```
   Name:              spam-detector-api
   Region:            Oregon (US West) - or closest to you
   Branch:            main
   Root Directory:    src/backend
   Environment:       Docker
   Plan:              Free
   ```

4. **Advanced Settings (click to expand):**
   
   **Docker:**
   - Dockerfile Path: `Dockerfile`
   - Docker Context: `.`
   - Docker Command: (leave empty - uses CMD from Dockerfile)

   **Health Check:**
   - Health Check Path: `/health`

5. **Environment Variables (Add these):**
   ```
   API_HOST=0.0.0.0
   API_PORT=8000
   API_WORKERS=1
   ```
   
   > **Note:** We'll add `API_CORS_ORIGINS` after frontend is deployed

6. **Click "Create Web Service"**

7. **Wait for deployment (~5 minutes)**
   - Watch the logs in real-time
   - You'll see Docker build process
   - When done, you'll get a URL like: `https://spam-detector-api.onrender.com`

8. **Test the backend:**
   ```bash
   # Health check
   curl https://spam-detector-api.onrender.com/health
   # Should return: {"status":"healthy"}
   
   # API docs
   open https://spam-detector-api.onrender.com/docs
   ```

---

### **STEP 3: Deploy Frontend (5 minutes)**

1. **In Render Dashboard:**
   - Click **"New +"** → **"Static Site"**

2. **Connect Repository:**
   - Select: `ML-Spam-Phising-Detector` (same repo)
   - Click **"Connect"**

3. **Configure Site:**
   ```
   Name:              spam-detector-frontend
   Branch:            main
   Root Directory:    (leave empty)
   Build Command:     cd src/frontend && npm ci && npm run build
   Publish Directory: src/frontend/dist
   ```

4. **Environment Variables:**
   ```
   VITE_API_URL=https://spam-detector-api.onrender.com
   ```
   > **Replace with YOUR actual backend URL from Step 2**

5. **Auto-Deploy:**
   - Enable "Auto-Deploy" (on by default)

6. **Click "Create Static Site"**

7. **Wait for build (~2 minutes)**
   - Watch npm install and build logs
   - When done, you'll get a URL like: `https://spam-detector-frontend.onrender.com`

---

### **STEP 4: Update Backend CORS (2 minutes)**

Now that frontend is deployed, update backend to allow requests:

1. **Go to Backend Service** (spam-detector-api)

2. **Environment → Add Variable:**
   ```
   API_CORS_ORIGINS=https://spam-detector-frontend.onrender.com,https://spam-detector-frontend-XXXXX.onrender.com
   ```
   > **Use YOUR actual frontend URL**
   
   > **Tip:** Add both with and without random suffix if Render assigns one

3. **Click "Save Changes"**
   - Backend will auto-redeploy (~2 minutes)

---

### **STEP 5: Test Full Stack (1 minute)**

1. **Open frontend URL:**
   ```
   https://spam-detector-frontend.onrender.com
   ```

2. **Test with SPAM email:**
   ```
   URGENT! You won $1,000,000! Click here NOW to claim your prize!
   ```

3. **Verify response:**
   - Should show SPAM+PHISHING detection
   - Risk level: CRITICAL
   - Probabilities displayed in gauges

4. **Test with legitimate email:**
   ```
   Hi team, the meeting is rescheduled to 3PM tomorrow. Please review the documents. Best, John
   ```

5. **Verify response:**
   - Should show HAM (legitimate)
   - Risk level: LOW

---

## ✅ Success Criteria

You're live in production when:

- ✅ Backend health check returns 200: `curl https://YOUR-API.onrender.com/health`
- ✅ API docs accessible: `https://YOUR-API.onrender.com/docs`
- ✅ Frontend loads: `https://YOUR-FRONTEND.onrender.com`
- ✅ Email classification works end-to-end
- ✅ No CORS errors in browser console

---

## 🎨 Custom Domain (Optional)

### Add Custom Domain to Frontend:

1. **In Frontend Service → Settings:**
   - Scroll to "Custom Domains"
   - Click "Add Custom Domain"
   - Enter: `app.yourdomain.com`

2. **In your DNS provider (Namecheap, Cloudflare, etc.):**
   ```
   Type:  CNAME
   Name:  app
   Value: spam-detector-frontend.onrender.com
   TTL:   Automatic
   ```

3. **Wait for DNS propagation** (~5-30 minutes)

4. **Render auto-provisions SSL** (Let's Encrypt)

### Add Custom Domain to Backend:

Same process, but use: `api.yourdomain.com`

---

## 💰 Costs

### Free Tier Limits:
```
✅ Frontend: Unlimited (Static Site)
⚠️  Backend:  Spins down after 15 min inactivity
              First request after sleep: ~30-60s delay
              
Free tier includes:
- 750 hours/month (enough for hobby projects)
- Custom domains with free SSL
- Auto-deploy from GitHub
- Basic DDoS protection
```

### Upgrade Options:
```
Starter Plan: $7/month per service
- Backend stays always active (no sleep)
- Faster builds
- Priority support

Pro Plan: $25/month per service
- Horizontal scaling
- More resources
- Advanced metrics
```

---

## 🔧 Troubleshooting

### Backend fails to build:

**Error:** `Models not found`
```bash
# Ensure Git LFS is tracking models
git lfs track "*.joblib"
git add .gitattributes
git commit -m "Track models with Git LFS"
git push
```

**Error:** `uv: command not found`
```dockerfile
# Ensure Dockerfile has uv copy step (already in your Dockerfile)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
```

### Frontend build fails:

**Error:** `npm ERR! Missing script: "build"`
```bash
# Check package.json has build script
cd src/frontend
npm run build  # Test locally first
```

**Error:** `VITE_API_URL not set`
```bash
# Ensure environment variable is set in Render dashboard
VITE_API_URL=https://your-backend.onrender.com
```

### CORS errors in browser:

**Error:** `Access-Control-Allow-Origin`
```bash
# Update backend environment variable
API_CORS_ORIGINS=https://your-frontend.onrender.com

# Redeploy backend (auto-triggers on env change)
```

### Backend sleeps (Free tier):

**Symptom:** First request slow (30-60s)

**Solutions:**
1. Upgrade to Starter ($7/mo) - stays awake
2. Use external monitor (cron-job.org) to ping every 10 min
3. Accept the tradeoff for free hosting

---

## 🔄 Updating Your App

### Automatic Deploy (Recommended):

```bash
# Make changes locally
git add .
git commit -m "feat: new feature"
git push origin main

# Render auto-deploys both services
# Watch progress in Render dashboard
```

### Manual Deploy:

1. Go to service in Render dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

---

## 📊 Monitoring

### View Logs:

1. **Backend Logs:**
   - Service → Logs tab
   - Real-time streaming
   - Filter by error/warning

2. **Frontend Logs:**
   - Build logs only (static site)
   - Check browser console for runtime errors

### Metrics (Pro plan):

- Request rate
- Response time
- Error rate
- CPU/Memory usage

---

## 🎯 Next Steps

After successful deployment:

1. **Add monitoring:**
   - Setup https://uptimerobot.com (free)
   - Monitor both frontend and backend `/health`

2. **Setup analytics:**
   - Google Analytics
   - Plausible (privacy-friendly)

3. **Improve performance:**
   - Add Redis for model caching (Render add-on)
   - Upgrade to Starter if you need always-on

4. **Security:**
   - Add rate limiting (already in FastAPI)
   - Setup WAF (Cloudflare free tier)

---

## 📚 Resources

- **Render Docs:** https://render.com/docs
- **Render Status:** https://status.render.com
- **Community:** https://community.render.com
- **Support:** support@render.com

---

## ✨ You're Live!

Congrats! Your ML application is now in production. 🎉

**Share your app:**
```
🚀 Live Demo: https://your-frontend.onrender.com
📖 API Docs:  https://your-api.onrender.com/docs
```

---

**Built with ❤️ using FastAPI, React, and Render**
