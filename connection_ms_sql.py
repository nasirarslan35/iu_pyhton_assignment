import pyodbc

class CreateDatabaseTable:
    """
    A class to manage the creation of a database and its tables in Microsft SQL Server using pyodbc.

    Attributes:
        server (str): The server name or IP address where the SQL Server instance is hosted.
        database_name (str): The name of the database to create.
        username (str): The username for SQL Server authentication.
        password (str): The password for SQL Server authentication.
        driver (str): The ODBC driver used for the connection.
        port (int): The port number for the SQL Server instance.
        tables (dict): A dictionary where keys are table names and values are lists of tuples,
                       each tuple containing the column name and data type.
    
    Methods:
        create_database(): Attempts to create the database specified in the `database_name` attribute.
                           Prints a success message or indicates if the database already exists.
                           
        create_tables(): Attempts to create tables specified in the `tables` attribute within the
                         previously created database. Prints a success message for each table created
                         or indicates if a table already exists.
    """
    
    def __init__(self, server, database_name, username, password, driver, port, tabels):
        """
        Initializes the CreateDatabaseTable class with server details, authentication credentials,
        and table definitions.
        """
        self.server = server
        self.database_name = database_name
        self.username = username
        self.password = password
        self.driver = driver
        self.port = port
        self.tabels = tabels

    def create_database(self):
        """
        Attempts to create the database on the server. If the database already exists,
        it catches the exception and prints a message.
        """
        # Connection string without specifying the database
        initial_conn_str = f'DRIVER={{{self.driver}}};SERVER={self.server};UID={self.username};PWD={self.password};Port={self.port};TrustServerCertificate=yes;'

        # Attempt to create the database
        try:
            with pyodbc.connect(initial_conn_str, autocommit=True) as conn:
                with conn.cursor() as cursor:
                    try:
                        cursor.execute(f"CREATE DATABASE {self.database_name}")
                        print(f"Database '{self.database_name}' created successfully.")
                    except Exception as d:
                        print(f'Database "{self.database_name}" already exist')
        except Exception as e:
            print(f'Connection or another error occurred: {e}')
            
    def create_tables(self): 
        """
        Connects to the database and attempts to create the tables as defined in the 'tables' attribute.
        If a table already exists, it catches the exception and prints a message.
        """   
        # Connection string updated with database name after creation of database
        conn_str = f'DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database_name};UID={self.username};PWD={self.password};Port={self.port};TrustServerCertificate=yes;'
        
        # Definitions for tables
        tabels = self.tabels

        try:
            with pyodbc.connect(conn_str, autocommit=True) as conn:
                    with conn.cursor() as cursor:
                            for table_name, columns in tabels.items():
                                try:
                                    create_table_command = f"CREATE TABLE {table_name} ("
                                    col_definitions = [f"[{col_name}] {data_type}" for col_name, data_type in columns]
                                    create_table_command += ", ".join(col_definitions)
                                    create_table_command += ")"
                                    
                                    # Execute the CREATE TABLE command
                                    cursor.execute(create_table_command)
                                    print(f"Table '{table_name}' created successfully.")
                                    
                                except Exception as d:
                                    print(f"Table '{table_name}' Already Present: {d}")
        except Exception as e:
            print(f"An connection error occurred while creating tables: {e}")
        
