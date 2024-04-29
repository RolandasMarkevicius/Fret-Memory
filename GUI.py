from PySide6.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve, Signal, Property, QParallelAnimationGroup
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea
from PySide6.QtGui import QPaintEvent, QPixmap, QPainter, QColor, QIcon, QResizeEvent, QPen, QBrush, QFont, QPalette, QPen
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

        #Images
        #Fret boad image
        fretboard_image_size = QSize(900, 200)
        fretboard_image = QSvgWidget("C://Users//Rolandas//Desktop//Portfolio//DL&Python Projects//Fret Memory//Images//Fret_Board.svg")
        fretboard_image.setContentsMargins(0, 0, 0, 0)
        fretboard_image.setFixedSize(fretboard_image_size)

        #Sheet zone
        sheet_zone = QScrollArea()
        sheet_zone.setWidgetResizable(True)

        sheet_widget = SheetWindow(width=1500, height=5000)
        sheet_zone.setWidget(sheet_widget)
        sheet_zone.setFixedSize(QSize(1500, 500))
        

        #Buttons
        button_size = QSize(20, 20)
        button_roundness = 3

        evi_button = NoteButton(size=button_size, 
                                   text="E", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey, 
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)
        evi_button.setContentsMargins(0, 0, 0, 0)

        b_button = NoteButton(size=button_size, 
                                   text="B", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey,
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)
        b_button.setContentsMargins(0, 0, 0, 0)
        
        g_button = NoteButton(size=button_size, 
                                   text="G", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey, 
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)
        g_button.setContentsMargins(0, 0, 0, 0)
        
        d_button = NoteButton(size=button_size, 
                                   text="D", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey, 
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)
        d_button.setContentsMargins(0, 0, 0, 0)
        
        a_button = NoteButton(size=button_size, 
                                   text="A", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey, 
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)
        a_button.setContentsMargins(0, 0, 0, 0)
        
        ei_button = NoteButton(size=button_size, 
                                   text="E", 
                                   background_colour=self.c_background_black, 
                                   neutral_colour=self.c_neutral_grey, 
                                   highlight_colour=self.c_neutral_white,
                                   roundness=button_roundness)
        ei_button.setContentsMargins(0, 0, 0, 0)

        #NoteSheet
        # self.label = QLabel()
        # canvas = QPixmap(400, 300)
        # canvas.fill(Qt.white)
        # self.label.setPixmap(canvas)
        # self.line_paint()


        #Layouts
        first_layout = QVBoxLayout(background_widget)
        first_layout.setContentsMargins(0, 0, 0, 0)
        first_layout.setSpacing(0)

        second_layout = QVBoxLayout()
        second_layout.setContentsMargins(0, 0, 0, 0)
        second_layout.setSpacing(0)

        third_layout = QHBoxLayout()
        third_layout.setContentsMargins(0, 0, 0, 0)
        third_layout.setSpacing(0)

        fourth_layout = QVBoxLayout()
        fourth_layout.setContentsMargins(0, 0, 0, 23)
        fourth_layout.setSpacing(0)

        fourth_layout.addWidget(evi_button)
        fourth_layout.addWidget(b_button)
        fourth_layout.addWidget(g_button)
        fourth_layout.addWidget(d_button)
        fourth_layout.addWidget(a_button)
        fourth_layout.addWidget(ei_button)

        third_layout.addLayout(fourth_layout)
        third_layout.addWidget(fretboard_image)

        second_layout.addLayout(third_layout)
        second_layout.addWidget(sheet_zone)
        # second_layout.addWidget(self.label)

        first_layout.addLayout(second_layout)
        first_layout.setAlignment(second_layout, Qt.AlignCenter)   

    # def line_paint(self):
    #     painter = QPainter(self.label.pixmap())
    #     painter.setPen(self.c_neutral_white)
    #     painter.drawLine(100, 100, 1000, 5000)
    #     painter.end()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.c_neutral_white)
        painter.drawLine(100, 100, 1000, 5000)
        painter.end()


    def toggle_e(self, checked):
        #get the checked state of the button
        self.test_button_state = checked
        if self.test_button_state == True:
            self.test_button.setText('Disabled')
        elif self.test_button_state == False:
            self.test_button.setText('Enabled')
            #self.test_button.setEnabled(True)
    

class Test_Line(QWidget):
    def __init__(self, colour):
        super().__init__()

        self.colour = colour

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.colour)
        painter.drawLine(10, 10, 100, 500)


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
            margin: 0px;
            padding: 0px;
                           """)
        self.setFixedSize(self.size)

        self.anim_background = QVariantAnimation(self)
        self.anim_letter = QVariantAnimation(self)
        self.anim_group = QParallelAnimationGroup()
        self.anim_background.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim_letter.setEasingCurve(QEasingCurve.InOutCubic)

        self.enterEvent = self.button_enter_event #qt sends a signal as enter event, it's assignes to function button _enter event
        self.leaveEvent = self.button_leave_event #dito

        self.pressed.connect(self.pressed_animation)
        self.released.connect(self.release_animation)
        self.clicked.connect(self.button_click)

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
            margin: 0px;
            padding: 0px;
                           """)

        self.anim_background.setStartValue(QColor(self.neutral_colour.name()))
        self.anim_background.setEndValue(QColor(self.highlight_colour.name()))
        self.anim_background.setDuration(250)
        self.anim_background.valueChanged.connect(set_style_sheet)
        self.anim_background.start()

    def button_leave_event(self, event):
        def set_style_sheet():
            print(f'letter colour - {self.anim_letter.currentValue().name()}')
            print(f'background colour - {self.anim_background.currentValue().name()}')
            letter_colour = self.anim_letter.currentValue().name()
            backgorund_colour = self.anim_background.currentValue().name()
            self.setStyleSheet(f"""
            border: none;
            text-align: center;
            text-decoration: none;
            border-radius: {self.roundness}px;
            background-color: {backgorund_colour};;
            color: {letter_colour};
            font-family: Calibri;
            font-size: 15px;
            font-weight: bold;
            margin: 0px;
            padding: 0px;
                           """)
            
        if self.isChecked():
            print("On") 

            self.anim_background.setStartValue(QColor(self.highlight_colour.name()))
            self.anim_background.setEndValue(QColor(self.neutral_colour.name()))
            self.anim_background.setDuration(250)

            self.anim_letter.setStartValue(QColor(self.neutral_colour.name()))
            self.anim_letter.setEndValue(QColor(self.highlight_colour.name()))
            self.anim_letter.setDuration(250)

            self.anim_letter.valueChanged.connect(set_style_sheet)

            self.anim_group.addAnimation(self.anim_letter)
            self.anim_group.addAnimation(self.anim_background)
            self.anim_group.start()

        else:
            print("Off")

            self.anim_background.setStartValue(QColor(self.highlight_colour.name()))
            self.anim_background.setEndValue(QColor(self.neutral_colour.name()))
            self.anim_background.setDuration(250)

            self.anim_letter.setStartValue(QColor(self.neutral_colour.name()))
            self.anim_letter.setEndValue(QColor(self.neutral_colour.name()))
            self.anim_letter.setDuration(250)

            self.anim_letter.valueChanged.connect(set_style_sheet)

            self.anim_group.addAnimation(self.anim_letter)
            self.anim_group.addAnimation(self.anim_background)
            self.anim_group.start()

    def pressed_animation(self):

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
                margin: 0px;
                padding: 0px;
                            """)

        self.anim_background.setStartValue(QColor(self.highlight_colour.name()))
        self.anim_background.setEndValue(QColor(self.neutral_colour.name()))
        self.anim_background.setDuration(100)
        self.anim_background.valueChanged.connect(set_style_sheet)
        self.anim_background.start()

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
                margin: 0px;
                padding: 0px;
                            """)

        self.anim_background.setStartValue(QColor(self.neutral_colour.name()))
        self.anim_background.setEndValue(QColor(self.highlight_colour.name()))
        self.anim_background.setDuration(100)
        self.anim_background.valueChanged.connect(set_style_sheet)
        self.anim_background.start()


    def button_click(self, checked):
        print("button clicked", checked)

class SheetWindow(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)

        self.c_background_black = QColor(50, 50, 51)
        self.c_neutral_grey = QColor(97, 98, 102)
        self.c_neutral_white = QColor(181, 182, 188)

        self.setMinimumSize(width, height)
        self.sheet_height = height
        self.sheet_width = width
        self.initUI()

    def initUI(self):
        self.pixmap = QPixmap(self.sheet_width, self.sheet_height)
        self.pixmap.fill(self.c_background_black)

        painter = QPainter(self.pixmap)
        painter.setPen(QPen(self.c_neutral_grey, 1, Qt.SolidLine))
        for i in range(0, self.sheet_height, 50):
            painter.drawLine(0, i, self.sheet_width, i)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)


#Qapplication instance
app = QApplication([])

#Widgets
window = MainWindow()
window.show()

#Event loop
app.exec()
