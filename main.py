#############################
# main.py                   #
#                           #
# GUI that supports         #
# functionality of showing  #
# finance data through      #
# graphs, charts, and       #
# spreadsheets. Queries and #
# fetches data from MS SQL  #
# server.                   #
#############################

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # TODO maybe only neeed these in query_data.py
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import openpyxl
import query_data
from add_new import AnotherWindow

from itertools import product

# main window
class Window(QWidget):
      
    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        self.figure = plt.figure() # plot
        self.canvas = FigureCanvas(self.figure)
        self.table_widget = QTableWidget()
        self.layoutUI()
    
    # "Title Screen" tab
    def tab1(self): 
        # GUI items
        tab1_items = QWidget()
        tab1_items.layout = QVBoxLayout(tab1_items) 
        l = QLabel() 
        l.setText("Feeble Finance\nTrack your finances.") 
        
        # adding items onto the layout
        tab1_items.layout.addWidget(l) 
        tab1_items.setLayout(tab1_items.layout) 

        return tab1_items

    # Tab to show data through graphs and charts
    def tab2(self):
        # GUI items
        tab2_items = QWidget()
        tab2_items.layout = QVBoxLayout(tab2_items)
        Button_01 = QPushButton("Refresh Data")
        Button_01.clicked.connect(self.plot)
        tab2_items.layout.addWidget(Button_01)
        tab2_items.setLayout(tab2_items.layout)

        # creating a scrollable widget
        scroll = QScrollArea(self)
        tab2_items.layout.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)

        # Defining items that will go on screen
        graph_text = QLabel() 
        graph_text.setText("Graph of Expenses") 
        chart_text = QLabel() 
        chart_text.setText("Chart of Expense Breakdown")   
        self.toolbar = NavigationToolbar(self.canvas, tab2_items) # toolbar

        # Adding items to the screen through a vertical layout
        scrollLayout.addWidget(graph_text)
        scrollLayout.addWidget(self.toolbar)
        scrollLayout.addWidget(self.canvas)
        scrollLayout.addWidget(chart_text)

        scroll.setWidget(scrollContent)
        
        return tab2_items

    # Tab to show current database, and add more items to the database
    def tab3(self):
        # GUI items
        tab3_items = QWidget()
        tab3_items.layout = QVBoxLayout(tab3_items)
        current_text = QLabel() 
        current_text.setText("My Current Financial Data") 
        Button_ref = QPushButton("Refresh Data")
        Button_ref.clicked.connect(self.excel_sheet)
        add_button = QPushButton("Add More Data") 
        add_button.clicked.connect(self.add_form)
 
        # adding items onto the layout
        tab3_items.layout.addWidget(Button_ref)
        tab3_items.layout.addWidget(current_text)
        tab3_items.layout.addWidget(self.table_widget)
        tab3_items.layout.addWidget(add_button)
        tab3_items.setLayout(tab3_items.layout)

        return tab3_items

    # main layout with bar of tabs
    def layoutUI(self):

        self.principle_layout = QVBoxLayout(self) 
  
        # Initialize tab screen 
        self.tabs = QTabWidget() 
        self.tab1 = self.tab1()
        self.tab2 = self.tab2()
        self.tab3 = self.tab3() 
        self.tabs.resize(300, 200) 
  
        # Add tabs 
        self.tabs.addTab(self.tab1, "Home") 
        self.tabs.addTab(self.tab2, "Graphs and Charts") 
        self.tabs.addTab(self.tab3, "My Data") 

        # Add tabs to widget 
        self.principle_layout.addWidget(self.tabs) 
        self.setLayout(self.principle_layout)

    # Financial graph for tab 3 
    def plot(self):
        # TODO THIS IS NEXT!
        self.figure.clear()
        ax = self.figure.add_subplot(111) # create an axis

        # plot data
        data = query_data.graph_data()
        ax.plot(data, '*-')
  
        # refresh canvas
        self.canvas.draw()

    # Chart for tab 3
    def chart(self):
        # TODO THIS IS NEXT!
        pass
    
    # finds input from a form to add to data
    def add_form(self):
        self.w = AnotherWindow()
        self.w.show()
    
    # creates the GUI data sheet and the data inside
    def excel_sheet(self):
        # initialising the finance_data file
        query_data.make_excel() # writing the finance_data.xlsx file
        path = "finance_data.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        
        # row and col count
        self.table_widget.setRowCount(sheet.max_row)
        self.table_widget.setColumnCount(sheet.max_column)
        
        # column headers
        list_values = list(sheet.values)
        self.table_widget.setHorizontalHeaderLabels(list_values[0])
        
        # filling the table
        row_index = 0
        for value_tuple in list_values[1:]:
            col_index = 0
            for value in value_tuple:
                self.table_widget.setItem(row_index , col_index, QTableWidgetItem(str(value)))
                col_index += 1
            row_index += 1

    # close the query connection upon exiting the program
    def closeEvent(self, event):
        query_data.finish()
  
# driver code
if __name__ == '__main__':
    
    # creating the SQL database if it doesn't exist already
    query_data.create_database()

    # creating apyqt5 application
    app = QApplication(sys.argv)
  
    # creating a window object
    main = Window()
    main.setWindowTitle("Feeble Finance")
    main.setGeometry(200, 200, 800, 600)

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())
