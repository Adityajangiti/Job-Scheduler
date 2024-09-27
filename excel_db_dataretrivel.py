import pandas as pd
import psycopg2

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    host='your_host',
    port=5432,
    user='user_name',
    password='Passowrd',
    dbname='dbName'
)

cursor = connection.cursor()

# Read data from the Excel sheet
excel_file = f'Sample_data.xlsx'
excel_data = pd.read_excel(excel_file)

# Iterate through the Excel data and fetch data
for index, row in excel_data.iterrows():
    id_value = row['Origin_commodity']

    # sql_query=f"select * from company_code where report_profit_center='{id_value};"

    sql_query = f"""

    """

    cursor.execute(sql_query)
    result = cursor.fetchall()

    # fetched data to the DataFrame
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

    # Save the DataFrame to a new Excel
    output_file = f"op_{id_value}.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Results saved to {output_file}")

# Closing conn
cursor.close()
connection.close()