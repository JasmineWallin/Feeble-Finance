# Feeble Finance
See your finances through charts and plots to track your expenses! PyQt5 Graphical User Interface (GUI) Application for visualizing finances using SQL and matplotlib. 
Built on a 2019 Ventura Intel Macbook, using Docker Desktop, Azure Data Studio, and VSCode. 

Necessary Software: Microsoft SQL network/database

Set Up
------
Installations Needed: python3, pyqt5, pyqt5-tools, pymssql, matplotlib, openpyxl, xlsxwriter

1) Install the needed installations and connect to a Microsoft SQL database.
2) Download or clone this repository.
3) Create a duplicate of the file 'pymssql_sess.py.example.txt' and name it 'pymssql_sess.py'. Fill the tuple (replace '' occurences) with information that you will be using. Save the file. *Check [this out](https://pymssql.readthedocs.io/en/latest/ref/pymssql.html#functions) for information on how to fill out a pymssql connect tuple.*

# How to Run
- run ```main.py```. A GUI should show up.
    - 'refresh data' buttons on tab 2 and tab 3 will need to be pressed whenever new data is added, or upon starting the program.
    - to add new data to the database, navigate to tab 3 and click the 'Add More Data' button.

In Production.


*July 2024 @Jasmine Wallin.*
