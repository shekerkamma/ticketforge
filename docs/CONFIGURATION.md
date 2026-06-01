# TicketForge Configuration Reference

## Environment Variables

All configuration is via environment variables.

- Production backend/worker variables: copy [/.env.example](/home/shekerk/ticketforge/.env.example) to `.env`
- Local backend variables: copy [backend/.env.example](/home/shekerk/ticketforge/backend/.env.example) to `backend/.env`
- Frontend local variables: copy [frontend/.env.example](/home/shekerk/ticketforge/frontend/.env.example) if needed
- Frontend Vercel reference: [frontend/.env.vercel.example](/home/shekerk/ticketforge/frontend/.env.vercel.example)

### Required

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (`postgresql+asyncpg://...`) |
| `GITHUB_CLIENT_ID` | GitHub OAuth app client ID |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth app client secret |
| `GITHUB_WEBHOOK_SECRET` | Shared secret for webhook signature verification |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude |
| `JWT_SECRET` | Secret key for JWT token signing (use a strong random value) |
| `ENCRYPTION_KEY` | Fernet-compatible key for encrypting GitHub tokens at rest |
| `POSTGRES_USER` | PostgreSQL username for `docker-compose.prod.yml` |
| `POSTGRES_PASSWORD` | PostgreSQL password for `docker-compose.prod.yml` |
| `POSTGRES_DB` | PostgreSQL database name for `docker-compose.prod.yml` |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_URL` | `http://localhost:3000` | Frontend URL (used for CORS and Stripe redirects) |
| `APP_URLS` | _(empty)_ | Additional allowed frontend origins, comma-separated |
| `APP_URL_REGEX` | _(empty)_ | Regex for allowed frontend origins, useful for Vercel preview URLs |
| `API_URL` | `http://localhost:8000` | Backend URL (used for webhook registration) |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection for ARQ task queue |
| `JWT_EXPIRY_HOURS` | `24` | JWT token lifetime in hours |
| `STRIPE_SECRET_KEY` | _(empty)_ | Stripe secret key for billing |
| `STRIPE_WEBHOOK_SECRET` | _(empty)_ | Stripe webhook signing secret |
| `STRIPE_PRICE_ID_TEAM` | _(empty)_ | Stripe Price ID for the Team plan |
| `SENTRY_DSN` | _(empty)_ | Sentry DSN for backend error tracking |
| `NEXT_PUBLIC_SENTRY_DSN` | _(empty)_ | Sentry DSN for frontend error tracking |
| `LOCAL_DEV_GITHUB_LOGIN` | `local-dev` | Local identity used by `/api/auth/dev-login` when bootstrapping a fresh DB |
| `LOCAL_DEV_EMAIL` | `local-dev@example.com` | Local dev email used for `/api/auth/dev-login` |
| `LOCAL_DEV_TEAM_NAME` | `Local Dev Team` | Local team name created by `/api/auth/dev-login` |

## Production URL Rules

These values must stay consistent:

- `APP_URL` is the frontend origin users land on after auth
- `APP_URLS` can list extra fixed frontend origins that should be allowed
- `APP_URL_REGEX` can allow dynamic preview origins such as Vercel branch URLs
- `API_URL` is the backend public origin
- GitHub OAuth callback URL must be:
  `{API_URL}/api/auth/github/callback`
- Frontend `NEXT_PUBLIC_API_URL` must point at the same backend origin as `API_URL`

Example production set:

```env
APP_URL=https://ticketforge.example.com
APP_URLS=
APP_URL_REGEX=^https://ticketforge.*\.vercel\.app$
API_URL=https://api.ticketforge.example.com
NEXT_PUBLIC_API_URL=https://api.ticketforge.example.com
```

## Repository Configuration

Each connected repository has a JSONB `config` field. Set via the API (`PATCH /api/v1/teams/:id/repos/:repo_id`):

```json
{
  "review": {
    "require_tests": true,
    "security_check": true,
    "style_check": true,
    "min_confidence": 0.6
  },
  "slack_webhook_url": "https://hooks.slack.com/services/..."
}
```

### Review Config

| Key | Default | Description |
|-----|---------|-------------|
| `require_tests` | `true` | Require test coverage in generated fixes |
| `security_check` | `true` | Reject fixes with security score < 0.3 |
| `style_check` | `true` | Include style dimension in review |
| `min_confidence` | `0.6` | Minimum confidence threshold for auto-approve |

### Slack Notifications

Set `slack_webhook_url` in repo config to receive Slack messages when tickets are escalated.

## Plan Limits

| Plan | Monthly Tickets |
|------|----------------|
| Free | 20 |
| Team | 500 |
| Enterprise | 10,000 |

## Trigger Labels

Configure which GitHub issue labels trigger the pipeline. Default: `["bug"]`. Set per-repository in the dashboard Settings page.
