from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared.database.base import Base


class UserRole(str, Enum):
    ADMINISTRADOR = "administrador"
    LIDER_PROYECTO = "lider_proyecto"
    USUARIO = "usuario"


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(
            UserRole,
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        default=UserRole.USUARIO,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    owned_projects: Mapped[list["ProjectModel"]] = relationship(
        back_populates="owner", foreign_keys="ProjectModel.owner_id"
    )
    assigned_tasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="assignee", foreign_keys="TaskModel.assignee_id"
    )
    created_tasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="creator", foreign_keys="TaskModel.created_by_id"
    )
    history_entries: Mapped[list["HistoryModel"]] = relationship(back_populates="user")
    project_memberships: Mapped[list["ProjectMemberModel"]] = relationship(
        back_populates="user"
    )
    notifications: Mapped[list["NotificationModel"]] = relationship(
        back_populates="user"
    )
