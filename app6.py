import pyodbc

# Connection details
server = 'KE-REPORTS-SERV\MSSQLSERVER01'
database = 'BataKenyaStores'
username = 'portalman'  
password = 'Cos-Link-Admin' 

# Connection string
connection_string = f"""
    Driver={{SQL Server}};
    Server={server};
    Database={database};
    UID={username};
    PWD={password};
"""

# Establishing the connection
try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful")
except pyodbc.Error as e:
    print("Error in connection:", e)

