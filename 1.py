import oracledb

# Replace with your own credentials and database details
username = 'system'
password = 'Dominos123'
dsn = '192.168.0.196:1521/XE'

# Create a connection
connection = oracledb.connect(user=username, password=password, dsn=dsn)

print("Successfully connected to Oracle Database")

# Don't forget to close the connection
connection.close()


import oracledb
try:
            # Build connection string
            connection_string = f"oracle://{username}:{password}@{server_name}/{database_name}"
            # connection_string = f"oracle://{username}:{password}@{server_name}"


            # Connect
            connection = oracledb.connect(connection_string)

            # Execute test query
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM DUAL")