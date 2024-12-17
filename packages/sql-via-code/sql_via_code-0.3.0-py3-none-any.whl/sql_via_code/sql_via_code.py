from sql_via_code.engine_manager import EngineManager
from sql_via_code.logger_config import logger
from datetime import datetime
from sqlalchemy import text
import pandas as pd
import sqlalchemy
import aiofiles
import asyncio
import os

engine_manager = EngineManager()

"""
    Converts SQLAlchemy query results into a pandas DataFrame.

    Args:
        query_output (ResultProxy): SQLAlchemy query output.

    Returns:
        pd.DataFrame: DataFrame containing the query results.
    """
async def format_to_df(query_output):
    try:
        rows = await query_output.fetchall()
        columns_name = query_output.keys()
        return pd.DataFrame(rows, columns=columns_name)
    except Exception as e:
        logger.error(f"Error converting query output to DataFrame: {e}")
        raise

""" Executes a SQL query or stored procedure asynchronously, handles errors, and formats the result as a DataFrame.

    Args:
        query_or_procedure (str): The query string or stored procedure name.
        table_to_backup (str): Table name for backup before executing the query.
        env_file_name (str, optional): The environment file for DB configuration.
        params (dict, optional): Parameters to pass to the query or procedure.
        is_query (bool, optional): If False, treats as procedure name. Default is True.

    Returns:
        pd.DataFrame: The result of the query or procedure formatted into a DataFrame, or None if no rows are returned.
    """
async def _execute_db_query_or_procedure(query_or_procedure , table_to_backup, env_file_name=None, params=None, is_query=True):
    kind = "query" if is_query else "procedure"
    conn = None
    try:
        conn = await engine_manager.connect_db(env_file_name)
        await backup_table(table_to_backup, conn)

        if not is_query:
            params_string = build_procedure_param_string(params)
            output = await conn.execute(text(f"EXEC {query_or_procedure} {params_string}"), params)
        else:
            output = await conn.execute(text(query_or_procedure), params)
            await conn.commit()

        if not output.returns_rows:
            return None
        return await format_to_df(output)
    except sqlalchemy.exc.SQLAlchemyError as e:
        error_message = f"Failed to execute {kind}:\n{e}"
        logger.error(error_message)
        raise ValueError(f"An error occurred while executing the {kind}. Please check your syntax or database connection.") from e
    finally:
        if conn:
            await conn.close()


"""Executes a SQL query and optionally backs up a specified table.

Args:
    query (str): The SQL query string to execute.
    table_to_backup (str or None): The name of the table to back up. Pass `None` to skip backup.
    env_file_name (str, optional): Path to the `.env` file with database credentials. Defaults to `None`.
    params (dict, optional): Parameters to pass to the query.

Returns:
    pd.DataFrame: DataFrame containing the query results.

Raises:
    ValueError: If a database error occurs during query execution.
"""
async def get_query_from_db(query , table_to_backup , env_file_name = None , params = None):
    return await _execute_db_query_or_procedure(query, table_to_backup, env_file_name, params, is_query=True)

"""Executes a stored procedure and optionally backs up a specified table.

Args:
    procedure_name (str): The name of the stored procedure to execute.
    table_to_backup (str or None): The name of the table to back up. Pass `None` to skip backup.
    env_file_name (str, optional): Path to the `.env` file with database credentials. Defaults to `None`.
    params (dict, optional): Parameters to pass to the stored procedure.

Returns:
    pd.DataFrame: DataFrame containing the procedure's output.

Raises:
    ValueError: If a database error occurs during procedure execution.
"""
async def exec_procedure_from_db(procedure_name , table_to_backup , env_file_name = None , params = None):
    return await _execute_db_query_or_procedure(procedure_name, table_to_backup, env_file_name, params, is_query=False)

"""Builds a formatted string for stored procedure parameters.

Args:
    params (dict): Dictionary containing parameter keys and values.

Returns:
    str: A formatted string for procedure parameters.
"""
def build_procedure_param_string(params):
    if not params: # No parameters to process
        return ""
    return ", ".join([f"@{key} = :{key}" for key in params.keys()]) # Build the parameter string


"""Backs up a table's data to a Markdown file.

Args:
    table_to_backup (str or None): The name of the table to back up. Pass `None` to skip backup.
    conn (AsyncConnection): An active database connection.

Raises:
    ValueError: If `table_to_backup` is an empty string.
    Exception: If an error occurs during the backup process.
"""
async def backup_table(table_to_backup , conn):
    if table_to_backup == "":
        raise ValueError("Parameter 'table_to_backup' cannot be an empty string.")
    elif table_to_backup is not None:
        backup_dir_name = "tables_backup"
        os.makedirs(backup_dir_name, exist_ok=True)

        backup_query = f"SELECT * FROM {table_to_backup}"
        result = await conn.execute(text(backup_query))
        rows = result.fetchall()
        columns = result.keys()
        backup_df = pd.DataFrame(rows, columns=columns)
        backup_filename = os.path.join(backup_dir_name, f"{table_to_backup}_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md")

        try:
            async with aiofiles.open(backup_filename, 'w') as file:
                await file.write(backup_df.to_markdown(index=False))
            logger.info(f"Table '{table_to_backup}' backed up successfully as {backup_filename}")
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            raise

""" Reads an SQL query from a file, executes it, and optionally backs up a table.

    Args:
        file_path (str): Path to the file containing the SQL query.
        table_to_backup (str): Name of the table to back up before query execution.
        env_file_name (str, optional): Path to the environment file for database connection. Defaults to None.
        params (dict or tuple, optional): Parameters to bind to the SQL query. Defaults to None.

    Returns:
        Any: The result of the executed query.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty.
        IOError: If there is an issue reading the file or executing the query.
    """
def get_query_from_file(file_path, table_to_backup, env_file_name=None, params=None):
    if not os.path.exists(file_path):
        error_message = f"File '{file_path}' not found."
        logger.error(error_message)
        raise FileNotFoundError(error_message)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            query = file.read().strip()
            if not query:
                error_message = f"The file '{file_path}' is empty."
                logger.error(error_message)
                raise ValueError(error_message)
            return asyncio.run(get_query_from_db(query, table_to_backup , env_file_name , params))
    except ValueError:  # Handle explicit empty file exception
        raise
    except Exception as e:
        error_message = f"Failed to read query from file '{file_path}': {e}"
        logger.error(error_message)
        raise IOError(error_message)

""" Closes all active database engines synchronously. """
def close_engines():
    asyncio.run(engine_manager.close_engines())

