# Vercel Hobby Setup

Use Vercel Hobby for the `frontend/` app only. This repo's backend, worker, and Docker sandbox should stay off Vercel.

## What Vercel Handles

- Next.js frontend in `frontend/`
- Production deploys from `main`
- Preview deploys for branches and pull requests

## What Stays Elsewhere

- FastAPI backend
- ARQ worker
- Docker sandbox image and daemon
- PostgreSQL / Redis

## Vercel Project Settings

Create a new Vercel project connected to `shekerkamma/ticketforge`.

Set:

- Framework Preset: `Next.js`
- Root Directory: `frontend`
- Install Command: `npm install`
- Build Command: `npm run build`

`frontend/vercel.json` already matches those commands.

## Vercel Environment Variables

Set these in the Vercel project:

```env
NEXT_PUBLIC_API_URL=https://api.ticketforge.example.com
NEXT_PUBLIC_SENTRY_DSN=
```

Use your real backend origin for `NEXT_PUBLIC_API_URL`.

## Backend Environment Variables

Your backend must know the frontend origin used after GitHub OAuth and for browser CORS.

Minimum production backend values:

```env
APP_URL=https://ticketforge.example.com
API_URL=https://api.ticketforge.example.com
```

If you want Vercel preview deployments to support GitHub login too, add one of these:

```env
APP_URL_REGEX=^https://.*\.vercel\.app$
```

or a narrower regex for your actual Vercel project hostnames, for example:

```env
APP_URL_REGEX=^https://ticketforge.*\.vercel\.app$
```

You can also allow fixed extra origins explicitly:

```env
APP_URLS=https://staging.ticketforge.example.com,https://ticketforge-preview.example.com
```

## GitHub OAuth

Your GitHub OAuth app still points at the backend callback, not Vercel:

- Homepage URL: `https://ticketforge.example.com`
- Authorization callback URL: `https://api.ticketforge.example.com/api/auth/github/callback`

The frontend now passes its current origin to the backend auth flow, so Vercel previews can round-trip back to the right deployment if that origin is allowed by `APP_URL`, `APP_URLS`, or `APP_URL_REGEX`.

## Recommended Free Setup

- Frontend: Vercel Hobby
- Backend: one VPS or other always-on host
- Database: managed Postgres or VPS-local Postgres
- Redis: managed Redis or VPS-local Redis

This is the cheapest setup that still matches the codebase assumptions.
