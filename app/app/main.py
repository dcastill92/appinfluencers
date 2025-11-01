"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, users, profiles, campaigns, notifications, subscription_plans, transactions

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Backend API for Influencers Platform MVP",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
# Note: Cannot use allow_origins=["*"] with allow_credentials=True
# Must specify exact origins when using credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "https://influencers-frontend.onrender.com",
        "https://influencers-api.onrender.com",
        "https://influencers-api-bj5q.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(campaigns.router)
app.include_router(notifications.router)
app.include_router(subscription_plans.router)
app.include_router(transactions.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Influencers Platform API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    Initialize database connections and other resources.
    """
    print(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"CORS: Configured for specific origins (credentials enabled)")
    print(f"Database URL: {settings.DATABASE_URL[:20]}...")
    
    # Auto-seed database if empty
    try:
        print("🔄 Iniciando proceso de auto-seed...")
        from app.core.database import AsyncSessionLocal, engine, Base
        from app.core.seed import seed_initial_data
        
        # Crear tablas si no existen
        print("📋 Creando tablas...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas verificadas/creadas")
        
        # Seed data si la BD está vacía
        print("🌱 Verificando datos iniciales...")
        async with AsyncSessionLocal() as db:
            await seed_initial_data(db)
    except Exception as e:
        print(f"⚠️  Error durante auto-seed: {e}")
        import traceback
        traceback.print_exc()
        # No interrumpir el inicio de la app


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.
    Clean up resources.
    """
    print("Shutting down...")
