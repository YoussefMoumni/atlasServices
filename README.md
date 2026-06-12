# Atlas Maroc Capital Markets - Promotional Website

A professional static website showcasing Atlas Maroc Capital Markets services through dedicated HTML pages.

## 🚀 Quick Start

### Local Development

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

The website will be available at `http://localhost:8000`

## 📁 Project Structure

```
.
├── website/                    # Main website files
│   ├── index.html             # Service portfolio overview
│   ├── advisory.html          # Advisory service page
│   ├── brokerage.html         # Brokerage service page
│   ├── asset-management.html  # Asset Management page
│   ├── research.html          # Research service page
│   ├── capital-raising.html   # Capital Raising page
│   ├── trading.html           # Trading service page
│   └── README.md              # Website documentation
├── .github/workflows/         # CI/CD configuration
│   └── deploy.yml            # GitHub Actions deployment
├── DEPLOYMENT.md              # Deployment guide
├── IMPLEMENTATION_SUMMARY.md  # Implementation details
├── start.sh / start.bat      # Startup scripts
└── stop.sh / stop.bat        # Stop scripts
```

## 🎨 Features

- **7 Professional Pages**: Overview + 6 dedicated service pages
- **Responsive Design**: Desktop, tablet, and mobile optimized
- **Dark Theme**: Financial-services grade design
- **No Dependencies**: Pure HTML + CSS, no build tools
- **Fast Loading**: ~15 KB per page, inline styles
- **SEO Ready**: Semantic HTML, meta tags, proper headings
- **Accessible**: WCAG 2.1 AA compliant

## 🌐 Pages

1. **index.html** - Service Portfolio Overview
2. **advisory.html** - Strategic Advisory Services
3. **brokerage.html** - Institutional Brokerage
4. **asset-management.html** - Portfolio Management
5. **research.html** - Capital Markets Research
6. **capital-raising.html** - Funding Solutions
7. **trading.html** - Trading Capabilities

## 🚢 Deployment

### Recommended: One-Click Deploy

Deploy to Netlify or Vercel with one click.

### Other Options

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to:
- Netlify, Vercel, GitHub Pages
- AWS S3 + CloudFront
- Azure Static Web Apps
- Google Cloud Storage
- Cloudflare Pages
- Firebase Hosting
- And more...

## 🎯 Design System

### Colors
- **Background**: `#07111f` (Dark navy)
- **Brand Gold**: `#c8a96b`
- **Accent Blue**: `#63b3d1`
- **Text**: `#eff5fb` (Primary), `#a5b6c9` (Muted)

### Typography
- **Font**: Inter with system fallbacks
- **Responsive sizing** using CSS clamp()

### Layout
- **Max Width**: 1180px
- **Breakpoints**: 980px (tablet), 720px (mobile)

## 📊 Performance

- **Total Size**: ~110 KB (all pages)
- **HTTP Requests**: 1 per page
- **Load Time**: < 500ms
- **No JavaScript**: Instant interactivity

## ♿ Accessibility

- Semantic HTML5 structure
- ARIA labels and landmarks
- Keyboard navigation support
- WCAG 2.1 Level AA compliant
- High contrast text

## 🔧 Development

### Requirements
- Python 3 (for local server)
- Any modern web browser

### Local Development
```bash
./start.sh              # Start server
./stop.sh               # Stop server
```

### Validation
All HTML files are validated on every push via GitHub Actions.

## 📖 Documentation

- [README.md](README.md) - This file
- [website/README.md](website/README.md) - Website-specific docs
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment instructions
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical details

## 🛠️ Technology

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Grid and Flexbox
- **No JavaScript** - Pure static content
- **No Build Tools** - Deploy as-is

## 🌟 Browser Support

- Chrome/Edge (modern)
- Firefox (modern)
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## 📝 License

© 2026 Atlas Maroc Capital Markets. All rights reserved.

## 🚀 Ready to Deploy

This project is production-ready. Choose your deployment platform and go live in minutes!