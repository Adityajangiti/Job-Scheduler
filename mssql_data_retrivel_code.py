import pymssql
import pandas as pd
import time

start_time = time.time()


# Database connection details

server = 'server info'
database = 'database info'
username = 'your_username'
password = 'your_password'

# Establish a connection

conn = pymssql.connect(server=server, database=database, user=username, password=password)

cursor = conn.cursor()
print("Connected to server")

# List of SQL queries
queries = [
    '''
'''
]

# Executing each query 
for i, query in enumerate(queries):
    cursor.execute(query)
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    df['To order by Accep date'] = df['To order by Accep date'].dt.tz_localize(None)

    output_file = f"farmer_{i+1}.xlsx"
    print(f"Creating Excel file {output_file}...")
    df.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")

# Closing conn
cursor.close()
conn.close()

#time taken 
end_time = time.time()
print(f"Execution Time: {end_time - start_time} seconds")