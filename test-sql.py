from pymssql_sess import conn

# query to get information from example_table
SQL_QUERY = """
SELECT * FROM example_table
"""

# query that is supposed to add information to example_table
#SQL_QUERY = """
#INSERT INTO example_table (age, name)
#VALUES ('100', 'fungus')
#"""

# defining Cursor object
cursor = conn.cursor()

# trying to execute query
try:
    # Executing the SQL command
    cursor.execute(SQL_QUERY)
    # Commit your changes in the database
    #conn.commit() # TODO you don't need this if you're just printing out values or fetching them.

    # for fetching query
    # getting all items from the queried example_table table
    all = cursor.fetchall()
    for r in all:
        print(f"{r['age']}\t{r['name']}")
except:
   # Rolling back in case of error
   conn.rollback()

# closing everything
cursor.close()
conn.close()
