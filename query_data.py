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
from pymssql_sess import conn
import xlsxwriter
from datetime import datetime, date


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
    # if finance_table doesnt exist - make database
    except:
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

# get data for graph from MS SQL queried data
def graph_data(type):
    '''
    Output : (x_coords, y_coords)

        - x_coords : list - a list of strings that represent the x coordinates 
                    (dates in MM/DD/YYYY format) of a graph.
        - y_coords : list - a list the same length as x_coords, of integers that 
                    represent the y coordinates (amount of cumulative money 
                    spent on dates) of a graph.
    '''
    x_coords = []
    y_coords = []

    SQL_QUERY = """
    SELECT * FROM finance_table
    """
    # defining Cursor object
    cursor = conn.cursor()

    # trying to execute query
    try:
        # Executing the SQL command
        cursor.execute(SQL_QUERY)

        # getting all items from the queried finance_table
        all = cursor.fetchall()
        
        # making a dictionary with (key, value) as (start MM/DD/YYYY, $ amount)
        lst = {}
        for r in all: 
            # checking for correct type of line graph, if not general
            if (type == 'needs' and r['type'] != 'needs') or (type == 'fufillment' and r['type'] != 'fufillment') or (type == 'social' and r['type'] != 'social') or (type == 'extra' and r['type'] != 'extra'):
                # adding a dictionary definition so that outputs are all the same length
                if r['start_date'] not in lst:
                    lst[r['start_date']] = 0   
                if r['curr'] != 'yes':
                    if r['end_date'] not in lst:
                        lst[r['end_date']] = 0
                continue
            
            # adding to the coordinates if the right type
            if r['start_date'] not in lst:
                lst[r['start_date']] = float(r['monthly_expense'])
            else:
                lst[r['start_date']] += float(r['monthly_expense'])

            # if the monthly expense has an end date, make the monthly expense negative after the date
            if r['curr'] != 'yes':
                if r['end_date'] not in lst:
                    lst[r['end_date']] = 0 - float(r['monthly_expense'])
                else:
                    lst[r['end_date']] +=  (0 - float(r['monthly_expense']))
        
        # sorting the dictionary 
        sorted_dict = dict(sorted(lst.items(), key=lambda x: datetime.strptime(x[0], '%m/%d/%Y')))
        
        # going through sorted dictionary to make plot points
        curr_amount = 0 # current monthly spending
        for item in sorted_dict:
            curr_amount += sorted_dict[item]
            y_coords.append(curr_amount)
        
        x_coords = list(sorted_dict.keys())

    except:
        # Rolling back in case of error
        conn.rollback()

    # closing everything
    cursor.close()

    return (x_coords, y_coords)

# get monthly expense data for chart from queried data
def chart_data():
    '''
    Output : [needs, fufillment, social, extra]

        - needs : float - the float representation of the amount of money spent 
                this month for items of 'needs' type.
        - fufillment : float - the float representation of the amount of money
                        spent this month for items of 'fufillment' type.
        - social : float - the float representation of the amount of money spent
                    this month for items of the 'social' type.
        - extra : float - the float representation of the amount of money spent 
                this month for items of the 'extra' type.
    '''
    needs = 0.0
    fufillment = 0.0
    social = 0.0
    extra = 0.0

    SQL_QUERY = """
    SELECT * FROM finance_table
    """
    # defining Cursor object
    cursor = conn.cursor()

    # trying to execute query
    try:
        # Executing the SQL command
        cursor.execute(SQL_QUERY)

        # getting all items from the queried finance_table
        all = cursor.fetchall()

        for r in all:
            # if its a current item or the end date of the item is within this month
            if (r['curr'] == 'yes') or (r['curr'] == 'no' and datetime.strptime(r['end_date'], '%m/%d/%Y') >= datetime.strptime(datetime.now().strftime('%m') + '/01/' + datetime.now().strftime('%Y'), '%m/%d/%Y')):
                if r['type'] == 'needs':
                    needs += float(r['monthly_expense'])
                elif r['type'] == 'fufillment':
                    fufillment += float(r['monthly_expense'])
                elif r['type'] == 'social':
                    social += float(r['monthly_expense'])
                elif r['type'] == 'extra':
                    extra += float(r['monthly_expense'])
    except:
        # Rolling back in case of error
        conn.rollback()

    # closing everything
    cursor.close()

    # returning the ['needs', 'fufillment', 'social', 'extra'] item costs for this month
    return [needs, fufillment, social, extra]

# find the top three largest monthly charges from MS SQL data
def find_top_three():
    '''
    Output : [str, str, str]
        - All the same:
            str - '*item name* - $*item price*', of one of the top three monthly expenses.
        - Left as '' if there are not enough items in MS SQL database.
    '''
    ret = ['', '', '']

    SQL_QUERY = """
    SELECT * FROM finance_table
    """
    # defining Cursor object
    cursor = conn.cursor()

    # trying to execute query
    try:
        # Executing the SQL command
        cursor.execute(SQL_QUERY)

        # getting all items from the queried finance_table
        all = cursor.fetchall()
        
        # making a dictionary of (cost, item name) of all items that are current
        expense_dict = dict([(r['monthly_expense'], r['item']) for r in all if r['curr'] == 'yes'])
        
        ret = []
        # finding top 3
        for i in range(3):
            # if dictionary isn't empty
            if expense_dict != {}:
                max_item = max(expense_dict.items())
                del expense_dict[max_item[0]]
                ret.append(max_item[1] + " - $" + max_item[0])  
            # if there are no more items in dictionary, append empty string
            else:
                ret.append('')

    except:
        # Rolling back in case of error
        conn.rollback()

    # closing everything
    cursor.close()

    # return list of top three items
    return ret
    
# make excel file from queried data 
def make_excel():
    ''' 
    Output : finance_data.xlsx filled with data from sql database, 
            with column headers: item, monthly expense, start date, end date, type, curr
            - all columns are TEXT type
    '''
    
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
    Input: 
        item - string : the name of the financial expense
        monthlyexp - string : the integer only string that represents the monthly cost
        start - char[10] : date in format MM/DD/YYYY that represents when expense started
        end - char[10] : date in format MM/DD/YYYY that represents when expense ended (if '' then its current)
        type - string : either 'needs', 'fufillment', 'social', or 'extra'
        curr - string : 'yes' or 'no' if its a current item
    
    Output:
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
    pass

# close SQL query connection
def finish():
    conn.close()