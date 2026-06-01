# TicketForge Deployment Guide

## Production Architecture

- **Backend**: FastAPI + Gunicorn/Uvicorn, PostgreSQL, Redis
- **Frontend**: Next.js deployed to Vercel (or self-hosted)
- **Sandbox**: Docker daemon on the same VPS as the backend

## VPS Deployment

### Prerequisites

- Ubuntu 22.04+ VPS with Docker installed
- Domain name with DNS pointing to VPS
- PostgreSQL 16 (managed or self-hosted)
- Redis 7

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/ticketforge.git
   cd ticketforge
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

   Minimum production values:
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `POSTGRES_DB`
   - `APP_URL`
   - `API_URL`
   - `JWT_SECRET`
   - `ENCRYPTION_KEY`
   - `GITHUB_CLIENT_ID`
   - `GITHUB_CLIENT_SECRET`
   - `GITHUB_WEBHOOK_SECRET`
   - `ANTHROPIC_API_KEY`

3. **Build and run**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Set up SSL** (Caddy handles automatic HTTPS)
   ```
   # Caddyfile
   ticketforge.example.com {
       reverse_proxy localhost:8000
   }
   ```

5. **Build the sandbox image**
   ```bash
   docker build -t ticketforge-sandbox -f sandbox/Dockerfile.sandbox sandbox/
   ```

## Vercel Frontend Deployment

1. Connect the `frontend/` directory to Vercel
2. Set environment variables:
   - `NEXT_PUBLIC_API_URL` = `https://api.ticketforge.example.com`
   - `NEXT_PUBLIC_SENTRY_DSN` = your Sentry DSN
   - Use [frontend/.env.vercel.example](/home/shekerk/ticketforge/frontend/.env.vercel.example) as the reference
3. Deploy

Important:
- `NEXT_PUBLIC_API_URL` must match the backend public origin
- That same backend public origin should also be used as `API_URL` on the backend
- If these drift, GitHub OAuth callbacks and browser API requests will break

## GitHub OAuth App

Create a GitHub OAuth app:
- Homepage URL: `https://ticketforge.example.com`
- Callback URL: `https://api.ticketforge.example.com/api/auth/github/callback`

For local development with your GitHub account, see [docs/github-oauth-setup.md](/home/shekerk/ticketforge/docs/github-oauth-setup.md).

## Stripe Setup

1. Create a product and price in Stripe Dashboard
2. Set `STRIPE_PRICE_ID_TEAM` to the price ID
3. Configure webhook endpoint: `https://api.ticketforge.example.com/api/webhooks/stripe`
4. Events to listen for: `checkout.session.completed`, `customer.subscription.deleted`

Recommended production envs:
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRICE_ID_TEAM`

## Monitoring

- **Sentry**: Backend and frontend error tracking
- **Health check**: `GET /api/health` returns `{"status": "ok"}`

## Recommended Split

- Frontend: Vercel
- Backend: VPS with Docker Compose
- Worker: same VPS as backend
- Postgres: managed or VPS-local
- Redis: managed or VPS-local

This split matches the codebase assumptions today without requiring a major deployment refactor.
