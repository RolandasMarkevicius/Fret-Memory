from PySide6.QtCore import QSize, Qt, QPropertyAnimation
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon, QResizeEvent
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QVariantAnimation


#Widgets
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Fret Memory')
        self.setMinimumSize(QSize(1920, 1080))
        #self.setSiz

        #Background Colour
        background_widget = QWidget()
        self.setCentralWidget(background_widget)

        background_colour = QColor(50, 50, 51)
        background_widget.setAutoFillBackground(True)

        p = background_widget.palette()
        p.setColor(background_widget.backgroundRole(), background_colour)

        background_widget.setPalette(p)

        first_layout = QVBoxLayout(background_widget)
        second_layout = QVBoxLayout()

        #String buttons

        str_button_size = QSize(50, 50)

        #e button
        # self.e_button = QPushButton(self) #define push button widget
        # e_button_icon = self.svg_to_icon(size=str_button_size, path="Images\e_button.svg")
        # self.e_button.setIcon(e_button_icon)
        # self.e_button.setMinimumSize(str_button_size)

        self.e_button = SVG_Button(svg_path="Images\e_button.svg", size=str_button_size)
        self.e_button.resize(50, 50)
        #self.e_button.setIconSize(QSize(50, 50))
        # self.e_button.setStyleSheet("")
        # self.e_button.setText("")

        #self.e_button.setCheckable(True)
        # self.e_button.clicked.connect(self.toggle_e)
        # #test_button.setChecked(self.test_value)

        second_layout.addWidget(self.e_button)
        first_layout.addLayout(second_layout)
        first_layout.setAlignment(second_layout, Qt.AlignCenter)



    # def svg_to_icon(self, size, path):

    #     #scg to QPixmap
    #     button_pixmap = QPixmap(QSize(500, 500)) #define a pixmap (pixmas is basically a canvas)
    #     button_pixmap.fill(Qt.transparent) #set transparent background for the pixmap
    #     painter = QPainter(button_pixmap) #define the Qpainter object
    #     e_button_img = QSvgRenderer(path) #get the svg image
    #     e_button_img.render(painter) #render the svg on the pixmap
    #     painter.end()

    #     #convert pixmap to icon
    #     icon = QIcon(button_pixmap) 

    #     return icon
        

    def toggle_e(self, checked):
        #get the checked state of the button
        self.test_button_state = checked
        if self.test_button_state == True:
            self.test_button.setText('Disabled')
        elif self.test_button_state == False:
            self.test_button.setText('Enabled')
            #self.test_button.setEnabled(True)


class SVG_Button(QPushButton):
    def __init__(self, svg_path, size, parent=None):
        super().__init__(parent)

        #scg to QPixmap
        button_pixmap = QPixmap(size) #define a pixmap (pixmas is basically a canvas)
        button_pixmap.fill(Qt.transparent) #set transparent background for the pixmap
        painter = QPainter(button_pixmap) #define the Qpainter object
        e_button_img = QSvgRenderer(svg_path) #get the svg image
        e_button_img.render(painter) #render the svg on the pixmap
        painter.end()

        #set the icon
        self.setIcon(QIcon(button_pixmap))
        self.setIconSize(size)

        #hover animation
        self.animation = QPropertyAnimation(self, b"icon")
        self.animation.setDirection(200)
        self.animation.setLoopCount(1)

        self.animation.setStartValue(QIcon(button_pixmap))
        self.animation.


        self.clicked.connect(self.test_click)

        self.setFlat(True)
        self.setStyleSheet("QPushButton { padding: 0px; border: none; }")

    #Hover animation

    #test if button works
    def test_click(self):
        print("button clicked")

    # def resizeEvent(self, event):
    #     return self.setIconSize(event.size(self.size))

    # def resizeEvent(self, event):
    #     # Update icon size when button is resized
    #     self.update_icon_size()


#Qapplication instance
app = QApplication([])

#Widgets
window = MainWindow()
window.show()

#Event loop
app.exec()

#Make a resizable window
#Make a text button For 
