# VPC Animated Frontend

Responsive animated dashboard for the VPC FastAPI reliability lab.

## Files
- `index.html` — semantic dashboard layout
- `styles.css` — responsive styling, animated infrastructure motif, reduced-motion support
- `app.js` — polls `/health`, `/ready`, `/metrics` every 15 seconds

## API connection
The dashboard expects API routes at the same origin as the page. Your current API was bound to `127.0.0.1:18002`; opening this page via `file://` or hosting it on another origin will not automatically connect. Browser same-origin and CORS rules apply.

For a local preview, run `python3 -m http.server 8080` in this directory and open `http://127.0.0.1:8080`. The visual page will load, but live probes need a same-origin reverse proxy or a reachable API origin with a deliberately configured CORS policy.

Do not expose the API publicly just to make the dashboard work. Before any public tunnel, restrict `/metrics` and review FastAPI `/docs`, `/redoc`, and `/openapi.json`.

## Security
API response values are inserted with `textContent` rather than `innerHTML`. This reduces DOM-XSS risk in this frontend, but is not a full security audit. Google Fonts are loaded externally; remove the font links for a fully self-hosted page.
