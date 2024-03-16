import pyodbc

class CreateDatabaseTable:
    
    def __init__(self, server, database_name, username, password, driver, port, tabels):
        self.server = server
        self.database_name = database_name
        self.username = username
        self.password = password
        self.driver = driver
        self.port = port
        self.tabels = tabels

    def create_database(self):
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
        
