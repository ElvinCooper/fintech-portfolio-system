import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import cartera_endpoint, clientes_endpoint, healthcheck_endpoint

frontend_url = os.getenv("FRONTEND_URL")
cors_origins = [frontend_url] if frontend_url else []

app = FastAPI(
    title="Customer Portfolio System",
    description="API Empresarial para la gestión centralizada de carteras de clientes con Oracle PL/SQL.",
    version="1.0.0",
)

# CORS: permitir únicamente el frontend configurado
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

# Incluir routers
app.include_router(healthcheck_endpoint.router)
app.include_router(clientes_endpoint.router)
app.include_router(cartera_endpoint.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Customer Portfolio System API",
        "docs": "/docs",
        "status": "online",
    }
