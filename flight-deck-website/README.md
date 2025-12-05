# Flight Deck - Aviation Infrastructure Intelligence

A brutalist, terminal-aesthetic website for strategic advisory in airport privatization and Advanced Air Mobility (AAM) infrastructure.

## Design Philosophy

**Executive-Grade Positioning**
- No marketing fluff or subjective language
- Factual, urgent, and direct communication
- Technical aesthetic inspired by NYC design studios (dd.nyc)
- Dark terminal interface with Bloomberg-style data streams

**Visual Language**
- **Typography**: Inter (body), Space Mono (terminal/mono), Lora (serif headlines)
- **Colors**: Deep Black (#0B0C10), Silver (#C5C6C7), Cyan Accent (#45A29E)
- **Layout**: Brutalist grid system with mathematical precision
- **No Stock Photos**: Abstract data visualizations only

## Features

### Dynamic Interactions
✅ **Parallax scrolling** - Multi-layer depth on scroll
✅ **Scroll-triggered animations** - Fade-ins and slide-ups via Intersection Observer
✅ **Animated data visualizations** - SVG path drawing and data point reveals
✅ **Horizontal scroll effects** - Ticker and grid movement
✅ **Mouse-reactive grid** - Background responds to cursor position
✅ **Timeline progress animation** - 15-year horizon visualization
✅ **Number counting** - Animated numerical reveals
✅ **Glitch hover effects** - Subtle cyberpunk aesthetic on titles

### Sections
1. **Dashboard (Hero)** - Core positioning + live data ticker
2. **Signal** - Market dynamics with abstract chart visualization
3. **Mechanics** - Methodology cards with blueprint overlay
4. **Forecast** - Predictive strategy with timeline
5. **Access** - Contact block with terminal aesthetic

## Project Structure

```
flight-deck-website/
├── index.html          # Single-page application (5 sections)
├── css/
│   └── style.css       # Complete design system (brutalist + terminal)
├── js/
│   └── main.js         # All dynamic interactions and animations
└── README.md           # This file
```

## Local Development

**1. Open directly in browser**
```bash
open index.html
# or
python3 -m http.server 8080
```

**2. Live Server (VS Code)**
- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

## Deployment

### Option 1: Netlify (Recommended)
```bash
# Drag and drop the flight-deck-website folder to netlify.com/drop
# or use Netlify CLI:
npm install -g netlify-cli
cd flight-deck-website
netlify deploy --prod
```

### Option 2: Vercel
```bash
npm install -g vercel
cd flight-deck-website
vercel --prod
```

### Option 3: GitHub Pages
```bash
# Push to GitHub repository
# Enable GitHub Pages in Settings → Pages → Source: main branch
# Set custom domain if needed
```

### Option 4: Render (Static Site)
```yaml
# Create render.yaml in root:
services:
  - type: web
    name: flight-deck-website
    env: static
    staticPublishPath: ./flight-deck-website
    buildCommand: echo "No build needed"
```

### Option 5: AWS S3 + CloudFront
```bash
# Upload to S3 bucket with static hosting enabled
aws s3 sync flight-deck-website/ s3://your-bucket-name --acl public-read
```

## Customization

### Update Content
Edit `index.html` sections:
- Hero title: `.hero-title`
- Ticker items: `.ticker-item` (duplicate for seamless loop)
- Deliverables: `.deliverable-item` blocks
- Contact info: `.contact-item` blocks

### Change Colors
Edit CSS variables in `style.css`:
```css
:root {
    --black: #0B0C10;       /* Background */
    --silver: #C5C6C7;      /* Text */
    --cyan: #45A29E;        /* Accent */
}
```

### Adjust Animations
Modify JavaScript in `main.js`:
- Parallax speeds: `parallaxElements` array
- Animation delays: `setTimeout` values
- Scroll thresholds: `IntersectionObserver` options

## Performance

**Optimization Features:**
- Zero dependencies (vanilla JS)
- Inline SVG graphics (no external images)
- CSS animations (GPU-accelerated)
- Lazy loading via Intersection Observer
- Throttled scroll events
- Debounced resize handlers

**Load Time Metrics:**
- First Contentful Paint: < 1s
- Time to Interactive: < 2s
- Lighthouse Score: 95+ (Performance)

## Browser Support

✅ Chrome/Edge 90+
✅ Firefox 88+
✅ Safari 14+
✅ Mobile browsers (iOS Safari, Chrome Mobile)

**Progressive Enhancement:**
- Core content accessible without JavaScript
- CSS Grid with flexbox fallback
- Intersection Observer with fallback visibility

## Accessibility

- Semantic HTML5 structure
- ARIA labels on interactive elements
- Keyboard navigation support
- High contrast ratio (WCAG AA)
- Reduced motion support (prefers-reduced-motion)

## Technical Stack

**Frontend Only:**
- HTML5 (semantic markup)
- CSS3 (Grid, Flexbox, Animations)
- Vanilla JavaScript (ES6+)

**Fonts (Google Fonts):**
- Inter (body text)
- Space Mono (terminal/monospace)
- Lora (serif headlines)

## Future Enhancements

**Phase 2 (Optional):**
- [ ] Contact form with backend integration
- [ ] CMS integration (Contentful, Sanity)
- [ ] Analytics (Plausible, Fathom)
- [ ] Dark/Light mode toggle
- [ ] Multi-language support
- [ ] Blog/Insights section

**Advanced Interactions:**
- [ ] WebGL background (Three.js)
- [ ] Cursor trail effect
- [ ] Sound design (subtle UI sounds)
- [ ] Scroll-jacking sections

## License

Proprietary - All rights reserved

## Contact

**Email**: advisory@flightdeck.com
**Office**: Montreal | Dubai
**Sector**: Global Infrastructure & Privatization

---

Built with precision. No compromises.
