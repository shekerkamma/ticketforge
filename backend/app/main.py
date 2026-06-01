import contextlib
from collections.abc import Awaitable, Callable

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app import models as _models  # noqa: F401
from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router
from app.api.billing import router as billing_router
from app.api.dashboard import router as dashboard_router
from app.api.error_handlers import register_error_handlers
from app.api.repos import router as repos_router
from app.api.sse import router as sse_router
from app.api.teams import router as teams_router
from app.api.tickets import router as tickets_router
from app.api.webhooks import router as webhooks_router
from app.config import settings
from app.db import Base, engine

if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0.1)


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

app = FastAPI(
    title="TicketForge",
    description="From GitHub Issue to merged PR via multi-agent AI pipeline",
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
register_error_handlers(app)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(_request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={"error": "rate_limit_exceeded", "message": "Too many requests"},
        headers={"Retry-After": str(exc.detail)},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_app_origins(),
    allow_origin_regex=settings.app_url_regex or None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(webhooks_router)
app.include_router(dashboard_router)
app.include_router(teams_router)
app.include_router(repos_router)
app.include_router(tickets_router)
app.include_router(sse_router)
app.include_router(analytics_router)
app.include_router(billing_router)


@app.middleware("http")
async def add_cache_headers(
    request: Request,
    call_next: Callable[[Request], Awaitable[JSONResponse]],
):
    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
