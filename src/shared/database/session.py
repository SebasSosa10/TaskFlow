from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.shared.config.settings import settings
from src.shared.database.base import Base


def import_all_models() -> None:
    """Registra todos los modelos ORM en metadata."""
    from src.modules.users.entities.user import UserModel  # noqa: F401
    from src.modules.projects.entities.project import ProjectModel  # noqa: F401
    from src.modules.projects.entities.project_member import ProjectMemberModel  # noqa: F401
    from src.modules.tasks.entities.task import TaskModel  # noqa: F401
    from src.modules.history.entities.history import HistoryModel  # noqa: F401
    from src.modules.notifications.entities.notification import NotificationModel  # noqa: F401


import_all_models()

engine = create_async_engine(
    settings.db_url,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
