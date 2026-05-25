from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    secret_key: str = "your_secret_key_change_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    app_name: str = "TaskFlow API"
    app_version: str = "1.0.0"

    # SQL Server
    db_server: str = r"DESKTOP-1N08KOM\MSSQLSERVER01"
    db_name: str = "TaskFlow"
    db_driver: str = "ODBC Driver 17 for SQL Server"
    db_trusted_connection: bool = True
    db_user: str = ""
    db_password: str = ""
    database_url: str | None = None

    @property
    def db_url(self) -> str:
        if self.database_url:
            return self.database_url

        if self.db_trusted_connection:
            odbc = (
                f"DRIVER={{{self.db_driver}}};"
                f"SERVER={self.db_server};"
                f"DATABASE={self.db_name};"
                f"Trusted_Connection=yes;"
                f"TrustServerCertificate=yes;"
            )
        else:
            odbc = (
                f"DRIVER={{{self.db_driver}}};"
                f"SERVER={self.db_server};"
                f"DATABASE={self.db_name};"
                f"UID={self.db_user};"
                f"PWD={self.db_password};"
                f"TrustServerCertificate=yes;"
            )

        return f"mssql+aioodbc:///?odbc_connect={quote_plus(odbc)}"


settings = Settings()
