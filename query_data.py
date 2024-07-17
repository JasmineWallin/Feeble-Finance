######################
# query_data.py      #
#                    #
# functions that     #
# interact with the  #
# MS SQL data to     # 
# return data for    #
# the GUI.           #
######################

###IMPORTS###
import random #TODO delete probably
from pymssql_sess import conn
import xlsxwriter

# check if the SQL dtabase exists and if it does create it
def create_database():
    SQL_QUERY = """
    SELECT * FROM finance_table
    """
    # defining Cursor object
    cursor = conn.cursor()

    # if finance_table exists
    try:
        cursor.execute(SQL_QUERY)
    # if finance_table doesnt exist 
    except:
        print("making a new database")
        sql ='''CREATE TABLE finance_table(
        item TEXT,
        monthly_expense TEXT,
        start_date TEXT,
        end_date TEXT,
        type TEXT,
        curr TEXT
        )'''
        cursor.execute(sql)
        conn.commit()
    # closing everything
    cursor.close()

# get data for graph from queried data
def graph_data():
    return [random.random() for i in range(10)]

# get data for chart from queried data
def chart_data():
    pass

# make excel file from queried data 
def make_excel():
    ''' 
    input: none
    output: finance_data.xlsx filled with data from sql database, 
            with column headers: item, monthly expense, start date, end date, type, curr
            - all columns are string/chars type
    '''
    print('making excel...')
    SQL_QUERY = """
    SELECT * FROM finance_table
    """
    # defining Cursor object
    cursor = conn.cursor()

    # trying to execute query
    try:
        # Executing the SQL command
        cursor.execute(SQL_QUERY)
       
        # initialising the xlsx workbook to write into
        workbook = xlsxwriter.Workbook('finance_data.xlsx')
        worksheet = workbook.add_worksheet()
        # writing the column headers
        worksheet.write('A1', 'item')
        worksheet.write('B1', 'monthly expense')
        worksheet.write('C1', 'start date')
        worksheet.write('D1', 'end date')
        worksheet.write('E1', 'type')
        worksheet.write('F1', 'current?')

        # getting all items from the queried finance_table
        all = cursor.fetchall()
        curr_row = 2
        # writing items into the xlsx file by col header 
        for r in all: 
            worksheet.write('A' + str(curr_row), r['item'])
            worksheet.write('B' + str(curr_row), r['monthly_expense'])
            worksheet.write('C' + str(curr_row), r['start_date'])
            worksheet.write('D' + str(curr_row), r['end_date'])
            worksheet.write('E' + str(curr_row), r['type'])
            worksheet.write('F' + str(curr_row), r['curr'])
            curr_row += 1

        # closing the xlsx workbook
        workbook.close()

    except:
        # Rolling back in case of error
        conn.rollback()

    # closing everything
    cursor.close()
    
# input data into the SQL server 
def input_query(item, monthlyexp, start, end, type, curr): 
    '''
    inputs: 
        item - string : the name of the financial expense
        monthlyexp - string : the integer only string that represents the monthly cost
        start - char[10] : date in format MM/DD/YYYY that represents when expense started
        end - char[10] : date in format MM/DD/YYYY that represents when expense ended (if '' then its current)
        type - string : either 'needs', 'fufillment', 'social', or 'extra'
        curr - string : 'yes' or 'no' if its a current item
    output:
        return_out - int : 0/1 based on if input_query was successful
    '''
    return_out = 1

    SQL_QUERY = "INSERT INTO finance_table (item, monthly_expense, start_date, end_date, type, curr) VALUES ('" + str(item) + "', '" + str(monthlyexp) + "', '" + str(start) + "', '" + str(end) + "', '" + str(type) + "', '" + str(curr) + "')"
   
    cursor = conn.cursor()

    # trying to execute query
    try:
        cursor.execute(SQL_QUERY)
        conn.commit() 

    # failure
    except:
        # Rolling back in case of error
        conn.rollback()
        return_out = 0

    # closing everything
    cursor.close()

    return return_out

# delete something from SQL server
def delete_query_item():
    #TODO
    pass

# close SQL query connection
def finish():
    conn.close()