from PySide6.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve, Signal, Property
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon, QResizeEvent, QPen, QBrush, QFont, QPalette
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

class NoteButton(QPushButton):
    def __init__(self, size, text, back_colour, letter_colour, roundness, parent=None):
        super().__init__(parent)

        self.setFlat(True)

        self.size = size
        self.text = text
        #self.font = QFont("Calibri", 13)
        self.back_colour = back_colour
        self.letter_colour = letter_colour
        self.roundness = roundness

        self.custom_font = QFont() #define the font class
        self.custom_font.setFamily("Calibri") #set the font type
        self.custom_font.setBold(True) #set font class to Bold
        self.custom_font.setPointSize(13) #set the font size


        self.setFixedSize(size) #set the size

        self.clicked.connect(self.test_click)

        #Hover animation
        # self.normal_style = f"background-color: {self.back_colour.name()};"
        # self.hover_style = f"background-color: #122fe0;" ##b5b6bc

        self.enterEvent = self.button_enter_event #qt sends a signal as enter event, it's assignes to function button _enter event
        self.leaveEvent = self.button_leave_event #dito

        self.animation = QVariantAnimation(self)
        self.animation.setDuration(2000)
        #self.animation.setEasingCurve(QEasingCurve.InOutCubic)

    def button_enter_event(self, event):
        print('test enter')
        palette = self.palette()
        role = self.foregroundRole()

        def updateColour(colour):
            palette.setColor(role, colour)
            self.setPalette(palette)

        self.animation.setStartValue(QColor(129, 40, 59))
        self.animation.setEndValue(QColor(93, 135, 150))
        self.animation.valueChanged.connect(updateColour)
        self.animation.start(self.animation) #self.animation.DeleteWhenStopped

        
        # print(f"{self.back_colour.name()}")
        # self.animation.setStartValue(QColor(29, 40, 59))
        # self.animation.setEndValue(QColor(93,35, 50))
        # self.animation.start()

    def button_leave_event(self, event):
        print("left button")
        self.animation.setStartValue(QColor(29, 40, 59))
        self.animation.setEndValue(QColor(93, 135, 150))
        self.animation.start()

        # #Click animation
        # self.animateClick()

        #Generate the image
    # def paintEvent(self, event): #what does the event do?
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing) #enable anti aliasing for smooth edges

    #     #Draw rounded rectangle
    #     painter.setPen(Qt.NoPen)
    #     painter.setBrush(self.back_colour)
    #     painter.drawRoundedRect(0, 0, self.width(), self.height(), self.roundness, self.roundness)

    #     #Draw letter
    #     painter.setPen(self.letter_colour)
    #     painter.setFont(self.custom_font)
    #     painter.drawText(event.rect(), Qt.AlignCenter, self.text)
    #     painter.end()


    def paintEvent(self, event):
        # Let's clear the background in case style sheet has a background color
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.base)
        self.setStyleSheet("")

        # Now we'll set the style sheet to draw the rounded rectangle
        style_sheet = f"QPushButton {{ border-radius: {self.roundness}px; background-color: {self.back_colour.name()}; }}"
        self.setStyleSheet(style_sheet)

        # We'll set the text color directly in the style sheet
        style_sheet += f"color: {self.letter_colour.name()};"  # Text color
        style_sheet += f"font-family: Calibri;"  # Font family
        style_sheet += f"font-size: 11pt;"  # Font size
        style_sheet += f"font-weight: bold;"

        # style_sheet += "}"  # Close the style sheet

        # Call the base class paintEvent to draw the button's text
        super().paintEvent(event)

    def test_click(self):
        print("button clicked")



#Qapplication instance
app = QApplication([])

#Widgets
window = MainWindow()
window.show()

#Event loop
app.exec()
