## Options Tracking & Risk Dashboard

This is a small web dashboard for tracking options positions and viewing simple portfolio risk metrics. It is built with React and Vite and can be deployed as a static web app.

### Running locally

1. Install dependencies:

```bash
cd /Users/sumitsapkota/Desktop/project-1
npm install
```

2. Start the dev server:

```bash
npm run dev
```

Then open the printed local URL in your browser.

### Building for the web (deployment)

To create a static production build:

```bash
npm run build
```

This outputs static files into the `dist` directory. You can deploy the contents of `dist` to any static host (for example Netlify, GitHub Pages, or Vercel).

### Features

- **Options tracking**: Interactive table where you can add, edit, or remove listed options positions (symbol, strike, expiry, type, quantity, premium, IV).
- **Risk summary**: High-level metrics including:
  - **Total delta**: Simple approximate delta exposure in underlying shares.
  - **Net premium**: Total premium paid/received across positions.
  - **Stress P/L (±15%)**: Hypothetical worst case P/L under ±15% price shocks.
  - **Configurable risk-free rate**: Used as a configurable assumption in your risk view.


