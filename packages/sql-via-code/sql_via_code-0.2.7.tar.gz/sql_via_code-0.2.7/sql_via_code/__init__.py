# Import the functions you want to expose
from .sql_via_code import get_query_from_db, exec_procedure_from_db, backup_table , get_query_from_file, EngineManager

_engine_manager = EngineManager()

""" Exposes the dispose_engines method of EngineManager.
    Closes all active database engines synchronously.
"""
def close_engines():
    import asyncio
    asyncio.run(_engine_manager.close_engines())

# Define the public API of the package
__all__ = ["get_query_from_db", "exec_procedure_from_db", "backup_table" , "get_query_from_file" , "close_engines"]
