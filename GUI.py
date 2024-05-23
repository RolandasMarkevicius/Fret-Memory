from PySide6.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve, Signal, Property, QParallelAnimationGroup, QThread, Signal, QEventLoop
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QSizePolicy
from PySide6.QtGui import QPaintEvent, QPixmap, QPainter, QColor, QIcon, QResizeEvent, QPen, QBrush, QFont, QPalette, QPen, QFontMetrics, QPainterPath
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import QVariantAnimation

import math
import numpy as np
import threading
import time
import queue

from sound_processing import StringPicker, CalibrateGuitar, SoundProcessing

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

        sheet_zone.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        sheet_zone.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)#scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        #Buttons
        button_size = QSize(20, 20)
        button_roundness = 3

        self.evi_button = NoteButton(size=button_size, 
                                   text="E", 
                                   roundness=button_roundness)
        self.evi_button.setContentsMargins(0, 0, 0, 0)

        self.b_button = NoteButton(size=button_size, 
                                   text="B", 
                                   roundness=button_roundness)
        self.b_button.setContentsMargins(0, 0, 0, 0)
        
        self.g_button = NoteButton(size=button_size, 
                                   text="G", 
                                   roundness=button_roundness)
        self.g_button.setContentsMargins(0, 0, 0, 0)
        
        self.d_button = NoteButton(size=button_size, 
                                   text="D", 
                                   roundness=button_roundness)
        self.d_button.setContentsMargins(0, 0, 0, 0)
        
        self.a_button = NoteButton(size=button_size, 
                                   text="A", 
                                   roundness=button_roundness)
        self.a_button.setContentsMargins(0, 0, 0, 0)
        
        self.ei_button = NoteButton(size=button_size, 
                                   text="E", 
                                   roundness=button_roundness)
        self.ei_button.setContentsMargins(0, 0, 0, 0)

        self.calibrate_guitar_button = TextButton(text='Calibrate the Guitar')

        #Button Functions
        self.string_check = StringPicker()
        self.evi_button.clicked.connect(self.string_check.click_evi)
        self.b_button.clicked.connect(self.string_check.click_b)
        self.g_button.clicked.connect(self.string_check.click_g)
        self.d_button.clicked.connect(self.string_check.click_d)
        self.a_button.clicked.connect(self.string_check.click_a)
        self.ei_button.clicked.connect(self.string_check.click_ei)

        self.calibrate_guitar_button.clicked.connect(self.calibrate_guitar)


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

        fourth_layout.addWidget(self.evi_button)
        fourth_layout.addWidget(self.b_button)
        fourth_layout.addWidget(self.g_button)
        fourth_layout.addWidget(self.d_button)
        fourth_layout.addWidget(self.a_button)
        fourth_layout.addWidget(self.ei_button)

        third_layout.addLayout(fourth_layout)
        third_layout.addWidget(fretboard_image)

        second_layout.addLayout(third_layout)
        second_layout.addWidget(self.calibrate_guitar_button)
        second_layout.addWidget(sheet_zone)
        # second_layout.addWidget(self.label)

        first_layout.addLayout(second_layout)
        first_layout.setAlignment(second_layout, Qt.AlignCenter)   

        self.calibrate_guitar_thread = None
        self.loop = QEventLoop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.c_neutral_white)
        painter.drawLine(100, 100, 1000, 5000)
        painter.end()

    def calibrate_guitar(self):
        self.bounds_list = []

        string_evi = 'evi'
        string_b = 'b'
        string_g = 'g'
        string_d = 'd'
        string_a = 'a'
        string_ei = 'ei'

        # animate calibrate guitar button
        self.calibrate_guitar_button.tuning_start()

        # evi button
        self.evi_button.tuning_start() #animate
        self.calibrate_guitar_calculate(string_evi) #calculate
        print("calibrated evi")
        self.evi_button.tuning_end()

        # b button
        self.b_button.tuning_start()
        self.calibrate_guitar_calculate(string_b)
        print("calibrated b")
        self.b_button.tuning_end()

        # g button
        self.g_button.tuning_start()
        self.calibrate_guitar_calculate(string_g) #calculate
        print("calibrated g")
        self.g_button.tuning_end()

        # d button
        self.d_button.tuning_start()
        self.calibrate_guitar_calculate(string_d) #calculate
        print("calibrated d")
        self.d_button.tuning_end()

        # a button
        self.a_button.tuning_start()
        self.calibrate_guitar_calculate(string_a) #calculate
        print("calibrated a")
        self.a_button.tuning_end()

        # ei button
        self.ei_button.tuning_start()
        self.calibrate_guitar_calculate(string_ei) #calculate
        print("calibrated ei")
        self.ei_button.tuning_end()

        self.calibrate_guitar_button.tuning_end()
        print(self.bounds_list)

    def calibrate_guitar_calculate(self, string):
        self.calibrate_guitar_thread = CalibrateGuitar(string)
        self.calibrate_guitar_thread.finished.connect(self.stop_calib_temp)
        self.calibrate_guitar_thread.start()
        self.loop.exec()

    def stop_calib_temp(self, result):
        print("finished signal worked")
        self.bounds_list.append(result)
        print(result)
        self.loop.quit()

    def start_reset(self):
        self.note_list = self.generate_notes()
        self.checker_thread = SoundProcessing(mode_list=self.string_check.mode_list, bound_list=self.bounds_list, note_list=self.note_list)
        #develop sound processing
        pass

    def generate_notes(self): #generate and draw the notes
        self.string_check.key_str_list
        for i in range(50, self.sheet_height, 150):
            for h_line in np.linspace(0, 100, 6).tolist():
                paint = DrawNote(text=, position=, state=)
                painter = QPainter(self)
                painter.drawLine(25, i + h_line, self.sheet_width - 25, i + h_line)
        for i in range(1,48):

            pass

class TextButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        self.c_background_black = QColor(50, 50, 51)
        self.c_neutral_grey = QColor(97, 98, 102)
        self.c_neutral_white = QColor(181, 182, 188)
        self.c_highlight_pastelgold = QColor(222, 205, 135)

        self.text = text

        self.setFlat(True)
        self.setText(self.text)

        self.setMinimumSize(self.sizeHint())
        self.setMaximumSize(self.sizeHint())

        #default look
        self.setStyleSheet(f"""
            border: none;
            text-align: center;
            text-decoration: none;
            color: {self.c_neutral_grey.name()};
            font-family: Calibri;
            font-size: 13px;
            font-weight: light;
            margin: 0px;
            padding: 0px;
                           """)
        
        self.anim_letter = QVariantAnimation(self)
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
                color: {color.name()};
                font-family: Calibri;
                font-size: 13px;
                font-weight: regular;
                margin: 0px;
                padding: 0px;
                            """)

        self.anim_letter.setStartValue(QColor(self.c_neutral_grey.name()))
        self.anim_letter.setEndValue(QColor(self.c_neutral_white.name()))
        self.anim_letter.setDuration(250)
        self.anim_letter.valueChanged.connect(set_style_sheet)
        self.anim_letter.start()

    def button_leave_event(self, event):
        def set_style_sheet(color):
            self.setStyleSheet(f"""
                border: none;
                text-align: center;
                text-decoration: none;
                color: {color.name()};
                font-family: Calibri;
                font-size: 13px;
                font-weight: regular;
                margin: 0px;
                padding: 0px;
                            """)

        if self.isChecked():
            self.anim_letter.valueChanged.connect(set_style_sheet)

        else:
            self.anim_letter.setStartValue(QColor(self.c_neutral_white.name()))
            self.anim_letter.setEndValue(QColor(self.c_neutral_grey.name()))
            self.anim_letter.setDuration(250)

            self.anim_letter.valueChanged.connect(set_style_sheet)
            self.anim_letter.start()

    def pressed_animation(self):
        def set_style_sheet(color):
            self.setStyleSheet(f"""
                border: none;
                text-align: center;
                text-decoration: none;
                color: {color.name()};
                font-family: Calibri;
                font-size: 13px;
                font-weight: light;
                margin: 0px;
                padding: 0px;
                            """)

        self.anim_letter.setStartValue(QColor(self.c_neutral_white.name()))
        self.anim_letter.setEndValue(QColor(self.c_neutral_grey.name()))
        self.anim_letter.setDuration(100)
        self.anim_letter.valueChanged.connect(set_style_sheet)
        self.anim_letter.start()

    def release_animation(self):
        def set_style_sheet(color):
            self.setStyleSheet(f"""
                border: none;
                text-align: center;
                text-decoration: none;
                color: {color.name()};
                font-family: Calibri;
                font-size: 13px;
                font-weight: light;
                margin: 0px;
                padding: 0px;
                            """)

        self.anim_letter.setStartValue(QColor(self.c_neutral_grey.name()))
        self.anim_letter.setEndValue(QColor(self.c_neutral_white.name()))
        self.anim_letter.setDuration(100)
        self.anim_letter.valueChanged.connect(set_style_sheet)
        self.anim_letter.start()

    def button_click(self, checked):
        print("button clicked", checked)

    def tuning_start(self):
        def set_style_sheet(color):
            self.setStyleSheet(f"""
                border: none;
                text-align: center;
                text-decoration: none;
                color: {color.name()};
                font-family: Calibri;
                font-size: 13px;
                font-weight: light;
                margin: 0px;
                padding: 0px;
                            """)

        self.anim_letter.setStartValue(QColor(self.c_neutral_white.name()))
        self.anim_letter.setEndValue(QColor(self.c_highlight_pastelgold.name()))
        self.anim_letter.setDuration(100)
        self.anim_letter.valueChanged.connect(set_style_sheet)
        self.anim_letter.start()

    def tuning_end(self):
        def set_style_sheet(color):
            self.setStyleSheet(f"""
                border: none;
                text-align: center;
                text-decoration: none;
                color: {color.name()};
                font-family: Calibri;
                font-size: 13px;
                font-weight: light;
                margin: 0px;
                padding: 0px;
                            """)

        self.anim_letter.setStartValue(QColor(self.c_highlight_pastelgold.name()))
        self.anim_letter.setEndValue(QColor(self.c_neutral_white.name()))
        self.anim_letter.setDuration(100)
        self.anim_letter.valueChanged.connect(set_style_sheet)
        self.anim_letter.start()

class NoteButton(QPushButton):
    def __init__(self, size, text, roundness, parent=None):
        super().__init__(parent)

        self.setFlat(True)

        self.size = size
        self.text = text

        self.c_background_black = QColor(50, 50, 51)
        self.c_neutral_grey = QColor(97, 98, 102)
        self.c_neutral_white = QColor(181, 182, 188)
        self.c_highlight_pastelgold = QColor(222, 205, 135)
        self.c_highlight_crimsonred = QColor(180, 75, 67)

        self.roundness = roundness

        self.setText(self.text)
        self.setStyleSheet(f"""
            border: none;
            text-align: center;
            text-decoration: none;
            border-radius: {self.roundness}px;
            background-color: {self.c_neutral_grey.name()};
            color: {self.c_background_black.name()};
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
            color: {self.c_background_black.name()};
            font-family: Calibri;
            font-size: 15px;
            font-weight: bold;
            margin: 0px;
            padding: 0px;
                           """)

        self.anim_background.setStartValue(QColor(self.c_neutral_grey.name()))
        self.anim_background.setEndValue(QColor(self.c_neutral_white.name()))
        self.anim_background.setDuration(250)
        self.anim_background.valueChanged.connect(set_style_sheet)
        self.anim_background.start()

    def button_leave_event(self, event):
        def set_style_sheet():
            letter_colour = self.letter_col
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
            self.anim_background.setStartValue(QColor(self.c_neutral_white.name()))
            self.anim_background.setEndValue(QColor(self.c_neutral_grey.name()))
            self.anim_background.setDuration(250)
            self.anim_background.valueChanged.connect(set_style_sheet)
            self.anim_background.start()

            self.letter_col = self.c_neutral_white.name()

        else:
            self.anim_background.setStartValue(QColor(self.c_neutral_white.name()))
            self.anim_background.setEndValue(QColor(self.c_neutral_grey.name()))
            self.anim_background.setDuration(250)
            self.anim_background.valueChanged.connect(set_style_sheet)
            self.anim_background.start()

            self.letter_col = self.c_background_black.name()

    def pressed_animation(self):

        def set_style_sheet(colour):
                self.setStyleSheet(f"""
                border: none;
                text-align: center;
                text-decoration: none;
                border-radius: {self.roundness}px;
                background-color: {colour.name()};;
                color: {self.c_background_black.name()};
                font-family: Calibri;
                font-size: 15px;
                font-weight: bold;
                margin: 0px;
                padding: 0px;
                            """)

        self.anim_background.setStartValue(QColor(self.c_neutral_white.name()))
        self.anim_background.setEndValue(QColor(self.c_neutral_grey.name()))
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
                color: {self.c_background_black.name()};
                font-family: Calibri;
                font-size: 15px;
                font-weight: bold;
                margin: 0px;
                padding: 0px;
                            """)

        self.anim_background.setStartValue(QColor(self.c_neutral_grey.name()))
        self.anim_background.setEndValue(QColor(self.c_neutral_white.name()))
        self.anim_background.setDuration(100)
        self.anim_background.valueChanged.connect(set_style_sheet)
        self.anim_background.start()

    def button_click(self, checked):
        print("button clicked", checked)

    def tuning_start(self):
        def set_style_sheet(color):
            letter_colour = self.tunings_col
            self.setStyleSheet(f"""
            border: none;
            text-align: center;
            text-decoration: none;
            border-radius: {self.roundness}px;
            background-color: {color.name()};
            color: {letter_colour};
            font-family: Calibri;
            font-size: 15px;
            font-weight: bold;
            margin: 0px;
            padding: 0px;
                        """)
        
        if self.isChecked() == True:
            self.tunings_col = self.c_neutral_white.name()

        elif self.isChecked() == False:
            self.tunings_col = self.c_background_black.name()
            

        self.anim_background.setStartValue(QColor(self.c_neutral_grey.name()))
        self.anim_background.setEndValue(QColor(self.c_highlight_pastelgold.name()))
        self.anim_background.setDuration(250)
        self.anim_background.valueChanged.connect(set_style_sheet)
        self.anim_background.start()


    def tuning_end(self):
        def set_style_sheet(color):
            letter_colour = self.tuninge_col
            self.setStyleSheet(f"""
            border: none;
            text-align: center;
            text-decoration: none;
            border-radius: {self.roundness}px;
            background-color: {color.name()};
            color: {letter_colour};
            font-family: Calibri;
            font-size: 15px;
            font-weight: bold;
            margin: 0px;
            padding: 0px;
                        """)
            
        if self.isChecked() == True:
            self.tuninge_col = self.c_neutral_white.name()

        elif self.isChecked() == False:
            self.tuninge_col = self.c_background_black.name()

        self.anim_background.setStartValue(QColor(self.c_highlight_pastelgold.name()))
        self.anim_background.setEndValue(QColor(self.c_neutral_grey.name()))
        self.anim_background.setDuration(250)
        self.anim_background.valueChanged.connect(set_style_sheet)
        self.anim_background.start()

class SheetWindow(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)

        self.c_background_black = QColor(50, 50, 51)
        self.c_neutral_grey = QColor(97, 98, 102)
        self.c_neutral_white = QColor(181, 182, 188)

        self.setMinimumSize(width, height)
        self.sheet_height = height
        self.sheet_width = width
        self.initsheetlines()

    def initsheetlines(self):
        self.pixmap = QPixmap(self.sheet_width, self.sheet_height)
        self.pixmap.fill(self.c_background_black)

        painter = QPainter(self.pixmap)
        painter.setPen(QPen(self.c_neutral_grey, 0.75, Qt.SolidLine))

        for i in range(50, self.sheet_height, 150):
            for h_line in np.linspace(0, 100, 6).tolist():
                painter.drawLine(25, i + h_line, self.sheet_width - 25, i + h_line)
        painter.end()

        painter_2 = QPainter(self.pixmap)
        painter_2.setPen(QPen(self.c_neutral_grey, 0.25, Qt.SolidLine))

        for i in range(50, self.sheet_height, 150):
            for v_line in np.linspace(25, self.sheet_width - 25, 24):
                painter_2.drawLine(v_line, i, v_line, i + 100)
        painter_2.end()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)

class OutlinedLabel(QLabel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.w = 1 / 25
        self.mode = True
        self.setBrush(Qt.white)
        self.setPen(Qt.black)

    def scaledOutlineMode(self):
        return self.mode

    def setScaledOutlineMode(self, state):
        self.mode = state

    def outlineThickness(self):
        return self.w * self.font().pointSize() if self.mode else self.w

    def setOutlineThickness(self, value):
        self.w = value

    def setBrush(self, brush):
        if not isinstance(brush, QBrush):
            brush = QBrush(brush)
        self.brush = brush

    def setPen(self, pen):
        if not isinstance(pen, QPen):
            pen = QPen(pen)
        pen.setJoinStyle(Qt.RoundJoin)
        self.pen = pen

    def sizeHint(self):
        w = math.ceil(self.outlineThickness() * 2)
        return super().sizeHint() + QSize(w, w)
    
    def minimumSizeHint(self):
        w = math.ceil(self.outlineThickness() * 2)
        return super().minimumSizeHint() + QSize(w, w)
    
    def paintEvent(self, event):
        w = self.outlineThickness()
        rect = self.rect()
        metrics = QFontMetrics(self.font())
        tr = metrics.boundingRect(self.text()).adjusted(0, 0, w, w)
        if self.indent() == -1:
            if self.frameWidth():
                indent = (metrics.boundingRect('x').width() + w * 2) / 2
            else:
                indent = w
        else:
            indent = self.indent()

        if self.alignment() & Qt.AlignLeft:
            x = rect.left() + indent - min(metrics.leftBearing(self.text()[0]), 0)
        elif self.alignment() & Qt.AlignRight:
            x = rect.x() + rect.width() - indent - tr.width()
        else:
            x = (rect.width() - tr.width()) / 2
            
        if self.alignment() & Qt.AlignTop:
            y = rect.top() + indent + metrics.ascent()
        elif self.alignment() & Qt.AlignBottom:
            y = rect.y() + rect.height() - indent - metrics.descent()
        else:
            y = (rect.height() + metrics.ascent() - metrics.descent()) / 2

        path = QPainterPath()
        path.addText(x, y, self.font(), self.text())
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)

        self.pen.setWidthF(w * 2)
        qp.strokePath(path, self.pen)
        if 1 < self.brush.style() < 15:
            qp.fillPath(path, self.palette().window())
        qp.fillPath(path, self.brush)

class DrawNote(QLabel):
    def __init__(self, text, position, state, parent=None):
        super().__init__(parent)

        self.c_background_black = QColor(50, 50, 51)
        self.c_neutral_grey = QColor(97, 98, 102)
        self.c_neutral_white = QColor(181, 182, 188)
        self.c_highlight_pastelgold = QColor(222, 205, 135)
        self.c_highlight_crimsonred = QColor(180, 75, 67)

        self.text = text

        note = OutlinedLabel(self.text, alignemnt=Qt.AlignCenter)
        note.setStyleSheet(
            '''
            font-family: Calibri; 
            font-size: 15px;
            font-weight: light;
            '''
        )

        note.setPen(self.c_background_black.name()) #Qt colour
        note.setBrush(self.c_neutral_grey.name()) #Qt colour

    def update_note(state):
        pass





#Qapplication instance
app = QApplication([])

#Widgets
window = MainWindow()
window.show()

#Event loop
app.exec()
