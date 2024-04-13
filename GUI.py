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
        
        #Colour Variables
        self.c_background_black = QColor(50, 50, 51)
        self.c_neutral_grey = QColor(97, 98, 102)
        self.c_neutral_white = QColor(181, 182, 188)

        #Background setup
        background_widget = QWidget()
        self.setCentralWidget(background_widget)
        background_widget.setAutoFillBackground(True)

        p = background_widget.palette()
        p.setColor(background_widget.backgroundRole(), self.c_background_black)

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
        button_roundness = 3

        evi_button = NoteButton(size=button_size, 
                                   text="E", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey, 
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)

        b_button = NoteButton(size=button_size, 
                                   text="B", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey,
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)
        
        g_button = NoteButton(size=button_size, 
                                   text="G", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey, 
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)
        
        d_button = NoteButton(size=button_size, 
                                   text="D", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey, 
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)
        
        a_button = NoteButton(size=button_size, 
                                   text="A", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey, 
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)
        
        ei_button = NoteButton(size=button_size, 
                                   text="E", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey, 
                                   highlight_colour=self.c_neutral_white,
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
    def __init__(self, size, text, background_colour, neutral_colour, highlight_colour, roundness, parent=None):
        super().__init__(parent)

        self.setFlat(True)

        self.size = size
        self.text = text
        self.background_colour = background_colour
        self.neutral_colour = neutral_colour
        self.highlight_colour = highlight_colour
        self.roundness = roundness

        self.setText(self.text)
        self.setStyleSheet(f"""
            border: none;
            text-align: center;
            text-decoration: none;
            border-radius: {self.roundness}px;
            background-color: {self.neutral_colour.name()};
            color: {self.background_colour.name()};
            font-family: Calibri;
            font-size: 15px;
            font-weight: bold;
            padding: 0;
                           """)
        self.setFixedSize(self.size)

        # self.clicked.connect(self.button_click)

        self.animation = QVariantAnimation(self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.enterEvent = self.button_enter_event #qt sends a signal as enter event, it's assignes to function button _enter event
        self.leaveEvent = self.button_leave_event #dito

        self.clicked.connect(self.click_animation)
        self.released.connect(self.release_animation)

        self.setCheckable(True)

    def button_enter_event(self, event):
        def set_style_sheet(color):
            self.setStyleSheet(f"""
            border: none;
            text-align: center;
            text-decoration: none;
            border-radius: {self.roundness}px;
            background-color: {color.name()};;
            color: {self.background_colour.name()};
            font-family: Calibri;
            font-size: 15px;
            font-weight: bold;
            padding: 0;
                           """)

        self.animation.setStartValue(QColor(self.neutral_colour.name()))
        self.animation.setEndValue(QColor(self.highlight_colour.name()))
        self.animation.setDuration(250)
        self.animation.valueChanged.connect(set_style_sheet)
        self.animation.start()

    def button_leave_event(self, event):
        def set_style_sheet(color):
            self.setStyleSheet(f"""
            border: none;
            text-align: center;
            text-decoration: none;
            border-radius: {self.roundness}px;
            background-color: {color.name()};;
            color: {self.background_colour.name()};
            font-family: Calibri;
            font-size: 15px;
            font-weight: bold;
            padding: 0;
                           """)

        self.animation.setStartValue(QColor(self.highlight_colour.name()))
        self.animation.setEndValue(QColor(self.neutral_colour.name()))
        self.animation.setDuration(250)
        self.animation.valueChanged.connect(set_style_sheet)
        self.animation.start()        

    def click_animation(self, checked):

        def set_style_sheet(colour):
                self.setStyleSheet(f"""
                border: none;
                text-align: center;
                text-decoration: none;
                border-radius: {self.roundness}px;
                background-color: {colour.name()};;
                color: {self.background_colour.name()};
                font-family: Calibri;
                font-size: 15px;
                font-weight: bold;
                padding: 0;
                            """)

        #self.mousePressEvent = True

        #if statement
        if checked == True:
            print("click test", checked)

            self.animation.setStartValue(QColor(self.highlight_colour.name()))
            self.animation.setEndValue(QColor(self.neutral_colour.name()))
            self.animation.setDuration(100)
            self.animation.valueChanged.connect(set_style_sheet)
            self.animation.start()

            #change the static button look            

        # elif checked == False:
        #     print("click test", checked)
        #     def set_style_sheet(color):
        #         self.setStyleSheet(f"""
        #         border: none;
        #         text-align: center;
        #         text-decoration: none;
        #         border-radius: {self.roundness}px;
        #         background-color: {color.name()};;
        #         color: {self.letter_colour.name()};
        #         font-family: Calibri;
        #         font-size: 15px;
        #         font-weight: bold;
        #         padding: 0;
        #                     """)

        #     self.animation.setStartValue(QColor(self.back_colour.name()))
        #     self.animation.setEndValue(QColor(self.highlight_colour.name()))
        #     self.animation.valueChanged.connect(set_style_sheet)
        #     self.animation.start()

    def release_animation(self):
        def set_style_sheet(colour):
                self.setStyleSheet(f"""
                border: none;
                text-align: center;
                text-decoration: none;
                border-radius: {self.roundness}px;
                background-color: {colour.name()};;
                color: {self.background_colour.name()};
                font-family: Calibri;
                font-size: 15px;
                font-weight: bold;
                padding: 0;
                            """)

        #if statement
        print("release test")

        self.animation.setStartValue(QColor(self.neutral_colour.name()))
        self.animation.setEndValue(QColor(self.highlight_colour.name()))
        self.animation.setDuration(100)
        self.animation.valueChanged.connect(set_style_sheet)
        self.animation.start()

        # elif checked == False:
        #     print("click test", checked)
        #     def set_style_sheet(color):
        #         self.setStyleSheet(f"""
        #         border: none;
        #         text-align: center;
        #         text-decoration: none;
        #         border-radius: {self.roundness}px;
        #         background-color: {color.name()};;
        #         color: {self.neutral_colour.name()};
        #         font-family: Calibri;
        #         font-size: 15px;
        #         font-weight: bold;
        #         padding: 0;
        #                     """)

        #     self.animation.setStartValue(QColor(self.background_colour.name()))
        #     self.animation.setEndValue(QColor(self.highlight_colour.name()))
        #     self.animation.valueChanged.connect(set_style_sheet)
        #     self.animation.start()

    # def button_click(self):
    #     print("button clicked")

    # def button_release(self):
    #     print("button released")


#Qapplication instance
app = QApplication([])

#Widgets
window = MainWindow()
window.show()

#Event loop
app.exec()
