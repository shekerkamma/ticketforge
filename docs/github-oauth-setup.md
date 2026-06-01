# GitHub OAuth Setup

This repo uses a GitHub OAuth app for the browser sign-in flow.

The backend route is:

- `/api/auth/github`

The callback route expected by the backend is:

- `/api/auth/github/callback`

## Local setup for `shekerkamma`

Create the OAuth app under your GitHub account:

1. Open GitHub `Settings`
2. Open `Developer settings`
3. Open `OAuth apps`
4. Click `New OAuth App`

Use these values for local development:

- Application name: `TicketForge Local`
- Homepage URL: `http://localhost:3000`
- Authorization callback URL: `http://localhost:8000/api/auth/github/callback`

Then copy the generated values into `backend/.env`:

```env
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
GITHUB_WEBHOOK_SECRET=choose_a_random_secret
```

Local app URLs should remain:

```env
APP_URL=http://localhost:3000
API_URL=http://localhost:8000
```

## Production values

For production, create a separate OAuth app or update the existing one with your real deployed URLs.

Typical values:

- Homepage URL: `https://your-frontend-domain`
- Authorization callback URL: `https://your-api-domain/api/auth/github/callback`

Then set:

```env
APP_URL=https://your-frontend-domain
API_URL=https://your-api-domain
```

## Important constraints

- This app is using a GitHub OAuth app, not a GitHub App.
- GitHub OAuth apps can only have one callback URL.
- If you pass `redirect_uri`, GitHub requires the host and port to match the configured callback URL rules.
- For this repo, the backend constructs the callback URL from `API_URL`.

## Verify the flow

After saving the client ID and secret:

1. Start the backend and frontend
2. Open `http://localhost:3000`
3. Click `Sign in with GitHub`
4. Approve the OAuth app
5. Confirm that GitHub redirects to:
   `http://localhost:8000/api/auth/github/callback`
6. Confirm the app ends on:
   `http://localhost:3000/auth/callback?token=...`

## Current implementation references

- Backend auth routes: [backend/app/api/auth.py](/home/shekerk/ticketforge/backend/app/api/auth.py)
- Backend config: [backend/app/config.py](/home/shekerk/ticketforge/backend/app/config.py)

## Sources

- GitHub Docs, "Creating an OAuth app": https://docs.github.com/en/developers/apps/creating-an-oauth-app
- GitHub Docs, "Authorizing OAuth apps": https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps
