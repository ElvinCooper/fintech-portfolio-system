from fastapi import APIRouter

router = APIRouter(
    tags=["Health Check"],
)


@router.get("/health", status_code=200)
def health_check():
    """
    Endpoint para verificar la salud de la API y conectividad básica.
    """
    return {"status": "ok", "service": "portfolio-api"}
