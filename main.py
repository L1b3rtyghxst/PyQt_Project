import json
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, QWidget, \
    QVBoxLayout, QHBoxLayout, \
    QPushButton, QListWidget, \
    QListWidgetItem, QTextEdit, \
    QLineEdit, QCheckBox, \
    QLabel, QFileDialog, \
    QMessageBox


class TaskManagerApp(QMainWindow):

    # Инициализация
    def __init__(self):
        super().__init__()
        self.note_text = None
        self.notes_list = None
        self.done_tasks_label = None
        self.total_tasks_label = None
        self.task_description = None
        self.task_input = None
        self.task_list = None
        self.show_all_checkbox = None
        self.note_input = None
        self.tasks = []
        self.initUI()

    # Дизайн окна
    def initUI(self):
        self.setWindowTitle('Task Manager')
        self.setWindowIcon(QIcon('task_manager_icon.png'))
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        self.task_list = QListWidget(self)
        self.task_list.itemClicked.connect(self.onTaskClicked)
        layout.addWidget(self.task_list)

        task_input_layout = QHBoxLayout()
        self.task_input = QLineEdit(self)
        task_input_layout.addWidget(self.task_input)

        add_button = QPushButton('Добавить', self)
        add_button.clicked.connect(self.addTask)
        task_input_layout.addWidget(add_button)

        layout.addLayout(task_input_layout)

        self.task_description = QTextEdit(self)
        self.task_description.setPlaceholderText('Описание задачи...')
        layout.addWidget(self.task_description)

        control_layout = QHBoxLayout()

        edit_button = QPushButton('Редактировать', self)
        edit_button.clicked.connect(self.editTask)
        control_layout.addWidget(edit_button)

        delete_button = QPushButton('Удалить', self)
        delete_button.clicked.connect(self.deleteTask)
        control_layout.addWidget(delete_button)

        notes_button = QPushButton('Заметки', self)
        notes_button.clicked.connect(self.notes)
        control_layout.addWidget(notes_button)

        paint_button = QPushButton('Порисовать', self)
        paint_button.clicked.connect(self.deleteTask)
        control_layout.addWidget(paint_button)

        layout.addLayout(control_layout)

        save_button = QPushButton('Сохранить', self)
        save_button.clicked.connect(self.saveTasks)
        layout.addWidget(save_button)

        load_button = QPushButton('Загрузить', self)
        load_button.clicked.connect(self.loadTasks)
        layout.addWidget(load_button)

        filter_layout = QHBoxLayout()

        self.show_all_checkbox = QCheckBox('Показать все задачи', self)
        self.show_all_checkbox.stateChanged.connect(self.updateTaskList)
        filter_layout.addWidget(self.show_all_checkbox)

        self.total_tasks_label = QLabel('Всего задач: 0', self)
        filter_layout.addWidget(self.total_tasks_label)

        self.done_tasks_label = QLabel('Выполнено: 0', self)
        filter_layout.addWidget(self.done_tasks_label)

        layout.addLayout(filter_layout)

        self.updateStyleSheet()
        self.show()

    # Проверка на нажатие кнопки
    def onTaskClicked(self, item):
        current_row = self.task_list.row(item)
        task = self.tasks[current_row]
        self.task_input.setText(task['name'])
        self.task_description.setPlainText(task['description'])

    # Добавление задачи
    def addTask(self):
        task_name = self.task_input.text()

        if task_name:
            self.tasks.append({'name': task_name, 'description': self.task_description.toPlainText(), 'done': False})
            self.updateTaskList()
            self.task_input.clear()
            self.task_description.clear()

    # Редактирование задачи
    def editTask(self):
        current_row = self.task_list.currentRow()

        if current_row >= 0:
            task = self.tasks[current_row]
            task['name'] = self.task_input.text()
            task['description'] = self.task_description.toPlainText()
            self.updateTaskList()

    # Удаление задачи
    def deleteTask(self):
        current_row = self.task_list.currentRow()

        if current_row >= 0:
            del self.tasks[current_row]
            self.updateTaskList()
            self.task_input.clear()
            self.task_description.clear()

    # Количество задач
    def updateTaskList(self):
        self.task_list.clear()
        show_all = self.show_all_checkbox.isChecked()
        total_tasks = 0
        done_tasks = 0

        for task in self.tasks:

            if show_all or not task['done']:
                item = QListWidgetItem(task['name'])
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked if task['done'] else Qt.Unchecked)
                self.task_list.addItem(item)
                total_tasks += 1

                if task['done']:
                    done_tasks += 1

        self.total_tasks_label.setText(f'Всего задач: {total_tasks}')
        self.done_tasks_label.setText(f'Выполнено: {done_tasks}')

    # Стилизация главного окна
    def updateStyleSheet(self):
        style = """
            QWidget {
                background-color: #F1F1F1;
            }
            QListWidget, QTextEdit, QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #007ACC;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QCheckBox {
                font-weight: bold;
            }
            QLabel {
                font-size: 16px;
            }
        """
        self.setStyleSheet(style)
        self.setFont(QFont("Arial", 12))

    # Загрузить задачи
    def loadTasks(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, 'Загрузить задачи', '', 'JSON Files (*.json)', options=options)

        if file_name:

            try:

                with open(file_name, 'r', encoding='utf-8') as file:
                    self.tasks = json.load(file)
                self.updateTaskList()

            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', 'Не удалось загрузить задачи: ' + str(e))

    # Создание заметки
    def createNotesPage(self):
        notes_page = QWidget(self)
        notes_layout = QVBoxLayout(notes_page)

        self.notes_list = QListWidget(self)
        self.notes_list.itemClicked.connect(self.onNoteClicked)
        notes_layout.addWidget(self.notes_list)

        note_input_layout = QHBoxLayout()
        self.note_input = QLineEdit(self)
        note_input_layout.addWidget(self.note_input)

        add_note_button = QPushButton('Добавить заметку', self)
        add_note_button.clicked.connect(self.addNote)
        note_input_layout.addWidget(add_note_button)

        notes_layout.addLayout(note_input_layout)

        self.note_text = QTextEdit(self)
        self.note_text.setPlaceholderText('Текст заметки...')
        notes_layout.addWidget(self.note_text)

        return notes_page

    # Показать задачи
    def showTasksPage(self):
        self.stacked_widget.setCurrentIndex(0)

    # Показать заметки
    def showNotesPage(self):
        self.stacked_widget.setCurrentIndex(1)

    # Сохраниь задачи
    def saveTasks(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить задачи', '', 'JSON Files (*.json)', options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=4)

    # Открытие рисовашки
    @staticmethod
    def paint():
        os.system('paint.exe')

    # Открытие заметки
    @staticmethod
    def notes():
        os.system('word.exe')


def main():
    app = QApplication(sys.argv)
    task_manager = TaskManagerApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
