from PySide6.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve, Signal, Property, QParallelAnimationGroup, QThread, Signal, QEventLoop
from PySide6.QtWidgets import QApplication, QWidget, QSpacerItem, QPushButton, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QSizePolicy
from PySide6.QtGui import QPaintEvent, QPixmap, QPainter, QColor, QIcon, QResizeEvent, QPen, QBrush, QFont, QPalette, QPen, QFontMetrics, QPainterPath
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import QVariantAnimation

import math
import numpy as np
import threading
import time
import queue
import random

from sound_processing import StringPicker, CalibrateGuitar, SoundProcessing, StandardBounds, AutoScroll

#Layout the widgets properly
#Create autoscroll
#Update start/reset button to reset the sheetwindow
#Create an executable


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

        #Default bounds:
        self.starter_bounds = StandardBounds()
        self.bounds_list = self.starter_bounds.bounds_list

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
        self.sheet_zone = QScrollArea()
        self.sheet_zone.setWidgetResizable(True)

        self.string_check = StringPicker()

        self.sheet_widget = SheetWindow(width=1500, height=5000, 
                                   key_list=self.string_check.key_list, 
                                   key_str_list=self.string_check.key_str_list, 
                                   mode_list=self.string_check.mode_list,
                                   bound_list=self.bounds_list)
        self.sheet_zone.setWidget(self.sheet_widget)
        self.sheet_zone.setFixedSize(QSize(1500, 475))

        self.sheet_zone.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) #scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.sheet_zone.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)#scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        

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

        self.calibrate_guitar_button = TextButton(text='Calibrate')

        self.start_reset_button = StartButton(text='Start|Reset')

        self.numbers_button = TextButton(text='Numbers')

        self.letters_button = TextButton(text='Letters')

        #Button Functions
        self.evi_button.clicked.connect(self.string_check.click_evi)
        self.b_button.clicked.connect(self.string_check.click_b)
        self.g_button.clicked.connect(self.string_check.click_g)
        self.d_button.clicked.connect(self.string_check.click_d)
        self.a_button.clicked.connect(self.string_check.click_a)
        self.ei_button.clicked.connect(self.string_check.click_ei)

        self.calibrate_guitar_button.clicked.connect(self.calibrate_guitar)

        self.start_reset_button.clicked.connect(self.sheet_widget.start_reset)
        self.start_reset_button.clicked.connect(self.auto_scroll)

        self.numbers_button.clicked.connect(self.sheet_widget.number_actuator)
        self.letters_button.clicked.connect(self.sheet_widget.letter_actuator)

        #Layouts

        first_layout = QVBoxLayout(background_widget)
        first_layout.setContentsMargins(0, 0, 0, 100)
        first_layout.setSpacing(0)

        second_layout = QVBoxLayout()
        second_layout.setContentsMargins(0, 0, 0, 0)
        second_layout.setSpacing(10)

        third_layout = QHBoxLayout()
        third_layout.setContentsMargins(0, 0, 300, -50)
        third_layout.setSpacing(0)

        fourth_layout = QVBoxLayout()
        fourth_layout.setContentsMargins(300, 10, 0, 25) #0, 0, 0, 23
        fourth_layout.setSpacing(0)

        fourth_layout.addWidget(self.evi_button)
        fourth_layout.addWidget(self.b_button)
        fourth_layout.addWidget(self.g_button)
        fourth_layout.addWidget(self.d_button)
        fourth_layout.addWidget(self.a_button)
        fourth_layout.addWidget(self.ei_button)

        self.evi_button.move(50, 50)

        third_layout.addLayout(fourth_layout)
        third_layout.addWidget(fretboard_image)

        text_button_layout = QHBoxLayout()
        text_button_layout.setContentsMargins(400, 0, 500, 0)
        text_button_layout.setSpacing(0)

        text_button_layout.addWidget(self.start_reset_button)
        text_button_layout.addWidget(self.calibrate_guitar_button)
        text_button_layout.addWidget(self.numbers_button)
        text_button_layout.addWidget(self.letters_button)

        second_layout.addLayout(third_layout)
        second_layout.addLayout(text_button_layout)
        second_layout.addWidget(self.sheet_zone)
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

    def auto_scroll(self):
        self.auto_scroll_thread = AutoScroll(current_idx=self.sheet_widget.note_idx, step_idx=5)
        self.auto_scroll_thread.update.connect(self.scroll)
        self.auto_scroll_thread.start()

    def scroll(self, result):
        print(f'scroll {result}')

        if result:
            current_value = self.sheet_zone.verticalScrollBar().value()
            self.sheet_zone.verticalScrollBar().setValue(current_value + 475)

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

class StartButton(QPushButton):
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

        #qt sends a signal as enter event, it's assignes to function button _enter event
        self.enterEvent = self.button_enter_event
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
    def __init__(self, width, height, key_list, key_str_list, mode_list, bound_list, parent=None):
        super().__init__(parent)

        self.key_list = key_list
        self.key_str_list = key_str_list
        self.mode_list = mode_list
        self.bound_list = bound_list
        

        self.c_background_black = QColor(50, 50, 51)
        self.c_neutral_grey = QColor(97, 98, 102)
        self.c_neutral_white = QColor(181, 182, 188)
        self.c_highlight_pastelgold = QColor(222, 205, 135)
        self.c_highlight_crimsonred = QColor(180, 75, 67)

        self.setMinimumSize(width, height)
        self.sheet_height = height
        self.sheet_width = width
        self.current_pitch = 0
        self.note_idx = 0

        self.text_state = False
        self.number_state = False

        self.initsheetlines()

    def initsheetlines(self):

        self.pixmap = QPixmap(self.sheet_width, self.sheet_height)
        self.pixmap.fill(self.c_background_black)

        painter = QPainter(self.pixmap)
        painter.setPen(QPen(self.c_neutral_grey, 0.75, Qt.SolidLine))

        self.ycoor = range(50, self.sheet_height, 150)
        self.xcoor = np.linspace(25, self.sheet_width - 25, 24)

        self.stringcoor = np.linspace(0, 100, 6)

        self.length = len(self.ycoor)
        
        for i in self.ycoor:
            for h_line in self.stringcoor:
                painter.drawLine(25, i + h_line, self.sheet_width - 25, i + h_line)
        painter.end()

        painter_2 = QPainter(self.pixmap)
        painter_2.setPen(QPen(self.c_neutral_grey, 0.25, Qt.SolidLine))

        for i in self.ycoor:
            for v_line in self.xcoor:
                painter_2.drawLine(v_line, i, v_line, i + 100)
        painter_2.end()

    def start_reset(self):
        self.generate_notes()
        print(f'text state {self.text_state}')
        print(f'number state {self.number_state}')
        self.start_recording()

    def generate_notes(self): #generate and draw the notes
        #key values

        key_array = np.array(self.key_list)
        key_list_f = key_array.flatten()

        #key names
        self.key_str_array = np.array(self.key_str_list)
        key_str_list_f = self.key_str_array.flatten()

        random_list = list(range(len(key_str_list_f)))

        # generate a random key list
        self.rng_note_list = []

        note_nr = self.length * 23
        for i in range(note_nr):
            random.shuffle(random_list)
            random_idx = random_list[0]
            random_key_str = key_str_list_f[random_idx]
            self.rng_note_list.append(random_key_str)

        for idx, random_key_str in enumerate(self.rng_note_list):

            position = self.key_position(idx=idx, string=random_key_str)

            painter = QPainter(self.pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            font = QFont("Calibri", 12, weight=500)
            painter.setFont(font)
            self.text = self.text_sorter(random_key_str)

            path = QPainterPath()
            path.addText(int(position[0]), int(position[1]), font, self.text)

            # outline_pen = QPen(self.c_background_black, 5, Qt.SolidLine)
            painter.strokePath(path, QPen(self.c_background_black, 10, Qt.SolidLine))

            # Draw text fill
            painter.setPen(QPen(self.c_neutral_grey, 0.25, Qt.SolidLine))
            painter.drawText(int(position[0]), int(position[1]), self.text)
            painter.end()

    def start_recording(self):
        self.recording_thread = SoundProcessing(mode_list=self.mode_list, 
                                                bound_list = self.bound_list, 
                                                note_list=self.rng_note_list)
        self.recording_thread.update.connect(self.recording_result)
        self.recording_thread.start()

    def recording_result(self, result):
        self.current_key = result
        # print(result)

        if result == True:
            # print(self.note_idx)
            position = self.key_position(idx=self.note_idx, string=self.rng_note_list[self.note_idx])

            painter = QPainter(self.pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            font = QFont("Calibri", 12, weight=500)
            painter.setFont(font)
            self.text = self.text_sorter(self.rng_note_list[self.note_idx])

            path = QPainterPath()
            path.addText(int(position[0]), int(position[1]), font, self.text)

            # outline_pen = QPen(self.c_background_black, 5, Qt.SolidLine)
            painter.strokePath(path, QPen(self.c_background_black, 10, Qt.SolidLine))

            # Draw text fill
            painter.setPen(QPen(self.c_neutral_white, 0.25, Qt.SolidLine))
            painter.drawText(int(position[0]), int(position[1]), self.text)
            painter.end()

            self.note_idx += 1
            print(self.note_idx)

        if result == False:
            # print(self.note_idx)
            position = self.key_position(idx=self.note_idx, string=self.rng_note_list[self.note_idx])

            painter = QPainter(self.pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            font = QFont("Calibri", 12, weight=500)
            painter.setFont(font)
            self.text = self.text_sorter(self.rng_note_list[self.note_idx])

            path = QPainterPath()
            path.addText(int(position[0]), int(position[1]), font, self.text)

            # outline_pen = QPen(self.c_background_black, 5, Qt.SolidLine)
            painter.strokePath(path, QPen(self.c_background_black, 10, Qt.SolidLine))

            # Draw text fill
            painter.setPen(QPen(self.c_highlight_crimsonred, 0.25, Qt.SolidLine))
            painter.drawText(int(position[0]), int(position[1]), self.text)
            painter.end()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)
        self.update()

    def key_position(self, idx, string):

        y_idx = idx // 23
        x_idx = idx % 23

        #get position for notes

        if string[0] == 'i' and string[1] != 'i':
            position_x = self.xcoor[x_idx] + self.xcoor[0]
            position_y = self.ycoor[y_idx] + self.stringcoor[0]

        elif string[0] == 'i' and string[1] == 'i' and string[2] != 'i':
            position_x = self.xcoor[x_idx] + self.xcoor[0]
            position_y = self.ycoor[y_idx] + self.stringcoor[1]

        elif string[0] == 'i' and string[1] == 'i' and string[2] == 'i':
            position_x = self.xcoor[x_idx] + self.xcoor[0]
            position_y = self.ycoor[y_idx] + self.stringcoor[2]

        elif string[0] == 'i' and string[1] == 'v':
            position_x = self.xcoor[x_idx] + self.xcoor[0]
            position_y = self.ycoor[y_idx] + self.stringcoor[3]

        elif string[0] == 'v' and string[1] != 'i':
            position_x = self.xcoor[x_idx] + self.xcoor[0]
            position_y = self.ycoor[y_idx] + self.stringcoor[4]

        elif string[0] == 'v' and string[1] == 'i':
            position_x = self.xcoor[x_idx] + self.xcoor[0]
            position_y = self.ycoor[y_idx] + self.stringcoor[5]

        else:
            pass

        return (position_x, position_y)

    def number_actuator(self):
        if self.number_state == True:
            self.number_state = False

        elif self.number_state == False:
            self.number_state = True

        else:
            pass

    def letter_actuator(self):
        if self.text_state == True:
            self.text_state = False

        elif self.text_state == False:
            self.text_state = True

        else:
            pass

    def text_sorter(self, note):
        if self.number_state == True and self.text_state == True:
            
            if note[0] == 'i' and note[1] != 'i': #i_A#
                index = 2

                if note[index] == 'E':
                    output = f'0 {note[index:]}'

                if note[index] == 'F':
                    output = f'1 {note[index:]}'

                if note[index] == 'F#':
                    output = f'2 {note[index:]}'

                if note[index] == 'G':
                    output = f'3 {note[index:]}'

                if note[index] == 'G#':
                    output = f'4 {note[index:]}'

                if note[index] == 'A':
                    output = f'5 {note[index:]}'

                if note[index] == 'A#':
                    output = f'6 {note[index:]}'

                if note[index] == 'B':
                    output = f'7 {note[index:]}'

                if note[index] == 'C':
                    output = f'8 {note[index:]}'

                if note[index] == 'C#':
                    output = f'9 {note[index:]}'

                if note[index] == 'D':
                    output = f'10 {note[index:]}'

                if note[index] == 'D#':
                    output = f'11 {note[index:]}'

                if note[index] == 'e':
                    output = f'12 {note[index:]}'

                if note[index] == 'f':
                    output = f'13 {note[index:]}'

                if note[index] == 'f#':
                    output = f'14 {note[index:]}'

                if note[index] == 'g':
                    output = f'15 {note[index:]}'

                if note[index] == 'g#':
                    output = f'16 {note[index:]}'

                if note[index] == 'a':
                    output = f'17 {note[index:]}'

                if note[index] == 'a#':
                    output = f'18 {note[index:]}'

                if note[index] == 'b':
                    output = f'19 {note[index:]}'

                if note[index] == 'c':
                    output = f'20 {note[index:]}'

                if note[index] == 'c#':
                    output = f'21 {note[index:]}'

                if note[index] == 'd':
                    output = f'22 {note[index:]}'
                
                if note[index] == 'd#':
                    output = f'23 {note[index:]}'

            elif note[0] == 'i' and note[1] == 'i' and note[2] != 'i':
                index = 3

                if note[index] == 'B':
                    output = f'0 {note[index:]}'

                if note[index] == 'C':
                    output = f'1 {note[index:]}'

                if note[index] == 'C#':
                    output = f'2 {note[index:]}'

                if note[index] == 'D':
                    output = f'3 {note[index:]}'

                if note[index] == 'D#':
                    output = f'4 {note[index:]}'

                if note[index] == 'E':
                    output = f'5 {note[index:]}'

                if note[index] == 'F':
                    output = f'6 {note[index:]}'

                if note[index] == 'F#':
                    output = f'7 {note[index:]}'

                if note[index] == 'G':
                    output = f'8 {note[index:]}'

                if note[index] == 'G#':
                    output = f'9 {note[index:]}'

                if note[index] == 'A':
                    output = f'10 {note[index:]}'

                if note[index] == 'A#':
                    output = f'11 {note[index:]}'

                if note[index] == 'b':
                    output = f'12 {note[index:]}'

                if note[index] == 'c':
                    output = f'13 {note[index:]}'

                if note[index] == 'c#':
                    output = f'14 {note[index:]}'

                if note[index] == 'd':
                    output = f'15 {note[index:]}'
                
                if note[index] == 'd#':
                    output = f'16 {note[index:]}'

                if note[index] == 'e':
                    output = f'17 {note[index:]}'

                if note[index] == 'f':
                    output = f'18 {note[index:]}'

                if note[index] == 'f#':
                    output = f'19 {note[index:]}'

                if note[index] == 'g':
                    output = f'20 {note[index:]}'

                if note[index] == 'g#':
                    output = f'21 {note[index:]}'

                if note[index] == 'a':
                    output = f'22 {note[index:]}'

                if note[index] == 'a#':
                    output = f'23 {note[index:]}'

            elif note[0] == 'i' and note[1] == 'i' and note[2] == 'i':
                index = 4

                if note[index] == 'G':
                    output = f'0 {note[index:]}'

                if note[index] == 'G#':
                    output = f'1 {note[index:]}'

                if note[index] == 'A':
                    output = f'2 {note[index:]}'

                if note[index] == 'A#':
                    output = f'3 {note[index:]}'

                if note[index] == 'B':
                    output = f'4 {note[index:]}'

                if note[index] == 'C':
                    output = f'5 {note[index:]}'

                if note[index] == 'C#':
                    output = f'6 {note[index:]}'

                if note[index] == 'D':
                    output = f'7 {note[index:]}'

                if note[index] == 'D#':
                    output = f'8 {note[index:]}'

                if note[index] == 'E':
                    output = f'9 {note[index:]}'

                if note[index] == 'F':
                    output = f'10 {note[index:]}'

                if note[index] == 'F#':
                    output = f'11 {note[index:]}'

                if note[index] == 'g':
                    output = f'12 {note[index:]}'

                if note[index] == 'g#':
                    output = f'13 {note[index:]}'

                if note[index] == 'a':
                    output = f'14 {note[index:]}'

                if note[index] == 'a#':
                    output = f'15 {note[index:]}'

                if note[index] == 'b':
                    output = f'16 {note[index:]}'

                if note[index] == 'c':
                    output = f'17 {note[index:]}'

                if note[index] == 'c#':
                    output = f'18 {note[index:]}'

                if note[index] == 'd':
                    output = f'19 {note[index:]}'
                
                if note[index] == 'd#':
                    output = f'20 {note[index:]}'

                if note[index] == 'e':
                    output = f'21 {note[index:]}'

                if note[index] == 'f':
                    output = f'22 {note[index:]}'

                if note[index] == 'f#':
                    output = f'23 {note[index:]}'

            elif note[0] == 'i' and note[1] == 'v':
                index = 3

                if note[index] == 'D':
                    output = f'0 {note[index:]}'

                if note[index] == 'D#':
                    output = f'1 {note[index:]}'

                if note[index] == 'E':
                    output = f'2 {note[index:]}'

                if note[index] == 'F':
                    output = f'3 {note[index:]}'

                if note[index] == 'F#':
                    output = f'4 {note[index:]}'

                if note[index] == 'G':
                    output = f'5 {note[index:]}'

                if note[index] == 'G#':
                    output = f'6 {note[index:]}'

                if note[index] == 'A':
                    output = f'7 {note[index:]}'

                if note[index] == 'A#':
                    output = f'8 {note[index:]}'

                if note[index] == 'B':
                    output = f'9 {note[index:]}'

                if note[index] == 'C':
                    output = f'10 {note[index:]}'

                if note[index] == 'C#':
                    output = f'11 {note[index:]}'

                if note[index] == 'd':
                    output = f'12 {note[index:]}'
                
                if note[index] == 'd#':
                    output = f'13 {note[index:]}'

                if note[index] == 'e':
                    output = f'14 {note[index:]}'

                if note[index] == 'f':
                    output = f'15 {note[index:]}'

                if note[index] == 'f#':
                    output = f'16 {note[index:]}'

                if note[index] == 'g':
                    output = f'17 {note[index:]}'

                if note[index] == 'g#':
                    output = f'18 {note[index:]}'

                if note[index] == 'a':
                    output = f'19 {note[index:]}'

                if note[index] == 'a#':
                    output = f'20 {note[index:]}'

                if note[index] == 'b':
                    output = f'21 {note[index:]}'

                if note[index] == 'c':
                    output = f'22 {note[index:]}'

                if note[index] == 'c#':
                    output = f'23 {note[index:]}'

            elif note[0] == 'v' and note[1] != 'i':
                index = 2

                if note[index] == 'A':
                    output = f'0 {note[index:]}'

                if note[index] == 'A#':
                    output = f'1 {note[index:]}'

                if note[index] == 'B':
                    output = f'2 {note[index:]}'

                if note[index] == 'C':
                    output = f'3 {note[index:]}'

                if note[index] == 'C#':
                    output = f'4 {note[index:]}'

                if note[index] == 'D':
                    output = f'5 {note[index:]}'

                if note[index] == 'D#':
                    output = f'6 {note[index:]}'

                if note[index] == 'E':
                    output = f'7 {note[index:]}'

                if note[index] == 'F':
                    output = f'8 {note[index:]}'

                if note[index] == 'F#':
                    output = f'9 {note[index:]}'

                if note[index] == 'G':
                    output = f'10 {note[index:]}'

                if note[index] == 'G#':
                    output = f'11 {note[index:]}'

                if note[index] == 'a':
                    output = f'12 {note[index:]}'

                if note[index] == 'a#':
                    output = f'13 {note[index:]}'

                if note[index] == 'b':
                    output = f'14 {note[index:]}'

                if note[index] == 'c':
                    output = f'15 {note[index:]}'

                if note[index] == 'c#':
                    output = f'16 {note[index:]}'

                if note[index] == 'd':
                    output = f'17 {note[index:]}'
                
                if note[index] == 'd#':
                    output = f'18 {note[index:]}'

                if note[index] == 'e':
                    output = f'19 {note[index:]}'

                if note[index] == 'f':
                    output = f'20 {note[index:]}'

                if note[index] == 'f#':
                    output = f'21 {note[index:]}'

                if note[index] == 'g':
                    output = f'22 {note[index:]}'

                if note[index] == 'g#':
                    output = f'23 {note[index:]}'

            elif note[0] == 'v' and note[1] == 'i':
                index = 3

                if note[index] == 'E':
                    output = f'0 {note[index:]}'

                if note[index] == 'F':
                    output = f'1 {note[index:]}'

                if note[index] == 'F#':
                    output = f'2 {note[index:]}'

                if note[index] == 'G':
                    output = f'3 {note[index:]}'

                if note[index] == 'G#':
                    output = f'4 {note[index:]}'

                if note[index] == 'A':
                    output = f'5 {note[index:]}'

                if note[index] == 'A#':
                    output = f'6 {note[index:]}'

                if note[index] == 'B':
                    output = f'7 {note[index:]}'

                if note[index] == 'C':
                    output = f'8 {note[index:]}'

                if note[index] == 'C#':
                    output = f'9 {note[index:]}'

                if note[index] == 'D':
                    output = f'10 {note[index:]}'

                if note[index] == 'D#':
                    output = f'11 {note[index:]}'

                if note[index] == 'e':
                    output = f'12 {note[index:]}'

                if note[index] == 'f':
                    output = f'13 {note[index:]}'

                if note[index] == 'f#':
                    output = f'14 {note[index:]}'

                if note[index] == 'g':
                    output = f'15 {note[index:]}'

                if note[index] == 'g#':
                    output = f'16 {note[index:]}'

                if note[index] == 'a':
                    output = f'17 {note[index:]}'

                if note[index] == 'a#':
                    output = f'18 {note[index:]}'

                if note[index] == 'b':
                    output = f'19 {note[index:]}'

                if note[index] == 'c':
                    output = f'20 {note[index:]}'

                if note[index] == 'c#':
                    output = f'21 {note[index:]}'

                if note[index] == 'd':
                    output = f'22 {note[index:]}'
                
                if note[index] == 'd#':
                    output = f'23 {note[index:]}'

        if self.number_state == True and self.text_state == False:
            
            if note[0] == 'i' and note[1] != 'i':
                index = 2

                if note[index] == 'E' and len(note) == 3:
                    output = f'0'

                if note[index] == 'F' and len(note) == 3:
                    output = f'1'

                if note[index] == 'F' and len(note) == 4:
                    output = f'2'

                if note[index] == 'G' and len(note) == 3:
                    output = f'3'

                if note[index] == 'G' and len(note) == 4:
                    output = f'4'

                if note[index] == 'A' and len(note) == 3:
                    output = f'5'

                if note[index] == 'A' and len(note) == 4:
                    output = f'6'

                if note[index] == 'B' and len(note) == 3:
                    output = f'7'

                if note[index] == 'C' and len(note) == 3:
                    output = f'8'

                if note[index] == 'C' and len(note) == 4:
                    output = f'9'

                if note[index] == 'D' and len(note) == 3:
                    output = f'10'

                if note[index] == 'D' and len(note) == 4:
                    output = f'11'

                if note[index] == 'e' and len(note) == 3:
                    output = f'12'

                if note[index] == 'f' and len(note) == 3:
                    output = f'13'

                if note[index] == 'f' and len(note) == 4:
                    output = f'14'

                if note[index] == 'g' and len(note) == 3:
                    output = f'15'

                if note[index] == 'g' and len(note) == 4:
                    output = f'16'

                if note[index] == 'a' and len(note) == 3:
                    output = f'17'

                if note[index] == 'a' and len(note) == 4:
                    output = f'18'

                if note[index] == 'b' and len(note) == 3:
                    output = f'19'

                if note[index] == 'c' and len(note) == 3:
                    output = f'20'

                if note[index] == 'c' and len(note) == 4:
                    output = f'21'

                if note[index] == 'd' and len(note) == 3:
                    output = f'22'
                
                if note[index] == 'd' and len(note) == 4:
                    output = f'23'

            elif note[0] == 'i' and note[1] == 'i' and note[2] != 'i':
                index = 3

                if note[index] == 'B' and len(note) == 3:
                    output = f'0'

                if note[index] == 'C' and len(note) == 3:
                    output = f'1'

                if note[index] == 'C' and len(note) == 4:
                    output = f'2'

                if note[index] == 'D' and len(note) == 3:
                    output = f'3'

                if note[index] == 'D' and len(note) == 4:
                    output = f'4'

                if note[index] == 'E' and len(note) == 3:
                    output = f'5'

                if note[index] == 'F' and len(note) == 3:
                    output = f'6'

                if note[index] == 'F' and len(note) == 4:
                    output = f'7'

                if note[index] == 'G' and len(note) == 3:
                    output = f'8'

                if note[index] == 'G' and len(note) == 4:
                    output = f'9'

                if note[index] == 'A' and len(note) == 3:
                    output = f'10'

                if note[index] == 'A' and len(note) == 4:
                    output = f'11'

                if note[index] == 'b' and len(note) == 3:
                    output = f'12'

                if note[index] == 'c' and len(note) == 3:
                    output = f'13'

                if note[index] == 'c' and len(note) == 4:
                    output = f'14'

                if note[index] == 'd' and len(note) == 3:
                    output = f'15'
                
                if note[index] == 'd' and len(note) == 4:
                    output = f'16'

                if note[index] == 'e' and len(note) == 3:
                    output = f'17'

                if note[index] == 'f' and len(note) == 3:
                    output = f'18'

                if note[index] == 'f' and len(note) == 4:
                    output = f'19'

                if note[index] == 'g' and len(note) == 3:
                    output = f'20'

                if note[index] == 'g' and len(note) == 4:
                    output = f'21'

                if note[index] == 'a' and len(note) == 3:
                    output = f'22'

                if note[index] == 'a' and len(note) == 4:
                    output = f'23'

            elif note[0] == 'i' and note[1] == 'i' and note[2] == 'i':
                index = 4

                if note[index] == 'G' and len(note) == 3:
                    output = f'0'

                if note[index] == 'G' and len(note) == 4:
                    output = f'1'

                if note[index] == 'A' and len(note) == 3:
                    output = f'2'

                if note[index] == 'A' and len(note) == 4:
                    output = f'3'

                if note[index] == 'B' and len(note) == 3:
                    output = f'4'

                if note[index] == 'C' and len(note) == 3:
                    output = f'5'

                if note[index] == 'C' and len(note) == 4:
                    output = f'6'

                if note[index] == 'D' and len(note) == 3:
                    output = f'7'

                if note[index] == 'D' and len(note) == 4:
                    output = f'8'

                if note[index] == 'E' and len(note) == 3:
                    output = f'9'

                if note[index] == 'F' and len(note) == 3:
                    output = f'10'

                if note[index] == 'F' and len(note) == 4:
                    output = f'11'

                if note[index] == 'g' and len(note) == 3:
                    output = f'12'

                if note[index] == 'g' and len(note) == 4:
                    output = f'13'

                if note[index] == 'a' and len(note) == 3:
                    output = f'14'

                if note[index] == 'a' and len(note) == 4:
                    output = f'15'

                if note[index] == 'b' and len(note) == 3:
                    output = f'16'

                if note[index] == 'c' and len(note) == 3:
                    output = f'17'

                if note[index] == 'c' and len(note) == 4:
                    output = f'18'

                if note[index] == 'd' and len(note) == 3:
                    output = f'19'
                
                if note[index] == 'd' and len(note) == 4:
                    output = f'20'

                if note[index] == 'e' and len(note) == 3:
                    output = f'21'

                if note[index] == 'f' and len(note) == 3:
                    output = f'22'

                if note[index] == 'f' and len(note) == 4:
                    output = f'23'

            elif note[0] == 'i' and note[1] == 'v':
                index = 3

                if note[index] == 'D' and len(note) == 3:
                    output = f'0'

                if note[index] == 'D' and len(note) == 4:
                    output = f'1'

                if note[index] == 'E' and len(note) == 3:
                    output = f'2'

                if note[index] == 'F' and len(note) == 3:
                    output = f'3'

                if note[index] == 'F' and len(note) == 4:
                    output = f'4'

                if note[index] == 'G' and len(note) == 3:
                    output = f'5'

                if note[index] == 'G' and len(note) == 4:
                    output = f'6'

                if note[index] == 'A' and len(note) == 3:
                    output = f'7'

                if note[index] == 'A' and len(note) == 4:
                    output = f'8'

                if note[index] == 'B' and len(note) == 3:
                    output = f'9'

                if note[index] == 'C' and len(note) == 3:
                    output = f'10'

                if note[index] == 'C' and len(note) == 4:
                    output = f'11'

                if note[index] == 'd' and len(note) == 3:
                    output = f'12'
                
                if note[index] == 'd' and len(note) == 4:
                    output = f'13'

                if note[index] == 'e' and len(note) == 3:
                    output = f'14'

                if note[index] == 'f' and len(note) == 3:
                    output = f'15'

                if note[index] == 'f' and len(note) == 4:
                    output = f'16'

                if note[index] == 'g' and len(note) == 3:
                    output = f'17'

                if note[index] == 'g' and len(note) == 4:
                    output = f'18'

                if note[index] == 'a' and len(note) == 3:
                    output = f'19'

                if note[index] == 'a' and len(note) == 4:
                    output = f'20'

                if note[index] == 'b' and len(note) == 3:
                    output = f'21'

                if note[index] == 'c' and len(note) == 3:
                    output = f'22'

                if note[index] == 'c' and len(note) == 4:
                    output = f'23'

            elif note[0] == 'v' and note[1] != 'i':
                index = 2

                if note[index] == 'A' and len(note) == 3:
                    output = f'0'

                if note[index] == 'A' and len(note) == 4:
                    output = f'1'

                if note[index] == 'B' and len(note) == 3:
                    output = f'2'

                if note[index] == 'C' and len(note) == 3:
                    output = f'3'

                if note[index] == 'C' and len(note) == 4:
                    output = f'4'

                if note[index] == 'D' and len(note) == 3:
                    output = f'5'

                if note[index] == 'D' and len(note) == 4:
                    output = f'6'

                if note[index] == 'E' and len(note) == 3:
                    output = f'7'

                if note[index] == 'F' and len(note) == 3:
                    output = f'8'

                if note[index] == 'F' and len(note) == 4:
                    output = f'9'

                if note[index] == 'G' and len(note) == 3:
                    output = f'10'

                if note[index] == 'G' and len(note) == 4:
                    output = f'11'

                if note[index] == 'a' and len(note) == 3:
                    output = f'12'

                if note[index] == 'a' and len(note) == 4:
                    output = f'13'

                if note[index] == 'b' and len(note) == 3:
                    output = f'14'

                if note[index] == 'c' and len(note) == 3:
                    output = f'15'

                if note[index] == 'c' and len(note) == 4:
                    output = f'16'

                if note[index] == 'd' and len(note) == 3:
                    output = f'17'
                
                if note[index] == 'd' and len(note) == 4:
                    output = f'18'

                if note[index] == 'e' and len(note) == 3:
                    output = f'19'

                if note[index] == 'f' and len(note) == 3:
                    output = f'20'

                if note[index] == 'f' and len(note) == 4:
                    output = f'21'

                if note[index] == 'g' and len(note) == 3:
                    output = f'22'

                if note[index] == 'g' and len(note) == 4:
                    output = f'23'

            elif note[0] == 'v' and note[1] == 'i':
                index = 3

                if note[index] == 'E' and len(note) == 3:
                    output = f'0'

                if note[index] == 'F' and len(note) == 3:
                    output = f'1'

                if note[index] == 'F' and len(note) == 4:
                    output = f'2'

                if note[index] == 'G' and len(note) == 3:
                    output = f'3'

                if note[index] == 'G' and len(note) == 4:
                    output = f'4'

                if note[index] == 'A' and len(note) == 3:
                    output = f'5'

                if note[index] == 'A' and len(note) == 4:
                    output = f'6'

                if note[index] == 'B' and len(note) == 3:
                    output = f'7'

                if note[index] == 'C' and len(note) == 3:
                    output = f'8'

                if note[index] == 'C' and len(note) == 4:
                    output = f'9'

                if note[index] == 'D' and len(note) == 3:
                    output = f'10'

                if note[index] == 'D' and len(note) == 4:
                    output = f'11'

                if note[index] == 'e' and len(note) == 3:
                    output = f'12'

                if note[index] == 'f' and len(note) == 3:
                    output = f'13'

                if note[index] == 'f' and len(note) == 4:
                    output = f'14'

                if note[index] == 'g' and len(note) == 3:
                    output = f'15'

                if note[index] == 'g' and len(note) == 4:
                    output = f'16'

                if note[index] == 'a' and len(note) == 3:
                    output = f'17'

                if note[index] == 'a' and len(note) == 4:
                    output = f'18'

                if note[index] == 'b' and len(note) == 3:
                    output = f'19'

                if note[index] == 'c' and len(note) == 3:
                    output = f'20'

                if note[index] == 'c' and len(note) == 4:
                    output = f'21'

                if note[index] == 'd' and len(note) == 3:
                    output = f'22'
                
                if note[index] == 'd' and len(note) == 4:
                    output = f'23'

        if self.number_state == False and self.text_state == True:
            
            if note[0] == 'i' and note[1] != 'i':
                index = 2
                output = f'{note[index:]}'
                
            elif note[0] == 'i' and note[1] == 'i' and note[2] != 'i':
                index = 3
                output = f'{note[index:]}'

            elif note[0] == 'i' and note[1] == 'i' and note[2] == 'i':
                index = 4
                output = f'{note[index:]}'

            elif note[0] == 'i' and note[1] == 'v':
                index = 3
                output = f'{note[index:]}'

            elif note[0] == 'v' and note[1] != 'i':
                index = 2
                output = f'{note[index:]}'

            elif note[0] == 'v' and note[1] == 'i':
                index = 3
                output = f'{note[index:]}'

        if self.number_state == False and self.text_state == False:
            output = note

        return output


#Qapplication instance
app = QApplication([])

#Widgets
window = MainWindow()
window.show()

#Event loop
app.exec()
