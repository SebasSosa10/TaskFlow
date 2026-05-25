import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.modules.auth.routes.auth_routes import router as auth_router
from src.modules.history.routes.history_routes import router as history_router
from src.modules.kanban.routes.kanban_routes import router as kanban_router
from src.modules.notifications.routes.notification_routes import (
    router as notifications_router,
)
from src.modules.projects.routes.project_routes import router as projects_router
from src.modules.reports.routes.report_routes import router as reports_router
from src.modules.tasks.routes.task_routes import router as tasks_router
from src.modules.users.routes.user_routes import router as users_router
from src.shared.config.settings import settings
from src.shared.database.init_db import init_database
from src.shared.database.session import engine
from src.shared.exceptions.handlers import register_exception_handlers

API_PREFIX = "/api"

OPENAPI_TAGS = [
    {
        "name": "Autenticación",
        "description": "Inicio de sesión, registro y perfil del usuario.",
    },
    {
        "name": "Usuarios",
        "description": "Gestión de usuarios, roles y tareas asignadas.",
    },
    {
        "name": "Proyectos",
        "description": "Gestión de proyectos, miembros y tareas por proyecto.",
    },
    {"name": "Tareas", "description": "Creación, asignación y seguimiento de tareas."},
    {
        "name": "Reportes",
        "description": "Reportes de desempeño, proyectos, tareas y usuarios.",
    },
    {"name": "Historial", "description": "Registro de actividades del sistema."},
    {"name": "Tablero Kanban", "description": "Vista Kanban de tareas por proyecto."},
    {"name": "Notificaciones", "description": "Notificaciones para usuarios."},
    {"name": "Estado", "description": "Verificación de salud del servicio."},
]

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_database()
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST para gestión de proyectos y tareas con arquitectura modular.",
    openapi_tags=OPENAPI_TAGS,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(projects_router, prefix=API_PREFIX)
app.include_router(tasks_router, prefix=API_PREFIX)
app.include_router(reports_router, prefix=API_PREFIX)
app.include_router(history_router, prefix=API_PREFIX)
app.include_router(kanban_router, prefix=API_PREFIX)
app.include_router(notifications_router, prefix=API_PREFIX)


@app.get(
    "/health",
    tags=["Estado"],
    summary="Verificar estado del servicio",
    response_description="Estado actual de la API",
)
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
