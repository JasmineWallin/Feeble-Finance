from pymssql_sess import conn

# query to get information from example_table


#SQL_QUERY = """
#SELECT * FROM finance_table
#"""

# query that is supposed to add information to example_table
SQL_QUERY = ""
SQL_QUERY += "INSERT INTO finance_table (item, monthly_expense, start_date, end_date, type)"
SQL_QUERY += "VALUES ('fungus', '222', '12/14/2001', '', 'needs')"

# defining Cursor object
cursor = conn.cursor()

# trying to execute query
try:
    # Executing the SQL command
    cursor.execute(SQL_QUERY)

    # Commit your changes in the database
    conn.commit() # TODO you don't need this if you're just printing out values or fetching them.

    # for fetching query
    # getting all items from the queried example_table table
    #all = cursor.fetchall()
    #for r in all: #item, monthly_expense, start_date, end_date, type
    #    print(f"{r['item']}\t{r['monthly_expense']}\t{r['start_date']}\t{r['end_date']}\t{r['type']}")
except:
    print('fail')
    # Rolling back in case of error
    conn.rollback()

# closing everything
cursor.close()
conn.close()
