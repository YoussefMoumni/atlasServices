# Atlas Maroc Capital Markets - Static Website

A professional promotional website showcasing Atlas Maroc Capital Markets services through dedicated HTML pages.

## Overview

This is a pure static website built with HTML and CSS only. No backend, no frontend framework, no build process required.

## Structure

```
website/
├── index.html              # Service portfolio overview page
├── advisory.html           # Advisory service page
├── brokerage.html         # Brokerage service page
├── asset-management.html  # Asset Management service page
├── research.html          # Research service page
├── capital-raising.html   # Capital Raising service page
├── trading.html           # Trading service page
└── README.md              # This file
```

## Features

- **6 Dedicated Service Pages**: Each service has its own promotional page
- **Responsive Design**: Three breakpoints (desktop, tablet, mobile)
- **Professional Design**: Financial-services visual language with:
  - Dark theme (#07111f background)
  - Brand colors: Gold (#c8a96b) and Accent Blue (#63b3d1)
  - Inter font family
  - Layered card surfaces with shadows
  - Smooth gradients and glassmorphism effects

## Pages

### 1. index.html - Service Portfolio
The overview page presenting the entire Atlas Maroc Capital Markets service universe.

### 2. advisory.html - Advisory
Strategic advisory for issuers, shareholders, and institutions navigating decisive capital-markets moments.

### 3. brokerage.html - Brokerage
Institutional market access through attentive sales coverage, intelligent order handling, and responsive service.

### 4. asset-management.html - Asset Management
Portfolio management with institutional rigor, combining conviction, allocation discipline, and value creation.

### 5. research.html - Research
Independent capital-markets research delivering sector insight, issuer perspective, and actionable context.

### 6. capital-raising.html - Capital Raising
Capital raising solutions that align issuer ambition with investor appetite through disciplined preparation.

### 7. trading.html - Trading
Trading capabilities combining market awareness, execution precision, and responsive desk coverage.

## Deployment

### Option 1: Simple HTTP Server (Python)
```bash
cd website
python3 -m http.server 8000
```
Then open: http://localhost:8000

### Option 2: Simple HTTP Server (Node.js)
```bash
cd website
npx http-server -p 8000
```

### Option 3: Static Hosting Services
Deploy to any static hosting service:
- **Netlify**: Drag and drop the `website` folder
- **Vercel**: Connect your git repository
- **GitHub Pages**: Push to a GitHub repository and enable Pages
- **AWS S3 + CloudFront**: Upload to S3 bucket with static website hosting
- **Azure Static Web Apps**: Deploy via Azure portal or CLI
- **Google Cloud Storage**: Create bucket with website configuration

## Design System

### Color Palette
- **Background**: `#07111f` (Dark navy)
- **Panel**: `#0d1b2d` and `#10243d` (Layered surfaces)
- **Text**: `#eff5fb` (Primary) and `#a5b6c9` (Muted)
- **Brand**: `#c8a96b` (Gold)
- **Accent**: `#63b3d1` (Blue)
- **Lines**: `rgba(255,255,255,.1)` (Subtle borders)

### Typography
- **Font Family**: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- **H1**: clamp(2.6rem, 6vw, 4.9rem) - Responsive heading
- **H2**: clamp(1.7rem, 3vw, 2.35rem) - Section titles
- **Body**: 1rem with 1.6 line-height

### Layout
- **Max Width**: 1180px container
- **Border Radius**: 24px (panels), 22px (cards), 18px (stats)
- **Shadow**: `0 24px 60px rgba(0,0,0,.28)` - Elevated surfaces
- **Responsive Breakpoints**:
  - Desktop: > 980px
  - Tablet: 720px - 980px
  - Mobile: < 720px

## Page Structure

Each service page follows this consistent structure:

1. **Sticky Header** with brand and navigation
2. **Hero Section** with service title and description
3. **Value Highlights** - 3-column card grid
4. **Market Perspective** - Split grid layout
5. **Process/Approach** - Numbered steps
6. **Coverage/Strengths** - 3-column insight grid
7. **CTA Panel** - Call to action with navigation
8. **Footer** - Brand statement and links

## Navigation

All pages include consistent navigation:
- Overview (index.html)
- Advisory
- Brokerage
- Asset Management
- Research
- Capital Raising
- Trading

## Browser Support

- Chrome/Edge (modern)
- Firefox (modern)
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## Performance

- No JavaScript required
- Minimal CSS (embedded in each HTML file)
- No external dependencies
- Fast load times
- SEO-friendly semantic HTML

## Accessibility

- Semantic HTML5 structure
- ARIA labels and landmarks
- Keyboard navigation support
- Focus states on interactive elements
- Responsive text sizing with clamp()
- High contrast text (WCAG AA compliant)

## Development Notes

This website was designed with the following principles:

1. **Clarity first**: Hero content explains each service immediately
2. **Institutional tone**: Subdued colors and refined spacing reinforce trust
3. **Responsive readability**: Graceful collapse from desktop to mobile
4. **Static implementation**: No build tools or frameworks required

## License

© 2026 Atlas Maroc Capital Markets. All rights reserved.
