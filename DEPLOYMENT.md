# Deployment Guide - Atlas Maroc Capital Markets

This guide covers multiple deployment options for the Atlas Maroc Capital Markets static website.

## Quick Start (Local Development)

### Linux/macOS
```bash
chmod +x start.sh stop.sh
./start.sh
```

### Windows
```cmd
start.bat
```

The website will be available at `http://localhost:8000`

## Deployment Options

### 1. Netlify (Recommended for Quick Deploy)

#### Option A: Drag and Drop
1. Visit [netlify.com](https://netlify.com)
2. Drag the `website` folder to the deployment area
3. Your site is live!

#### Option B: GitHub Integration
1. Push code to GitHub
2. Connect repository to Netlify
3. Set build settings:
   - **Base directory**: `website`
   - **Publish directory**: `website`
4. Deploy

#### Option C: Netlify CLI
```bash
npm install -g netlify-cli
cd website
netlify deploy --prod
```

### 2. Vercel

#### Option A: Vercel CLI
```bash
npm install -g vercel
cd website
vercel --prod
```

#### Option B: GitHub Integration
1. Push code to GitHub
2. Import project on [vercel.com](https://vercel.com)
3. Set root directory to `website`
4. Deploy

### 3. GitHub Pages

#### Enable GitHub Pages
1. Push code to GitHub repository
2. Go to Settings → Pages
3. Source: GitHub Actions (recommended) or Branch: main, folder: `/website`
4. Your site will be at `https://yourusername.github.io/repo-name/`

#### Using GitHub Actions (included)
The `.github/workflows/deploy.yml` file is already configured.
Just push to main/master branch and it will auto-deploy.

### 4. AWS S3 + CloudFront

```bash
# Create S3 bucket
aws s3 mb s3://atlas-maroc-capital-markets --region us-east-1

# Configure for static website hosting
aws s3 website s3://atlas-maroc-capital-markets \
  --index-document index.html \
  --error-document index.html

# Upload files
cd website
aws s3 sync . s3://atlas-maroc-capital-markets --acl public-read

# Create CloudFront distribution (optional, for HTTPS and CDN)
aws cloudfront create-distribution \
  --origin-domain-name atlas-maroc-capital-markets.s3.amazonaws.com \
  --default-root-object index.html
```

### 5. Azure Static Web Apps

```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create resource group
az group create --name atlas-maroc-rg --location eastus

# Create static web app
az staticwebapp create \
  --name atlas-maroc-capital-markets \
  --resource-group atlas-maroc-rg \
  --source website \
  --location eastus \
  --branch main
```

### 6. Google Cloud Storage

```bash
# Create bucket
gsutil mb gs://atlas-maroc-capital-markets

# Configure for website hosting
gsutil web set -m index.html -e index.html gs://atlas-maroc-capital-markets

# Make bucket public
gsutil iam ch allUsers:objectViewer gs://atlas-maroc-capital-markets

# Upload files
cd website
gsutil -m rsync -r . gs://atlas-maroc-capital-markets

# Your site will be at:
# https://storage.googleapis.com/atlas-maroc-capital-markets/index.html
```

### 7. Cloudflare Pages

#### Option A: Dashboard
1. Log in to [dash.cloudflare.com](https://dash.cloudflare.com)
2. Go to Pages
3. Create a project
4. Connect GitHub repository
5. Set build configuration:
   - **Build command**: (leave empty)
   - **Build output directory**: `website`
6. Deploy

#### Option B: Wrangler CLI
```bash
npm install -g wrangler
cd website
wrangler pages publish . --project-name=atlas-maroc-capital-markets
```

### 8. Firebase Hosting

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
firebase init hosting
# Select: Public directory: website
# Configure as single-page app: No
# Set up automatic builds: No

# Deploy
firebase deploy --only hosting
```

### 9. DigitalOcean App Platform

1. Push code to GitHub
2. Go to [cloud.digitalocean.com/apps](https://cloud.digitalocean.com/apps)
3. Create App
4. Connect GitHub repository
5. Configure:
   - **Type**: Static Site
   - **Source Directory**: `/website`
6. Deploy

### 10. Traditional Web Hosting (cPanel, etc.)

1. Access your hosting control panel (cPanel, Plesk, etc.)
2. Navigate to File Manager
3. Go to `public_html` or `www` directory
4. Upload all files from the `website` folder
5. Ensure `index.html` is in the root

## Custom Domain Setup

After deploying to any platform, you can add a custom domain:

### DNS Configuration
Add these DNS records at your domain registrar:

For apex domain (example.com):
```
A     @      [Platform IP or ALIAS/CNAME target]
```

For www subdomain:
```
CNAME www    [Platform URL]
```

### Platform-Specific Instructions

**Netlify**: Settings → Domain management → Add custom domain
**Vercel**: Project Settings → Domains → Add domain
**GitHub Pages**: Repository Settings → Pages → Custom domain
**AWS/CloudFront**: Route 53 or your DNS provider
**Cloudflare**: Automatically configured if using Cloudflare DNS

## SSL/HTTPS

All modern platforms provide free SSL certificates automatically:
- **Netlify**: Automatic (Let's Encrypt)
- **Vercel**: Automatic (Let's Encrypt)
- **GitHub Pages**: Automatic (Let's Encrypt)
- **Cloudflare**: Automatic (Cloudflare SSL)
- **AWS CloudFront**: Free certificate via ACM
- **Azure**: Automatic (Let's Encrypt)

## Performance Optimization

The website is already optimized:
- ✅ No external dependencies
- ✅ Inline CSS (no extra HTTP requests)
- ✅ No JavaScript required
- ✅ Semantic HTML for fast parsing
- ✅ Responsive images not needed (no images used)

### Additional Optimizations (Optional)

1. **Enable Gzip Compression** (usually automatic on platforms)
2. **Enable Brotli Compression** (usually automatic on platforms)
3. **Add Cache Headers**:
   ```
   Cache-Control: public, max-age=31536000, immutable
   ```
4. **Enable HTTP/2** (usually automatic on platforms)

## Monitoring

### Check Website Status
```bash
# Simple health check
curl -I https://your-domain.com

# Detailed check
curl -v https://your-domain.com
```

### Analytics Setup (Optional)

Add analytics to each HTML file before `</body>`:

**Google Analytics**:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

**Plausible Analytics** (Privacy-friendly):
```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

## Troubleshooting

### Issue: 404 on Service Pages
**Solution**: Ensure all HTML files are in the root of the published directory, not in subdirectories.

### Issue: Styles Not Loading
**Solution**: Styles are embedded in each HTML file, so this shouldn't happen. Check that files weren't corrupted during upload.

### Issue: Broken Navigation
**Solution**: Ensure all HTML files are present and named correctly:
- index.html
- advisory.html
- brokerage.html
- asset-management.html
- research.html
- capital-raising.html
- trading.html

## CI/CD with GitHub Actions

The included `.github/workflows/deploy.yml` provides:
- HTML validation on every push
- Auto-deployment to Netlify/Vercel/GitHub Pages on main branch

### Required Secrets

Configure these in GitHub repository settings:

**For Netlify**:
- `NETLIFY_AUTH_TOKEN`
- `NETLIFY_SITE_ID`

**For Vercel**:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

## Support

For deployment issues:
- Check platform-specific documentation
- Verify all 7 HTML files are present
- Ensure file permissions are correct (644 for files, 755 for directories)
- Check browser console for errors

## License

© 2026 Atlas Maroc Capital Markets. All rights reserved.
