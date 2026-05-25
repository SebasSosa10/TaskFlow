import logging

from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError

from src.shared.config.settings import settings
from src.shared.database.base import Base
from src.shared.database.session import engine, import_all_models

logger = logging.getLogger(__name__)


def _connection_help_message() -> str:
    return (
        f"No se pudo conectar a SQL Server en {settings.db_server} "
        f"(base: {settings.db_name}). "
        "Verifica que SQL Server esté activo, que exista la BD TaskFlow "
        "y que tengas permisos (Windows Authentication). "
        "Si usas otro driver ODBC, cambia DB_DRIVER en .env "
        "(ej: ODBC Driver 18 for SQL Server)."
    )


async def init_database() -> None:
    """
    Crea las tablas definidas en los modelos ORM solo si no existen.
    Si la tabla ya está en la BD, no la vuelve a crear ni la modifica.
    """
    import_all_models()
    expected_tables = set(Base.metadata.tables.keys())

    try:
        async with engine.begin() as conn:
            def _create_missing(sync_conn) -> tuple[set[str], set[str]]:
                inspector = inspect(sync_conn)
                existing_before = set(inspector.get_table_names())

                Base.metadata.create_all(bind=sync_conn, checkfirst=True)

                existing_after = set(inspect(sync_conn).get_table_names())
                created = existing_after - existing_before
                already_exists = expected_tables & existing_before
                return created, already_exists

            created, already_exists = await conn.run_sync(_create_missing)
    except (OperationalError, OSError, ConnectionError) as exc:
        logger.error(_connection_help_message())
        raise RuntimeError(_connection_help_message()) from exc
    except Exception as exc:
        if "connection" in str(exc).lower() or "auth" in str(exc).lower():
            logger.error(_connection_help_message())
            raise RuntimeError(_connection_help_message()) from exc
        raise

    if created:
        logger.info("Tablas creadas: %s", ", ".join(sorted(created)))
    if already_exists:
        logger.info("Tablas ya existentes (sin cambios): %s", ", ".join(sorted(already_exists)))

    missing_from_db = expected_tables - created - already_exists
    if missing_from_db:
        logger.warning("Tablas esperadas no registradas en BD: %s", ", ".join(sorted(missing_from_db)))
