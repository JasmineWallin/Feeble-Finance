import sys
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QTableWidget, QTableWidgetItem, QTabWidget, QSizePolicy, QDialog, QFrame, QGridLayout, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QPalette, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import openpyxl
from query_data import graph_data, chart_data

from itertools import product

# main window
class Window(QWidget):
      
    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        self.figure = plt.figure() # plot
        self.canvas = FigureCanvas(self.figure)
        self.layoutUI()
    
    def tab1(self): 
        tab1_items = QWidget()
        tab1_items.layout = QVBoxLayout(tab1_items) 
        l = QLabel() 
        l.setText("Feeble Finance\nTrack your finances.") 
        tab1_items.layout.addWidget(l) 
        tab1_items.setLayout(tab1_items.layout) 

        return tab1_items

    def tab2(self):
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

    def tab3(self):
        tab3_items = QWidget()
        tab3_items.layout = QVBoxLayout(tab3_items)
        table_widget = QTableWidget()
        path = "list-countries-world.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        
        table_widget.setRowCount(sheet.max_row)
        table_widget.setColumnCount(sheet.max_column)
        
        list_values = list(sheet.values)
        table_widget.setHorizontalHeaderLabels(list_values[0])
        
        row_index = 0
        for value_tuple in list_values[1:]:
            col_index = 0
            for value in value_tuple:
                table_widget.setItem(row_index , col_index, QTableWidgetItem(str(value)))
                col_index += 1
            row_index += 1

        current_text = QLabel() 
        current_text.setText("My Current Financial Data") 
        add_text = QLabel() 
        add_text.setText("Add More Data") 

        tab3_items.layout.addWidget(current_text)
        tab3_items.layout.addWidget(table_widget)
        tab3_items.layout.addWidget(add_text)
        tab3_items.setLayout(tab3_items.layout)

        return tab3_items

    def layoutUI(self):

        self.principle_layout = QVBoxLayout(self) 
  
        ### Initialize tab screen 
        self.tabs = QTabWidget() 
        self.tab1 = self.tab1()
        self.tab2 = self.tab2()
        self.tab3 = self.tab3() 
        self.tabs.resize(300, 200) 
  
        ### Add tabs 
        self.tabs.addTab(self.tab1, "Home") 
        self.tabs.addTab(self.tab2, "Graphs and Charts") 
        self.tabs.addTab(self.tab3, "My Data") 

        ### Add tabs to widget 
        self.principle_layout.addWidget(self.tabs) 
        self.setLayout(self.principle_layout)

    # Financial graph 
    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111) # create an axis

        # plot data
        data = graph_data()
        ax.plot(data, '*-')
  
        # refresh canvas
        self.canvas.draw()

    def chart(self):
        pass
  
# driver code
if __name__ == '__main__':
      
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
