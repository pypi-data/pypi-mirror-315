from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncConnection
from .logger_config import logger
from dotenv import dotenv_values
from threading import Lock
import sqlalchemy
import aioodbc
import weakref

# Mapping of required fields for each supported database type
REQUIRED_FIELDS = {
    "sqlite": ["NAME"],
    "postgresql": ["USER", "PASSWORD", "HOST", "NAME"],
    "mysql": ["USER", "PASSWORD", "HOST", "NAME"],
    "mssql": ["USER", "PASSWORD", "HOST", "NAME", "DRIVER"],
    "oracle": ["USER", "PASSWORD", "HOST", "NAME"],
}

# Connection string templates for supported databases
CONNECTION_STRINGS = {
    "sqlite": "sqlite+aiosqlite:///{NAME}",
    "postgresql": "postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}/{NAME}",
    "mysql": "mysql+aiomysql://{USER}:{PASSWORD}@{HOST}/{NAME}",
    "mssql": "mssql+aioodbc://{USER}:{PASSWORD}@{HOST}/{NAME}?driver={DRIVER}",
    "oracle": "oracle+oracledb://{USER}:{PASSWORD}@{HOST}/{NAME}"
}

# Apply patches to ensure connection management works as expected
def patch_async_connection_init():
    original_init = AsyncConnection.__init__

    def connection_init_hook(connection_self, *args, **kwargs):
        weakref.finalize(connection_self, lambda: None)  # Ensures clean-up of AsyncConnection
        return original_init(connection_self, *args, **kwargs)

    AsyncConnection.__init__ = connection_init_hook

""" Builds a connection string for a given database type and environment configuration.

Args:
    db_type (str): The type of database (e.g., 'sqlite', 'postgresql').
    env (dict): A dictionary of environment variables for database configuration.

Returns:
    str: A formatted connection string for the specified database.
"""
def _build_connection_string(db_type, env):
    db_type = db_type.lower()
    _check_required_fields(env, db_type)
    return CONNECTION_STRINGS[db_type].format(**env)

""" Validates the presence of required fields in the environment configuration.

Args:
    env (dict): A dictionary containing environment variables.
    db_type (str): The type of database to validate fields for.

Raises:
    KeyError: If required fields are missing or empty.
"""
def _check_required_fields(env, db_type):
    for field in REQUIRED_FIELDS[db_type]:
        if not env.get(field) or not env[field].strip():
            error_message = f"Missing or empty required field: {field} for {db_type.capitalize()}"
            logger.error(error_message)
            raise KeyError(error_message)

# Apply patches to ensure connection management works as expected
patch_async_connection_init()

"""Manages asynchronous database engine connections."""
class EngineManager:

    """ Initializes the EngineManager class.

        Sets up thread safety and patches `aioodbc` connections for tracking.
        """
    def __init__(self):
        self._engines = {}
        self._lock = Lock()
        self._all_aioodbc_connections = []
        self._patch_aioodbc_connect()

    """ Patches aioodbc.connect to track active AioODBC connections."""
    def _patch_aioodbc_connect(self):
        original_aioodbc_connect = aioodbc.connect
        async def patched_aioodbc_connect(*args, **kwargs):
            conn = await original_aioodbc_connect(*args, **kwargs)
            self._all_aioodbc_connections.append(conn) # Track connections for clean-up
            return conn

        aioodbc.connect = patched_aioodbc_connect

    """ Retrieves or creates an asynchronous database engine.

        Args:
            env_file_name (str, optional): Path to an environment configuration file.
                                           Defaults to ".env".

        Returns:
            sqlalchemy.ext.asyncio.AsyncEngine: An asynchronous SQLAlchemy engine.
        """
    def get_engine(self, env_file_name=None):
        env_file = env_file_name or ".env"
        if env_file not in self._engines:
            with self._lock: # Thread safety for engine creation
                if env_file not in self._engines:
                    env = dotenv_values(env_file)

                    db_type = env.get("DB_TYPE").lower()
                    if not db_type or db_type not in REQUIRED_FIELDS:
                        if not db_type:
                            error_message = "Missing required environment variable: DB_TYPE"
                        else:
                            error_message = f"Unsupported database type: {db_type}. Supported types are: {', '.join(REQUIRED_FIELDS.keys())}"
                        logger.error(error_message)
                        raise KeyError(error_message)
                    try:
                        connection_string = _build_connection_string(db_type, env)
                        logger.info(f"Creating engine for {db_type}...")
                        self._engines[env_file] = create_async_engine(connection_string)
                    except KeyError as e:
                        logger.error(f"Error: {e}")
                        raise
                    except Exception as e:
                        logger.error(f"Failed to create engine: {e}")
                        raise
        return self._engines[env_file]

    """ Establishes an asynchronous database connection.

        Args:
            env_file_name (str, optional): Path to an environment configuration file.

        Returns:
            sqlalchemy.ext.asyncio.AsyncConnection: An active asynchronous database connection.
        """
    async def get_db_connection(self, env_file_name=None):
        engine = self.get_engine(env_file_name)
        try:
            conn = await engine.connect()
            return conn
        except sqlalchemy.exc.OperationalError as e:
            logger.error(f"Operational Error: {e}")
            raise
        except sqlalchemy.exc.ProgrammingError as e:
            logger.error(f"Programming Error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            raise

    """ Closes all active database engines and lingering connections."""
    async def close_engines(self):
        for env_file, engine in self._engines.items():
            logger.info(f"Disposing engine for: {env_file}")
            await engine.dispose()
        self._engines.clear()

