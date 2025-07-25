import os


class DatabaseConfig:
    """
    Database configuration for PostgreSQL.

    In Clean Architecture:
    - This is part of the Frameworks & Drivers layer
    - It handles environment-specific configuration
    - It's used by the Interface Adapters layer
    """

    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = int(os.getenv("POSTGRES_PORT", "5432"))
        self.database = os.getenv("POSTGRES_DB", "fastfood")
        self.username = os.getenv("POSTGRES_USER", "postgres")
        self.password = os.getenv("POSTGRES_PASSWORD", "password123")
        self.driver = os.getenv("DRIVER_NAME", "postgresql")

    @property
    def connection_string(self) -> str:
        """Get the PostgreSQL connection string"""
        return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def async_connection_string(self) -> str:
        """Get the async PostgreSQL connection string"""
        return f"{self.driver}+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

    def __str__(self) -> str:
        return f"DatabaseConfig(host={self.host}, port={self.port}, database={self.database}, username={self.username})"


# Global database configuration instance
db_config = DatabaseConfig()
