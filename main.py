import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QWidget, QMenu, QAction, QDialog, QVBoxLayout as QVLayout
from PyQt5.QtCore import Qt
from Tools.scripts.serve import app

from logic.student_logic import StudentLogic


class StudentInfoDialog(QDialog):
    def __init__(self, student_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Student Information")
        self.setGeometry(100, 100, 300, 200)

        layout = QVLayout()

        for key, value in student_info.items():
            label = QLabel(f"{key.capitalize()}: {value}")
            layout.addWidget(label)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logic = StudentLogic()

        self.setWindowTitle("Student Management App")
        self.setGeometry(100, 100, 600, 800)

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        self.class_label = QLabel("Class:")
        self.class_input = QLineEdit()

        self.add_button = QPushButton("Add Student")
        self.add_button.clicked.connect(self.add_student)

        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(self.search_students)
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_students)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(3)
        self.student_table.setHorizontalHeaderLabels(["ID", "Name", "Class"])
        self.refresh_student_table()

        self.student_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.student_table.customContextMenuRequested.connect(self.show_context_menu)

        self.details_button = QPushButton("Show Details")
        self.details_button.clicked.connect(self.show_student_details)

        self.add_arabic_students_button = QPushButton("Add Arabic Students")
        self.add_arabic_students_button.clicked.connect(self.add_arabic_students)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.class_label)
        layout.addWidget(self.class_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.student_table)
        layout.addWidget(self.details_button)
        layout.addWidget(self.add_arabic_students_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_student(self):
        name = self.name_input.text()
        class_ = self.class_input.text()
        self.logic.add_student(name, class_)
        self.refresh_student_table()

    def refresh_student_table(self):
        students = self.logic.get_all_students()
        self.student_table.setRowCount(len(students))

        for row, student in enumerate(students):
            self.student_table.setItem(row, 0, QTableWidgetItem(str(student['id'])))
            self.student_table.setItem(row, 1, QTableWidgetItem(student['name']))
            self.student_table.setItem(row, 2, QTableWidgetItem(student['class']))

    def show_context_menu(self, pos):
        menu = QMenu(self)
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.delete_selected_row)
        menu.addAction(delete_action)
        menu.exec_(self.student_table.viewport().mapToGlobal(pos))

    def delete_selected_row(self):
        selected_row = self.student_table.currentRow()
        if selected_row >= 0:
            item = self.student_table.item(selected_row, 0)
            student_id = int(item.text())
            self.logic.delete_student(student_id)
            self.refresh_student_table()

    def show_student_details(self):
        selected_row = self.student_table.currentRow()
        if selected_row >= 0:
            student_info = {
                "ID": self.student_table.item(selected_row, 0).text(),
                "Name": self.student_table.item(selected_row, 1).text(),
                "Class": self.student_table.item(selected_row, 2).text()
            }
            student_info_dialog = StudentInfoDialog(student_info, self)
            student_info_dialog.exec_()

    def search_students(self):
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            self.refresh_student_table()
            return

        students = self.logic.get_all_students()
        filtered_students = [student for student in students if
                             search_term in student['name'].lower() or search_term in student['class'].lower()]

        self.student_table.setRowCount(len(filtered_students))

        for row, student in enumerate(filtered_students):
            self.student_table.setItem(row, 0, QTableWidgetItem(str(student['id'])))
            self.student_table.setItem(row, 1, QTableWidgetItem(student['name']))
            self.student_table.setItem(row, 2, QTableWidgetItem(student['class']))

    def add_arabic_students(self):
        arabic_names = [
            "عبدالله", "محمد", "أحمد", "محمود", "مصطفى", "يوسف", "عمر", "علي", "خالد", "إسماعيل",
            "نور", "سارة", "فاطمة", "مريم", "ليلى", "عائشة", "زينب", "ميساء", "هاجر", "رانيا"
        ]

        for _ in range(50):
            random_name = random.choice(arabic_names)
            random_class = f"Class {random.randint(1, 12)}"
            self.logic.add_student(random_name, random_class)

        self.refresh_student_table()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
