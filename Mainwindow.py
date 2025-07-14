from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime
from database import Database
from charts import draw_all_charts
from PyQt5.QtGui import QIcon




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)


        self.topInputLayout = QtWidgets.QHBoxLayout()
        self.taskLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.taskLineEdit.setPlaceholderText("Task")
        self.topInputLayout.addWidget(self.taskLineEdit)

        self.moodComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.moodComboBox.addItems(["Happy", "Tired", "Motivated"])
        self.topInputLayout.addWidget(self.moodComboBox)

        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setDate(QDate.currentDate())
        self.topInputLayout.addWidget(self.dateEdit)

        self.productivitySpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.productivitySpinBox.setMaximum(10)
        self.topInputLayout.addWidget(self.productivitySpinBox)

        self.addButton = QtWidgets.QPushButton("Add", self.centralwidget)
        self.topInputLayout.addWidget(self.addButton)

        self.verticalLayout.addLayout(self.topInputLayout)


        self.tableWithButtonsLayout = QtWidgets.QHBoxLayout()
        self.taskTable = QtWidgets.QTableWidget(self.centralwidget)
        self.taskTable.setColumnCount(5)
        self.taskTable.setHorizontalHeaderLabels(["Date", "Task", "Mood", "Productivity", "ID"])
        self.tableWithButtonsLayout.addWidget(self.taskTable)

        self.editDeleteButtonLayout = QtWidgets.QVBoxLayout()
        self.editButton = QtWidgets.QPushButton("Edit", self.centralwidget)
        self.editDeleteButtonLayout.addWidget(self.editButton)
        self.deleteButton = QtWidgets.QPushButton("Delete", self.centralwidget)
        self.editDeleteButtonLayout.addWidget(self.deleteButton)

        self.tableWithButtonsLayout.addLayout(self.editDeleteButtonLayout)
        self.verticalLayout.addLayout(self.tableWithButtonsLayout)

        self.chartsLayout = QtWidgets.QHBoxLayout()
        self.barChartLayout = QtWidgets.QVBoxLayout()
        self.lineChartLayout = QtWidgets.QVBoxLayout()
        self.pieChartLayout = QtWidgets.QVBoxLayout()

        self.chartsLayout.addLayout(self.barChartLayout)
        self.chartsLayout.addLayout(self.lineChartLayout)
        self.chartsLayout.addLayout(self.pieChartLayout)
        self.verticalLayout.addLayout(self.chartsLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mood-Task Matrix APP"))
        self.editButton.setText(_translate("MainWindow", "Edit"))
        self.deleteButton.setText(_translate("MainWindow", "Delete"))


class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = Database()
        self.setWindowIcon(QIcon("image.jpg"))

        self.ui.editButton.clicked.connect(self.edit_task)
        self.ui.addButton.clicked.connect(self.add_task)
        self.ui.deleteButton.clicked.connect(self.delete_task)

        self.load_tasks()

    def add_task(self):
        task = self.ui.taskLineEdit.text()
        mood = self.ui.moodComboBox.currentText()
        date = self.ui.dateEdit.date().toString("MM-dd-yyyy")
        productivity = self.ui.productivitySpinBox.value()

        if task.strip():
            self.db.add_task(task, mood, date, productivity)
            self.load_tasks()
            self.ui.taskLineEdit.clear()
            self.ui.productivitySpinBox.setValue(0)
        else:
            QMessageBox.warning(self, "Warning", "Task field can not be empty.")

    def delete_task(self):
        row = self.ui.taskTable.currentRow()
        if row >= 0:
            task_id_item = self.ui.taskTable.item(row, 4)
            if task_id_item:
                task_id = int(task_id_item.text())
                self.db.delete_task(task_id)
                self.load_tasks()

    def edit_task(self):
        row = self.ui.taskTable.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Warning", "Please select a task to edit.")

        task_id_item = self.ui.taskTable.item(row, 4)
        if not task_id_item:
            return QMessageBox.warning(self, "Warning", "ID not found for selected task.")

        task_id = int(task_id_item.text())
        task = self.ui.taskLineEdit.text()
        mood = self.ui.moodComboBox.currentText()
        date = self.ui.dateEdit.date().toString("MM-dd-yyyy")
        productivity = self.ui.productivitySpinBox.value()

        if not task.strip():
            return QMessageBox.warning(self, "Warning", "Task field can not be empty.")

        self.db.edit_task(task_id, task, mood, date, productivity)
        self.load_tasks()

    def load_tasks(self):
        self.ui.taskTable.setRowCount(0)
        tasks = self.db.show_tasks()
        for row_index, task in enumerate(tasks):
            self.ui.taskTable.insertRow(row_index)
            values = [task[3], task[1], task[2], task[4], task[0]]
            for col_index, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                self.ui.taskTable.setItem(row_index, col_index, item)
        draw_all_charts(self.ui.barChartLayout, self.ui.lineChartLayout, self.ui.pieChartLayout, tasks)
