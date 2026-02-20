from fastapi import FastAPI
from app.api import clientes_endpoint, healthcheck_endpoint, cartera_endpoint

app = FastAPI(
    title="Customer Portfolio System",
    description="API Empresarial para la gestión centralizada de carteras de clientes con Oracle PL/SQL.",
    version="1.0.0",
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
        "status": "online"
    }
