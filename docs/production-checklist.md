# Production Checklist

This is the recommended deployment shape for TicketForge today:

- Frontend: Vercel
- Backend: one VPS
- Worker: same VPS
- Postgres: managed or VPS-local
- Redis: managed or VPS-local

## 1. Pick your public URLs

Choose the exact production domains first.

Recommended split:

- Frontend: `https://ticketforge.example.com`
- Backend API: `https://api.ticketforge.example.com`

These values drive OAuth, frontend API calls, Stripe redirects, and webhook registration.

## 2. Fill the backend production `.env`

Start from [/.env.example](/home/shekerk/ticketforge/.env.example).

You must provide these manually:

```env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

APP_URL=https://ticketforge.example.com
API_URL=https://api.ticketforge.example.com

JWT_SECRET=
ENCRYPTION_KEY=

GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
GITHUB_WEBHOOK_SECRET=

ANTHROPIC_API_KEY=

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_PRICE_ID_TEAM=

SENTRY_DSN=
```

Generate secrets:

```bash
python3 - <<'PY'
import secrets
from cryptography.fernet import Fernet
print("JWT_SECRET=" + secrets.token_urlsafe(48))
print("ENCRYPTION_KEY=" + Fernet.generate_key().decode())
print("GITHUB_WEBHOOK_SECRET=" + secrets.token_urlsafe(32))
PY
```

## 3. Set the Vercel frontend environment

Use [frontend/.env.vercel.example](/home/shekerk/ticketforge/frontend/.env.vercel.example) as the reference.

Set these in Vercel:

```env
NEXT_PUBLIC_API_URL=https://api.ticketforge.example.com
NEXT_PUBLIC_SENTRY_DSN=
```

That `NEXT_PUBLIC_API_URL` must match backend `API_URL`.

## 4. Create the production GitHub OAuth app

Under your GitHub account (`shekerkamma`) or an org you control, create an OAuth app with:

- Application name: `TicketForge Production`
- Homepage URL: `https://ticketforge.example.com`
- Authorization callback URL: `https://api.ticketforge.example.com/api/auth/github/callback`

Then copy:

- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`

into the backend production `.env`.

Reference: [docs/github-oauth-setup.md](/home/shekerk/ticketforge/docs/github-oauth-setup.md)

## 5. Configure Stripe

Create:

- one product for the Team plan
- one recurring price
- one webhook endpoint

Set:

- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRICE_ID_TEAM`

Webhook endpoint:

- `https://api.ticketforge.example.com/api/webhooks/stripe`

Events:

- `checkout.session.completed`
- `customer.subscription.updated`
- `customer.subscription.deleted`

## 6. Deploy backend and worker

On the VPS:

```bash
git clone https://github.com/shekerkamma/ticketforge.git
cd ticketforge
cp .env.example .env
# fill in real values
docker-compose -f docker-compose.prod.yml up -d
docker build -t ticketforge-sandbox -f sandbox/Dockerfile.sandbox sandbox/
```

## 7. Deploy frontend to Vercel

In Vercel:

1. Import the repo
2. Set the root directory to `frontend`
3. Add `NEXT_PUBLIC_API_URL`
4. Deploy

## 8. Point DNS

Create DNS records for:

- `ticketforge.example.com`
- `api.ticketforge.example.com`

The backend domain must resolve to the VPS.
The frontend domain must resolve to Vercel.

## 9. Verify production

Backend:

- `GET https://api.ticketforge.example.com/api/health`
- `GET https://api.ticketforge.example.com/docs`

Frontend:

- homepage loads
- `Sign in with GitHub` starts OAuth
- callback returns to the frontend with a token

Billing:

- Stripe checkout session can be created
- Stripe webhook reaches backend

## 10. Known manual inputs

I cannot infer or create these for you:

- GitHub OAuth client ID
- GitHub OAuth client secret
- Anthropic API key
- Stripe keys and price ID
- Sentry DSN
- production domain names
- VPS host/IP

## 11. Recommended first live pass

Do this in order:

1. Deploy backend with health check only
2. Deploy frontend with `NEXT_PUBLIC_API_URL`
3. Create GitHub OAuth app with the final domains
4. Test browser login
5. Add Stripe last
