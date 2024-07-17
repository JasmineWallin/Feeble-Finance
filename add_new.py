##############################
# add_new.py                 #
#                            #
# class that uses GUI form   #
# to add a new item to the   #
# financial database, and    #
# adds it to the MS SQL      #
# database if correct format #
##############################

import query_data
from PyQt5.QtWidgets import *

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setGeometry(100, 100, 300, 400)

        ### creating a group box
        self.formGroupBox = QGroupBox("Add New Financial Item")

        # creating spin box to select cost of item
        self.cost = QDoubleSpinBox()
        self.cost.setMaximum(99999.99)
        
        # spin box for start date , month , year
        self.startmonth = QSpinBox()
        self.startmonth.setMaximum(12)
        self.startday = QSpinBox()
        self.startday.setMaximum(31)
        self.startyear = QComboBox()
        self.startyear.addItems(['2020', '2021', '2022', '2023', '2024'])
        self.startLayout = QHBoxLayout()
        self.startLayout.addWidget(self.startmonth)
        self.startLayout.addWidget(QLabel("/"))
        self.startLayout.addWidget(self.startday)
        self.startLayout.addWidget(QLabel("/"))
        self.startLayout.addWidget(self.startyear)
        
        # spin box for end date , month , year
        self.endmonth = QSpinBox()
        self.endmonth.setMaximum(12)
        self.endday = QSpinBox()
        self.endday.setMaximum(31)
        self.endyear = QComboBox()
        self.endyear.addItems(['2020', '2021', '2022', '2023', '2024'])
        self.endLayout = QHBoxLayout()
        self.endLayout.addWidget(self.endmonth)
        self.endLayout.addWidget(QLabel("/"))
        self.endLayout.addWidget(self.endday)
        self.endLayout.addWidget(QLabel("/"))
        self.endLayout.addWidget(self.endyear)
        
        # creating combo box for if its a current item
        self.curritem = QComboBox()
        self.curritem.addItems(['yes', 'no'])
        
        # creating combo box to select use type
        self.useComboBox = QComboBox()
        self.useComboBox.addItems(['needs', 'fufillment', 'social', 'extra'])
        
        # creating a line edit for name of item
        self.item = QLineEdit()

        ### calling the method that create the form
        self.createForm()

        ### "Ok" button
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.input)

        # adding form group box to the layout
        layout.addWidget(self.formGroupBox)
        # adding button box to the layout
        layout.addWidget(self.buttonBox)
 
        ### setting lay out
        self.setLayout(layout) 
 
    # checking if input is valid, inputting data into MS SQL server
    def input(self):
        # if all inputted values in the form are valid
        if (self.item.text() != '') and (float(self.cost.text()) != 0) and ((self.curritem.currentText() == 'yes' and self.startmonth.text() != '0' and self.startday.text() != '0') or (self.curritem.currentText() == 'no' and self.startmonth.text() != '0' and self.startday.text() != '0' and self.endmonth.text() != '0' and self.endday.text() != '0')):
            out = query_data.input_query(self.item.text(), self.cost.text(), self.startmonth.text() + "/" + self.startday.text() + "/" + self.startyear.currentText(), self.endmonth.text() + "/" + self.endday.text() + "/" + self.endyear.currentText(), self.useComboBox.currentText(), self.curritem.currentText())
            # output an error messagebox if failed
            if out == 0:
                msg = QMessageBox()
                msg.setWindowTitle("Sorry!")
                msg.setText("Server Error: could not add '" + self.item.text() + "' to finance data.")

                x = msg.exec_()
            # output a success messagebox if succeeded, and close add finance item window
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Success")
                msg.setText("Added '" + self.item.text() + "' to finance data.")

                x = msg.exec_()

                # closing the window
                self.close()

        # if there are any invalid inputs in the form
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error!")
            msg.setText("Make sure data is in correct format:\n'Item Name' is not empty\n'Amount Spent' > 0\n'Start Date' is valid (month/date is not 0)\n'End Date' is valid if not 'Current Item' is 'no'\n")

            x = msg.exec_()
 
    # create form method
    def createForm(self):
 
        # creating a form layout
        layout = QFormLayout()
 
        ### adding rows ###

        layout.addRow(QLabel("Item Name"), self.item)
        layout.addRow(QLabel("Monthly Amount Spent"), self.cost)
        layout.addRow(QLabel("Start Date of Item Financing (form MM/DD/YYYY)"))
        layout.addRow(self.startLayout)
        layout.addRow(QLabel("Current Item? (no end date)"), self.curritem)
        layout.addRow(QLabel("End Date of Item Financing (form MM/DD/YYYY)"))
        layout.addRow(self.endLayout)
        layout.addRow(QLabel("Use"), self.useComboBox)
 
        # setting layout
        self.formGroupBox.setLayout(layout)
 
