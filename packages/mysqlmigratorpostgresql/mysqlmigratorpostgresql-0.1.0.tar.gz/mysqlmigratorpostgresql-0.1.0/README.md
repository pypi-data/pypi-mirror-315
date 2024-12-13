# MysqlMigratorPostgreSQL
```python
pip install mysqlmigratorpostgresql
```

## Introduction

**MysqlMigratorPostgreSQL** is a Python library designed to simplify the migration of entire databases from **MySQL** to **PostgreSQL**. This tool is ideal for software engineers seeking an automated solution to transfer data and table structures between these two relational database management systems.

The library offers:
- Easy connection to MySQL and PostgreSQL servers.
- Automated table migration, including columns and data types.
- Efficient connection and error handling.
- A modular and extensible design.

---

## Reserved Word Dictionary

During migration, certain data types in **MySQL** do not have an exact equivalent in **PostgreSQL**. Below is a summary of the conversions performed by the library:

| **MySQL Type**         | **PostgreSQL Type**   | **Description**                                                                |
|------------------------|------------------------|---------------------------------------------------------------------------------|
| `INT`                 | `INTEGER`             | Fixed-size integers.                                                           |
| `VARCHAR(n)`          | `TEXT`                | PostgreSQL does not require strict text limits.                                |
| `TEXT`                | `TEXT`                | Maintains the same type for long text fields.                                  |
| `FLOAT`               | `REAL`                | Floating-point values.                                                         |
| `DOUBLE`              | `DOUBLE PRECISION`    | Higher precision floating-point values in PostgreSQL.                          |
| `DATE`                | `DATE`                | Standard date in `YYYY-MM-DD` format.                                          |
| `DATETIME`            | `TIMESTAMP`           | Date and time with timezone.                                                   |
| `TINYINT(1)`          | `BOOLEAN`             | Interpreted as a logical value (`TRUE` or `FALSE`).                            |
| `ENUM`                | `TEXT`                | Converted to text since PostgreSQL does not directly support the `ENUM` type.  |

---

## Code Details

### **General Structure**

The library follows a modular approach. Each functionality is defined in a specific file:
- **`connect_mysql.py`**: Handles connection to a MySQL server.
- **`connect_postgresql.py`**: Handles connection to a PostgreSQL server.
- **`migrator.py`**: Orchestrates the migration of tables and data.

---

### **Changes in Data Types**

The logic to convert MySQL data types to PostgreSQL is located in `migrator.py`. Here is the key code fragment with explanation:

```python
# Data type mapping
if "int" in column_type:
    postgres_type = "INTEGER"
elif "varchar" in column_type or "text" in column_type:
    postgres_type = "TEXT"
elif "float" in column_type or "double" in column_type:
    postgres_type = "REAL"
elif "date" in column_type:
    postgres_type = "DATE"
elif "tinyint(1)" in column_type:
    postgres_type = "BOOLEAN"
else:
    postgres_type = "TEXT"  # Default type if no specific mapping is found
```

---

## Example Code

Here is a functional example demonstrating how to use the library to migrate all tables from a MySQL database to PostgreSQL:

```python
from mysqlmigratorpostgresql import MysqlMigratorPostgreSQL

# Instantiate the migrator
migrator = MysqlMigratorPostgreSQL()

# Connect to MySQL
migrator.connect_mysql(
    host="localhost",
    port=3306,  # Default MySQL port
    user="root",
    password="password",  # Replace with your password
    database="databases_name"
)

# Connect to PostgreSQL
migrator.connect_postgresql(
    host="localhost",
    port=5432,  # Default PostgreSQL port
    user="postgres",
    password="password",  # Replace with your password
    database="databases_name"
)

# Migrate all tables
migrator.migrate_all()

# Close connections
migrator.close_connections()
