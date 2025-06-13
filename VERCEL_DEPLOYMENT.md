# Vercel Deployment Guide for Smart Village Auth Service

## 🚀 Deploy to Vercel

### Prerequisites:
1. Vercel account (free tier available)
2. Vercel CLI installed
3. Git repository

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
# Navigate to project directory
cd /path/to/social_auth_service

# Deploy to Vercel
vercel
```

### Step 4: Configure Environment Variables
After deployment, add these environment variables in Vercel dashboard:

```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
SUPER_ADMIN_EMAIL=admin@smartvillage.com
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
LINE_CHANNEL_ID=your-line-channel-id
LINE_CHANNEL_SECRET=your-line-channel-secret
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
```

### Step 5: Update Google OAuth Settings
After getting Vercel URL, update Google Cloud Console:

1. Go to Google Cloud Console
2. Navigate to OAuth Client settings
3. Add new Authorized redirect URIs:
   ```
   https://your-vercel-app.vercel.app/api/auth/google/callback
   ```
4. Add new Authorized JavaScript origins:
   ```
   https://your-vercel-app.vercel.app
   ```

## 📁 Files Prepared for Vercel:

- ✅ `vercel.json` - Vercel configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `src/main.py` - Updated for Vercel compatibility
- ✅ `login.html` - Frontend login page

## 🔧 Vercel Configuration:

### Build Settings:
- **Framework Preset**: Other
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)
- **Install Command**: `pip install -r requirements.txt`

### Runtime:
- **Python Version**: 3.9
- **Node.js Version**: 18.x

## 🌐 Expected URLs:
- **API Base**: `https://your-app.vercel.app/api/`
- **Health Check**: `https://your-app.vercel.app/api/health`
- **Login Page**: `https://your-app.vercel.app/login.html`

## ⚠️ Important Notes:

1. **Database**: Uses SQLite in `/tmp` (ephemeral on Vercel)
2. **Environment Variables**: Must be set in Vercel dashboard
3. **CORS**: Configured to allow all origins (adjust for production)
4. **Cold Starts**: First request may be slower due to serverless nature

## 🔄 Deployment Process:

1. Push code to Git repository
2. Connect repository to Vercel
3. Configure environment variables
4. Deploy automatically on push
5. Update OAuth redirect URLs
6. Test all endpoints

Ready to deploy! 🚀

