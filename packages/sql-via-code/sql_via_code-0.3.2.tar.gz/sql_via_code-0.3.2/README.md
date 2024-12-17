# sql_via_code

## Overview

sql_via_code is a library for executing SQL queries, stored procedures, table backups, and reading queries from files, all with a clean and simple interface.

---

## Features

1. **Query Execution**: Execute SQL queries and fetch the results as a pandas DataFrame.
2. **Stored Procedure Execution**: Run stored procedures with input parameters.
3. **Table Backup**: Automatically back up a specified table's data before executing a query or procedure.
4. **Query from File**: Read and execute SQL queries from external files to improve maintainability.  
5. **Engine Management**: Close all active database engines cleanly using `close_engines`.

---

## Functions

### get_query_from_db
Executes a SQL query and optionally backs up a table.

#### Parameters:
- query *(str)*: SQL query to execute.
- table_to_backup *(str or None)*: Table to back up. Pass None to skip the backup.
- env_file_name *(str, optional)*: Path to the .env file for database credentials (default is .env).
- params *(dict, optional)*: Query parameters.

#### Returns:
- A pandas.DataFrame containing query results.

---

### exec_procedure_from_db
Executes a stored procedure and optionally backs up a table.

#### Parameters:
- procedure_name *(str)*: Name of the stored procedure.
- table_to_backup *(str or None)*: Table to back up. Pass None to skip the backup.
- env_file_name *(str, optional)*: Path to the .env file for database credentials (default is .env).
- params *(dict, optional)*: Procedure parameters.

#### Returns:
- A pandas.DataFrame containing procedure output.

---

### `get_query_from_file`
Reads and executes an SQL query from a file.

#### Parameters:
- `file_path` *(str)*: Path to the `.sql` or `.txt` file containing the query.
- `table_to_backup` *(str or None)*: Table to back up before executing the query. Pass `None` to skip the backup.
- `env_file_name` *(str, optional)*: Path to the `.env` file for database credentials.
- `params` *(tuple or dict, optional)*: Parameters to bind to the SQL query.

#### Returns:
- A `pandas.DataFrame` containing query results.

#### Example:
from sql_via_code import get_query_from_file

# Read and execute a query from a file
result_df = get_query_from_file("queries/select_employees.sql", table_to_backup="employees")
print(result_df)

---

### `close_engines`
Closes all active database engines.

**Important**:  
It is recommended to call this function at the **end of your program** to ensure that all database connections are closed properly and no resources are leaked.

#### Usage:
from sql_via_code import close_engines

# Close all active database engines
close_engines()

---

## Installation

To install the package and dependencies:

bash
pip install sql_via_code


---

## Dependencies

The project requires the following libraries:

- pandas==2.2.3
- SQLAlchemy==2.0.36
- python-dotenv==1.0.1
- pyodbc==5.2.0
- aiofiles==24.1.0
- tabulate==0.9.0
- asyncpg==0.30.0 *(for PostgreSQL)*
- aiomysql==0.2.0 *(for MySQL)*
- aiosqlite==0.20.0 *(for SQLite)*

---

## Environment Setup

Ensure you have a .env file in the root directory with the following database configuration:

plaintext
DB_TYPE=your_db_type
USER=your_username
PASSWORD=your_password
HOST=your_host
NAME=your_database_name
DRIVER=your_driver


Example .env file for MSSQL:

plaintext
DB_TYPE=mssql
USER=admin
PASSWORD=secretpassword
HOST=127.0.0.1
NAME=my_database
DRIVER=ODBC Driver 17 for SQL Server


Example .env file for SQLite:

plaintext
DB_TYPE=sqlite
NAME=example.db


---

## Usage Examples

### Example 1: Executing a Query with Backup

python
from sql_via_code import get_query_from_db

query = "SELECT * FROM employees"
result_df = await get_query_from_db(query, table_to_backup="employees")
print(result_df)


---

### Example 2: Executing a Stored Procedure

python
from sql_via_code import exec_procedure_from_db

procedure_name = "sp_get_employee_data"
params = {"department": "Sales"}
result_df = await exec_procedure_from_db(procedure_name, table_to_backup="employees", params=params)
print(result_df)


---

### Example 3: Reading Query from File

from sql_via_code import get_query_from_file, get_query_from_db, close_engines

query = get_query_from_file("queries/select_employees.sql", table_to_backup="employees")
result_df = get_query_from_db(query, table_to_backup="employees")
print(result_df)

# Final step: Close all engines
close_engines()

---

## Supported Databases

| Database    | DB_TYPE   | Required Fields                                    |
|-------------|-----------|----------------------------------------------------|
| SQLite      | sqlite    | NAME                                               |
| PostgreSQL  | postgresql| USER, PASSWORD, HOST, NAME                         |
| MySQL       | mysql     | USER, PASSWORD, HOST, NAME                         |
| MSSQL       | mssql     | USER, PASSWORD, HOST, NAME, DRIVER                 |
| Oracle      | oracle    | USER, PASSWORD, HOST, NAME                         |

---
