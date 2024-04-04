from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow


#Widgets
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Fret Memory')
        self.setFixedSize(QSize(800, 600))

        #Test button
        self.test_button = QPushButton('Enabled')
        self.test_button.setFixedSize(QSize(200, 50))
        self.test_button.setCheckable(True)
        self.test_button.clicked.connect(self.set_string)
        #test_button.setChecked(self.test_value)

        self.setCentralWidget(self.test_button)

    def set_string(self, checked):
        #get the checked state of the button
        self.test_button_state = checked
        if self.test_button_state == True:
            self.test_button.setText('Disabled')
        elif self.test_button_state == False:
            self.test_button.setText('Enabled')
            #self.test_button.setEnabled(True)


#Qapplication instance
app = QApplication([])

#Widgets
window = MainWindow()
window.show()

#Event loop
app.exec()