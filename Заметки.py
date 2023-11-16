from PyQt5 import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QColorDialog


class W(QMainWindow):
    def __init__(self):
        Qt.QMainWindow.__init__(self)
        self.tab = Qt.QTabWidget()
        self.setCentralWidget(self.tab)

        self.btnOpen = Qt.QPushButton('Открыть')
        self.btnOpen.clicked.connect(self.open)
        self.statusBar().addWidget(self.btnOpen)

        self.btnSave = Qt.QPushButton('Сохранить')
        self.btnSave.clicked.connect(self.save)
        self.statusBar().addWidget(self.btnSave)

        self.btnClose = Qt.QPushButton('Закрыть')
        self.btnClose.clicked.connect(self.close)
        self.statusBar().addWidget(self.btnClose)

        self.text_edit = QTextEdit()
        self.clear_button = QPushButton('Очистить')
        self.color_button = QPushButton('Сменить цвет кнопок')

        # Устанавливаем начальный цвет фона
        self.setStyleSheet("background-color: #3498db;")

        # Создаем вертикальный Layout
        layout = QVBoxLayout()

        # Добавляем виджеты в Layout
        layout.addWidget(self.text_edit)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.color_button)

        # Создаем виджет для центрального содержимого
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Подключаем обработчики событий для кнопок
        self.clear_button.clicked.connect(self.clearText)
        self.color_button.clicked.connect(self.changeBackgroundColor)

        # Устанавливаем параметры главного окна
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Приложение для заметок')
        self.show()

    def open(self):
        fname = Qt.QFileDialog.getOpenFileName()[0]

        if not fname:
            return

        with open(fname) as f:
            txt = f.read()

        idx = self.tab.addTab(Qt.QTextEdit(), fname)
        self.tab.widget(idx).setPlainText(txt)
        self.tab.setCurrentIndex(idx)

    def save(self):
        fname = Qt.QFileDialog.getSaveFileName()[0]

        if not fname:
            return

        txt = self.tab.currentWidget().toPlainText()

        with open(fname, 'w') as f:
            f.write(txt)

    def close(self):
        idx = self.tab.currentIndex()
        wgt = self.tab.widget(idx)
        self.tab.removeTab(idx)
        del wgt

    def clearText(self):
        self.text_edit.clear()

    def changeBackgroundColor(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()};")


if __name__ == "__main__":
    app = Qt.QApplication([])
    t = W()
    t.resize(640, 480)
    t.show()
    app.exec_()
