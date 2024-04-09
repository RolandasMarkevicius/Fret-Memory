from PySide6.QtCore import QSize, Qt, QPropertyAnimation
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon, QResizeEvent, QPen, QBrush, QFont
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtSvgWidgets import QSvgWidget
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

        #Layouts

        first_layout = QVBoxLayout(background_widget)
        second_layout = QVBoxLayout()
        third_layout = QHBoxLayout()
        fourth_layout = QVBoxLayout()

        #Images

        #Fret boad image
        fretboard_image_size = QSize(900, 200)
        fretboard_image = QSvgWidget("C://Users//Rolandas//Desktop//Portfolio//DL&Python Projects//Fret Memory//Images//Fret_Board.svg")
        fretboard_image.setFixedSize(fretboard_image_size)

        #Buttons
        button_size = QSize(20, 20)
        button_back_colour = QColor(97, 98, 102)
        button_letter_colour = QColor(50, 50, 51)
        button_roundness = 3

        evi_button = NoteButton(size=button_size, 
                                   text="E", 
                                   back_colour=button_back_colour, 
                                   letter_colour=button_letter_colour, 
                                   roundness=button_roundness)

        b_button = NoteButton(size=button_size, 
                                   text="B", 
                                   back_colour=button_back_colour, 
                                   letter_colour=button_letter_colour, 
                                   roundness=button_roundness)
        
        g_button = NoteButton(size=button_size, 
                                   text="G", 
                                   back_colour=button_back_colour, 
                                   letter_colour=button_letter_colour, 
                                   roundness=button_roundness)
        
        d_button = NoteButton(size=button_size, 
                                   text="D", 
                                   back_colour=button_back_colour, 
                                   letter_colour=button_letter_colour, 
                                   roundness=button_roundness)
        
        a_button = NoteButton(size=button_size, 
                                   text="A", 
                                   back_colour=button_back_colour, 
                                   letter_colour=button_letter_colour, 
                                   roundness=button_roundness)
        
        ei_button = NoteButton(size=button_size, 
                                   text="E", 
                                   back_colour=button_back_colour, 
                                   letter_colour=button_letter_colour, 
                                   roundness=button_roundness)

        # second_layout.addWidget(self.e_button)
        fourth_layout.addWidget(evi_button)
        fourth_layout.addWidget(b_button)
        fourth_layout.addWidget(g_button)
        fourth_layout.addWidget(d_button)
        fourth_layout.addWidget(a_button)
        fourth_layout.addWidget(ei_button)

        third_layout.addLayout(fourth_layout)
        third_layout.addWidget(fretboard_image)

        first_layout.addLayout(third_layout)
        first_layout.setAlignment(second_layout, Qt.AlignCenter)        

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
        # self.animation = QPropertyAnimation(self, b"icon")
        # self.animation.setDirection(200)
        # self.animation.setLoopCount(1)

        # self.animation.setStartValue(QIcon(button_pixmap))
        # #self.animation.


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

class NoteButton(QPushButton):
    def __init__(self, size, text, back_colour, letter_colour, roundness, parent=None):
        super().__init__(parent)

        self.setFlat(True)

        self.size = size
        self.text = text
        self.back_colour = back_colour
        self.letter_colour = letter_colour
        self.roundness = roundness

        self.custom_font = QFont() #define the font class
        self.custom_font.setFamily("Calibri") #set the font type
        self.custom_font.setBold(True) #set font class to Bold
        self.custom_font.setPointSize(13) #set the font size


        self.setFixedSize(size) #set the size

        self.clicked.connect(self.test_click)

        #Generate the image
    def paintEvent(self, event): #what does the event do?
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) #enable anti aliasing for smooth edges

        #Draw rounded rectangle
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.back_colour)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.roundness, self.roundness)

        #Draw letter
        painter.setPen(self.letter_colour)
        painter.setFont(self.custom_font)
        painter.drawText(event.rect(), Qt.AlignCenter, self.text)
        painter.end()

    def test_click(self):
        print("button clicked")



#Qapplication instance
app = QApplication([])

#Widgets
window = MainWindow()
window.show()

#Event loop
app.exec()
