import os
import configparser
import cx_Oracle

def connect_to_sql_server():
    config = configparser.ConfigParser()
    config_file_path = "db_settings.ini"

    # Load config file
    _load_config(config, config_file_path)

    # Choose action: create new or load existing connection
    action = input("Create a new connection (new) or load existing (load): ")

    if action.lower() == "new":
        _create_new_connection(config, config_file_path)
    elif action.lower() == "load":
        _load_existing_connection(config)
    else:
        print(f"Invalid action: '{action}'. Please enter 'new' or 'load'.")


def _load_config(config, config_file_path):
    """Loads the config file."""
    if not os.path.exists(config_file_path):
        print("Config file not found. Creating new config file...")
        config["DEFAULT"] = {}
        with open(config_file_path, "w") as f:
            config.write(f)

    config.read(config_file_path)


def _create_new_connection(config, config_file_path):
    """Creates a new connection profile and saves it to the config file."""
    profile_name = input("Enter profile name: ")

    # Check for duplicate profile names
    if profile_name in config.sections():
        print(f"Profile name '{profile_name}' already exists.")
        return

    config[profile_name] = {}

    # Prompt for connection details
    server_name = input("Server Name: ")
    username = input("Username: ")
    password = input("Password: ")
    database_name = input("Database Name: ")
    schema = input("Schema (optional): ")

    # Determine connection type (SQL Server or Oracle)
    connection_type = input("Connection Type (sqlserver or oracle): ")

    # Validate connection details
    try:
        _validate_connection(connection_type, server_name, username, password, database_name)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Save connection details
    config[profile_name]["server_name"] = server_name
    config[profile_name]["username"] = username
    config[profile_name]["password"] = password
    config[profile_name]["database_name"] = database_name
    config[profile_name]["schema"] = schema
    config[profile_name]["connection_type"] = connection_type

    with open(config_file_path, "w") as f:
        config.write(f)

    print(f"Connection profile '{profile_name}' created successfully.")


def _load_existing_connection(config):
    """Lists available connections and allows the user to choose one."""
    available_connections = config.sections()

    if not available_connections:
        print("No connection profiles found.")
        return

    for i, profile in enumerate(available_connections):
        print(f"{i + 1}. {profile}")

    choice = input("Choose a connection profile (1-{} or q to quit): ".format(
        len(available_connections)
    ))

    if choice.lower() == "q":
        return

    try:
        index = int(choice) - 1
        if index < 0 or index >= len(available_connections):
            raise ValueError("Invalid choice.")
    except ValueError:
        print("Invalid choice.")
        return

    profile_name = available_connections[index]
    print(f"Loading connection profile: '{profile_name}'")


def _validate_connection(connection_type, server_name, username, password, database_name):
    """
    Validates the connection details for specific connection type.
    Currently supports SQL Server and Oracle.
    """
    if connection_type.lower() == "sqlserver":
        import pyodbc
        try:
            connection = pyodbc.connect(
                # f"DRIVER={{SQL Server Native Client 11.0}};SERVER={server_name};UID={username};PWD={password};DATABASE={database_name};"
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};UID={username};PWD={password};DATABASE={database_name};"

            )
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            connection.close()
        except Exception as e:
            raise ValueError(f"Connection failed: {e}")
    elif connection_type.lower() == "oracle":
        import cx_Oracle
        try:
            connection = cx_Oracle.connect(username, password, database_name)
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            connection.close()
        except Exception as e:
            raise ValueError(f"Connection failed: {e}")
    else:
        raise ValueError("Invalid connection type.")

    print("Connection successful!")

def connect_to_sql_server():
    config = configparser.ConfigParser()
    config_file_path = "db_settings.ini"

    # Load config file
    _load_config(config, config_file_path)

    # Welcome message and prompt
    print("Welcome to the database connection manager.")
    action = input("Would you like to open a saved connection (load) or create a new connection profile (new)? ").lower()

    if action == "load":
        _load_existing_connection(config)
    elif action == "new":
        _create_new_connection(config, config_file_path)
    else:
        print(f"Invalid action: '{action}'. Please enter 'load' or 'new'.")


connect_to_sql_server()


# TODO: Implement logic to use the loaded connection profile

