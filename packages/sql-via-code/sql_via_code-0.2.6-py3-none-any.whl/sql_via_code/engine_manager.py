from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from .logger_config import logger
from dotenv import dotenv_values
from threading import Lock
import sqlalchemy
import gc
import asyncio
import weakref
import aioodbc

class EngineManager:
    REQUIRED_FIELDS = {
        "sqlite": ["NAME"],
        "postgresql": ["USER", "PASSWORD", "HOST", "NAME"],
        "mysql": ["USER", "PASSWORD", "HOST", "NAME"],
        "mssql": ["USER", "PASSWORD", "HOST", "NAME", "DRIVER"],
        "oracle": ["USER", "PASSWORD", "HOST", "NAME"],
    }

    def __init__(self):
        self._engines = {}
        self._lock = Lock()

        # Monkey-patch for AsyncConnection
        self._patch_async_connection_init()
        self._all_aioodbc_connections = []
        self._patch_aioodbc_connect()

    def _patch_async_connection_init(self):
        original_init = AsyncConnection.__init__

        def connection_init_hook(connection_self, *args, **kwargs):
            print(f"🔵 Connection opened: {connection_self}")
            weakref.finalize(connection_self, lambda: print(f"🟢 Connection closed (finalized): {connection_self}"))
            return original_init(connection_self, *args, **kwargs)

        AsyncConnection.__init__ = connection_init_hook

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

                    db_type = env.get("DB_TYPE")
                    if not db_type:
                        error_message = "Missing required environment variable: DB_TYPE"
                        logger.error(error_message)
                        raise KeyError(error_message)
                    try:
                        connection_string = self._build_connection_string(db_type, env)
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

    def _build_connection_string(self, db_type, env):
        db_type = db_type.lower()
        if db_type not in self.REQUIRED_FIELDS:
            error_message = f"Unsupported database type: {db_type}. Supported types are: {', '.join(self.REQUIRED_FIELDS.keys())}"
            logger.error(error_message)
            raise ValueError(error_message)
        self._check_required_fields(env, db_type)

        connection_func_name = f"_{db_type}_connection"
        connection_func = getattr(self, connection_func_name, None)

        if callable(connection_func):
            return connection_func(env)
        else:
            error_message = f"Connection function for {db_type} is not implemented."
            logger.error(error_message)
            raise NotImplementedError(error_message)

    def _check_required_fields(self, env, db_type):
        for field in self.REQUIRED_FIELDS[db_type]:
            if not env.get(field) or not env[field].strip():
                error_message = f"Missing or empty required field: {field} for {db_type.capitalize()}"
                logger.error(error_message)
                raise KeyError(error_message)

    def _sqlite_connection(self, env):
        self._check_required_fields(env, "sqlite")
        return f"sqlite+aiosqlite:///{env['NAME']}"

    def _postgresql_connection(self, env):
        self._check_required_fields(env, "postgresql")
        return f"postgresql+asyncpg://{env['USER']}:{env['PASSWORD']}@{env['HOST']}/{env['NAME']}"

    def _mysql_connection(self, env):
        self._check_required_fields(env, "mysql")
        return f"mysql+aiomysql://{env['USER']}:{env['PASSWORD']}@{env['HOST']}/{env['NAME']}"

    def _mssql_connection(self, env):
        self._check_required_fields(env, "mssql")
        return f"mssql+aioodbc://{env['USER']}:{env['PASSWORD']}@{env['HOST']}/{env['NAME']}?driver={env['DRIVER']}"

    def _oracle_connection(self, env):
        self._check_required_fields(env, "oracle")
        return f"oracle+oracledb://{env['USER']}:{env['PASSWORD']}@{env['HOST']}/{env['NAME']}"

    async def close_engines(self):
        """
        Closes all active database engines and attempts to forcibly close lingering connections.
        """
        for env_file, engine in self._engines.items():
            logger.info(f"Disposing engine for: {env_file}")
            await engine.dispose()

        self._engines.clear()

        # Force close all AsyncConnection (SQLAlchemy) lingering connections
        await self.force_close_sqlalchemy_connections()

        # Force close all aioodbc connections tracked
        await self.force_close_aioodbc_connections()

        logger.info("✅ Cleanup complete.")

    async def force_close_sqlalchemy_connections(self):
        """
        Forcefully close lingering AsyncConnection objects from SQLAlchemy still present in memory.
        """
        gc.collect()
        open_connections = [obj for obj in gc.get_objects() if isinstance(obj, AsyncConnection)]
        if open_connections:
            logger.warning(f"⚠️  Found {len(open_connections)} lingering SQLAlchemy connections. Forcing close...")
            for conn in open_connections:
                try:
                    if not conn.closed:
                        await conn.close()
                        logger.warning(f"🔴 Forced close for lingering SQLAlchemy connection: {conn}")
                except Exception as e:
                    logger.error(f"❌ Failed to close lingering SQLAlchemy connection: {e}")
        else:
            logger.info("✅ No lingering SQLAlchemy connections found.")

    async def force_close_aioodbc_connections(self):
        """
        Forcefully close all tracked aioodbc connections.
        """
        closed_count = 0
        tasks = []  # רשימת משימות לסגירה

        for conn in self._all_aioodbc_connections:
            try:
                if not conn.closed:
                    tasks.append(asyncio.create_task(conn.close()))
                    closed_count += 1
                    logger.warning(f"🔴 Scheduled close for lingering aioodbc connection: {conn}")
            except Exception as e:
                logger.error(f"❌ Failed to schedule close for aioodbc connection: {e}")

        # חכה שכל המשימות יושלמו
        await asyncio.gather(*tasks, return_exceptions=True)
        self._all_aioodbc_connections.clear()

        if closed_count == 0:
            logger.info("✅ No lingering aioodbc connections found.")
        else:
            logger.warning(f"⚠️  Closed {closed_count} lingering aioodbc connections.")

