from sqlalchemy import create_engine
import pandas as pd
class ReadCsv:
    def __init__(self, server, database_name, username, password, driver, port, dataset_path,file_names, tabels,file_to_table_map):
        self.server = server
        self.database_name = database_name
        self.username = username
        self.password = password
        self.driver = driver
        self.port = port
        self.tabels = tabels
        self.dataset_path = dataset_path.replace('\\','/')  #convert the path to unicode to avoid error
        self.file_names = file_names
        self.file_to_table_map = file_to_table_map
        self.engine = None  # Placeholder for the engine


    def alchemy_connection(self):
        ### Insert the data into SQL Server
        # Your connection string to insert data line by line using sqlalchemy
        connection_string_alchemy = f'mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database_name}?driver={self.driver.replace(" ", "+")}&TrustServerCertificate=yes'
        self.engine = create_engine(connection_string_alchemy)

    def read_csv_to_sql(self):
        self.alchemy_connection()
        if self.engine is None:
            print("Engine has not been initialized. Call alchemy_connection first.")
            return
        
        tabels_dic = self.tabels
        
        column_names = {}
        for file_name in self.file_names:
            # Determine the corresponding table name from the file name
            table_name = self.file_to_table_map.get(file_name)
            
            if table_name:
                # If there's a corresponding table name, proceed to extract and map column names
                columns_info = tabels_dic.get(table_name, [])
                table_columns = [col[0] for col in columns_info]
                column_names[file_name] = table_columns


        # Dictionary to store each DataFrame, using a modified file name as the key
        dataframes = {}

        for file_name in self.file_names:
            # Path to the current CSV file
            csv_path = f'{self.dataset_path}/{file_name}'
            
            # Read the first row to determine the number of columns in the CSV
            with open(csv_path, 'r') as csvfile:
                first_line = csvfile.readline()
                num_columns_in_csv = len(first_line.split(','))
            
            # Determine the column names to use based on the number of columns in the CSV
            if num_columns_in_csv <= len(column_names[file_name]):
                cols_to_use = column_names[file_name][:num_columns_in_csv]
            else:
                # If the CSV has more columns than expected, you could handle this case as needed.
                # For simplicity, this example will still use the defined columns up to the length of `column_names[file_name]`
                cols_to_use = column_names[file_name]
            
            # Now, read the CSV with the dynamically determined columns
            df = pd.read_csv(csv_path, names=cols_to_use, header=0)
            table_name = self.file_to_table_map[file_name]
            # Save the DataFrame to the SQL table
            df.to_sql(name=table_name, con=self.engine, if_exists='replace', index=False)
            print(f'Data Copied to {table_name} in SQL')
            
            # Removing '.csv' from file_name to use as dictionary key
            name_key = file_name.replace('.csv', '')
            
            # Storing the DataFrame in the dictionary
            dataframes[name_key] = df
           
        


