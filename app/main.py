from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

# Import routers
from app.routers import store, checkout
from app.config import get_settings
from app.services.store_service import StoreException, StoreService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ─── startup ───
    app.state.store_service = StoreService()  # SINGLETON
    logger.info(f"Starting {settings.app_name} v2.0.0")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Base URL: {settings.base_url}")
    yield
    # ─── shutdown ───
    # (nothing to clean for StoreService, but put teardown here if needed)
    logger.info(f"Shutting down {settings.app_name}")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A simple and secure online store for kids",
    version="2.0.0",
    debug=settings.debug,
    lifespan=lifespan
)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    max_age=settings.session_expire_seconds
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(store.router)
app.include_router(checkout.router)

# Templates
templates = Jinja2Templates(directory="templates")


# Exception handlers
@app.exception_handler(StoreException)
async def store_exception_handler(request: Request, exc: StoreException):
    """Handle store-specific exceptions"""
    logger.error(f"Store error: {exc.message}")

    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message, "status_code": exc.status_code}
        )
    else:
        # For web requests, redirect to error page or show error in template
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": exc.message},
            status_code=exc.status_code
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")

    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "status_code": exc.status_code}
        )
    else:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": exc.detail},
            status_code=exc.status_code
        )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "An unexpected error occurred", "status_code": 500}
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "app": settings.app_name}


# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint - redirect to store"""
    return templates.TemplateResponse("welcome.html", {"request": request})


# API info endpoint
@app.get("/api/info")
async def api_info():
    """Get API information"""
    return {
        "app_name": settings.app_name,
        "version": "2.0.0",
        "description": "Kids Web Store API",
        "endpoints": {
            "store": "/store/",
            "checkout": "/checkout/",
            "menu": "/store/menu",
            "cart": "/store/cart",
            "health": "/health"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )