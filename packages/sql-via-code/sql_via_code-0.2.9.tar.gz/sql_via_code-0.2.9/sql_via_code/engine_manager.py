from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from patches import patch_async_connection_init
from .logger_config import logger
from dotenv import dotenv_values
from threading import Lock
import sqlalchemy
import weakref
import aioodbc

REQUIRED_FIELDS = {
    "sqlite": ["NAME"],
    "postgresql": ["USER", "PASSWORD", "HOST", "NAME"],
    "mysql": ["USER", "PASSWORD", "HOST", "NAME"],
    "mssql": ["USER", "PASSWORD", "HOST", "NAME", "DRIVER"],
    "oracle": ["USER", "PASSWORD", "HOST", "NAME"],
}

CONNECTION_STRINGS = {
    "sqlite": "sqlite+aiosqlite:///{NAME}",
    "postgresql": "postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}/{NAME}",
    "mysql": "mysql+aiomysql://{USER}:{PASSWORD}@{HOST}/{NAME}",
    "mssql": "mssql+aioodbc://{USER}:{PASSWORD}@{HOST}/{NAME}?driver={DRIVER}",
    "oracle": "oracle+oracledb://{USER}:{PASSWORD}@{HOST}/{NAME}"
}

patch_async_connection_init()

def _build_connection_string(db_type, env):
    db_type = db_type.lower()
    _check_required_fields(env, db_type)
    return CONNECTION_STRINGS[db_type].format(**env)

def _check_required_fields(env, db_type):
    for field in REQUIRED_FIELDS[db_type]:
        if not env.get(field) or not env[field].strip():
            error_message = f"Missing or empty required field: {field} for {db_type.capitalize()}"
            logger.error(error_message)
            raise KeyError(error_message)

class EngineManager:

    def __init__(self):
        self._engines = {}
        self._lock = Lock()
        self._all_aioodbc_connections = []
        self._patch_aioodbc_connect()

    def _patch_aioodbc_connect(self):
        original_aioodbc_connect = aioodbc.connect
        async def patched_aioodbc_connect(*args, **kwargs):
            conn = await original_aioodbc_connect(*args, **kwargs)
            self._all_aioodbc_connections.append(conn)
            return conn

        aioodbc.connect = patched_aioodbc_connect

    def get_engine(self, env_file_name=None):
        env_file = env_file_name or ".env"
        if env_file not in self._engines:
            with self._lock:
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

    async def connect_db(self, env_file_name=None):
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

    async def close_engines(self):
        """
        Closes all active database engines and attempts to forcibly close lingering connections.
        """
        for env_file, engine in self._engines.items():
            logger.info(f"Disposing engine for: {env_file}")
            await engine.dispose()
        self._engines.clear()

