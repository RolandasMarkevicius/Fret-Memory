import pyaudio
import numpy as np
import aubio
import random
import statistics
import numpy as np
import queue
from PySide6.QtCore import QThread, Signal, QEventLoop, Slot

# pitch table

vi_E_true = 82.41
vi_F_true = 87.31
vi_Fsh_true = 92.50
vi_G_true = 98.00
vi_Gsh_true = 103.83
vi_A_true = 110.00
vi_Ash_true = 116.5500
vi_B_true = 123.48
vi_C_true = 130.82
vi_Csh_true = 138.60
vi_D_true = 146.84
vi_Dsh_true = 155.57
vi_e_true = 164.82
vi_f_true = 174.62
vi_fsh_true = 185.00
vi_g_true = 196.00
vi_gsh_true = 207.66
vi_a_true = 220.01
vi_ash_true = 233.09
vi_b_true = 246.95
vi_c_true = 261.63
vi_csh_true = 277.19
vi_d_true = 293.68
#vi_dsh_true = 311.14

v_A_true = 110.00
v_Ash_true = 116.5500
v_B_true = 123.48
v_C_true = 130.82
v_Csh_true = 138.60
v_D_true = 146.84
v_Dsh_true = 155.57
v_E_true = 164.82
v_F_true = 174.62
v_Fsh_true = 185.00
v_G_true = 196.00
v_Gsh_true = 207.66
v_a_true = 220.01
v_ash_true = 233.09
v_b_true = 246.95
v_c_true = 261.63
v_csh_true = 277.19
v_d_true = 293.68
v_dsh_true = 311.14
v_e_true = 329.64
v_f_true = 349.24
v_fsh_true = 370.01
v_g_true = 392.01
#v_gsh_true = 415.32

iv_D_true = 146.84
iv_Dsh_true = 155.57
iv_E_true = 164.82
iv_F_true = 174.62
iv_Fsh_true = 185.00
iv_G_true = 196.00
iv_Gsh_true = 207.66
iv_A_true = 220.01
iv_Ash_true = 233.09
iv_B_true = 246.95
iv_C_true = 261.63
iv_Csh_true = 277.19
iv_d_true = 293.68
iv_dsh_true = 311.14
iv_e_true = 329.64
iv_f_true = 349.24
iv_fsh_true = 370.01
iv_g_true = 392.01
iv_gsh_true = 415.32
iv_a_true = 440.02
iv_ash_true = 466.18
iv_b_true = 493.90
iv_c_true = 523.27
#iv_csh_true = 554.38


iii_G_true = 196.00
iii_Gsh_true = 207.66
iii_A_true = 220.01
iii_Ash_true = 233.09
iii_B_true = 246.95
iii_C_true = 261.63
iii_Csh_true = 277.19
iii_D_true = 293.68
iii_Dsh_true = 311.14
iii_E_true = 329.64
iii_F_true = 349.24
iii_Fsh_true = 370.01
iii_g_true = 392.01
iii_gsh_true = 415.32
iii_a_true = 440.02
iii_ash_true = 466.18
iii_b_true = 493.90
iii_c_true = 523.27
iii_csh_true = 554.38
iii_d_true = 587.35
iii_dsh_true = 622.28
iii_e_true = 659.28
iii_f_true = 698.48
#iii_fsh_true = 740.01


ii_B_true = 246.95
ii_C_true = 261.63
ii_Csh_true = 277.19
ii_D_true = 293.68
ii_Dsh_true = 311.14
ii_E_true = 329.64
ii_F_true = 349.24
ii_Fsh_true = 370.01
ii_G_true = 392.01
ii_Gsh_true = 415.32
ii_A_true = 440.02
ii_Ash_true = 466.18
ii_b_true = 493.90
ii_c_true = 523.27
ii_csh_true = 554.38
ii_d_true = 587.35
ii_dsh_true = 622.28
ii_e_true = 659.28
ii_f_true = 698.48
ii_fsh_true = 740.01
ii_g_true = 784.02
ii_gsh_true = 830.64
ii_a_true = 880.03
#ii_ash_true = 932.36

i_E_true = 329.64
i_F_true = 349.24
i_Fsh_true = 370.01
i_G_true = 392.01
i_Gsh_true = 415.32
i_A_true = 440.02
i_Ash_true = 466.18
i_B_true = 493.90
i_C_true = 523.27
i_Csh_true = 554.38
i_D_true = 587.35
i_Dsh_true = 622.28
i_e_true = 659.28
i_f_true = 698.48
i_fsh_true = 740.01
i_g_true = 784.02
i_gsh_true = 830.64
i_a_true = 880.03
i_ash_true = 932.36
i_b_true = 987.80
i_c_true = 1046.54
i_csh_true = 1108.77
i_d_true = 1174.70
#i_dsh_true = 1244.55

i_string = [i_E_true,
            i_F_true,
            i_Fsh_true,
            i_G_true,
            i_Gsh_true,
            i_A_true,
            i_Ash_true,
            i_B_true,
            i_C_true,
            i_Csh_true,
            i_D_true,
            i_Dsh_true,
            i_e_true,
            i_f_true,
            i_fsh_true,
            i_g_true,
            i_gsh_true,
            i_a_true,
            i_ash_true,
            i_b_true,
            i_c_true,
            i_csh_true,
            i_d_true]

i_string_str = ['i_E',
            'i_F',
            'i_F#',
            'i_G',
            'i_G#',
            'i_A',
            'i_A#',
            'i_B',
            'i_C',
            'i_C#',
            'i_D',
            'i_D#',
            'i_e',
            'i_f',
            'i_f#',
            'i_g',
            'i_g#',
            'i_a',
            'i_a#',
            'i_b',
            'i_c',
            'i_c#',
            'i_d']

ii_string = [ii_B_true,
            ii_C_true,
            ii_Csh_true,
            ii_D_true,
            ii_Dsh_true,
            ii_E_true,
            ii_F_true,
            ii_Fsh_true,
            ii_G_true,
            ii_Gsh_true,
            ii_A_true,
            ii_Ash_true,
            ii_b_true,
            ii_c_true,
            ii_csh_true,
            ii_d_true,
            ii_dsh_true,
            ii_e_true,
            ii_f_true,
            ii_fsh_true,
            ii_g_true,
            ii_gsh_true,
            ii_a_true]

ii_string_str = ['ii_B',
            'ii_C',
            'ii_C#',
            'ii_D',
            'ii_D#',
            'ii_E',
            'ii_F',
            'ii_F#',
            'ii_G',
            'ii_G#',
            'ii_A',
            'ii_A#',
            'ii_b',
            'ii_c',
            'ii_c#',
            'ii_d',
            'ii_d#',
            'ii_e',
            'ii_f',
            'ii_f#',
            'ii_g',
            'ii_g#',
            'ii_a']

iii_string = [iii_G_true,
            iii_Gsh_true,
            iii_A_true,
            iii_Ash_true,
            iii_B_true,
            iii_C_true,
            iii_Csh_true,
            iii_D_true,
            iii_Dsh_true,
            iii_E_true,
            iii_F_true,
            iii_Fsh_true,
            iii_g_true,
            iii_gsh_true,
            iii_a_true,
            iii_ash_true,
            iii_b_true,
            iii_c_true,
            iii_csh_true,
            iii_d_true,
            iii_dsh_true,
            iii_e_true,
            iii_f_true]

iii_string_str = ['iii_G',
            'iii_G#',
            'iii_A',
            'iii_A#',
            'iii_B',
            'iii_C',
            'iii_C#',
            'iii_D',
            'iii_D#',
            'iii_E',
            'iii_F',
            'iii_F#',
            'iii_g',
            'iii_g#',
            'iii_a',
            'iii_a#',
            'iii_b',
            'iii_c',
            'iii_c#',
            'iii_d',
            'iii_d#',
            'iii_e',
            'iii_f']

iv_string = [iv_D_true,
            iv_Dsh_true,
            iv_E_true,
            iv_F_true,
            iv_Fsh_true,
            iv_G_true,
            iv_Gsh_true,
            iv_A_true,
            iv_Ash_true,
            iv_B_true,
            iv_C_true,
            iv_Csh_true,
            iv_d_true,
            iv_dsh_true,
            iv_e_true,
            iv_f_true,
            iv_fsh_true,
            iv_g_true,
            iv_gsh_true,
            iv_a_true,
            iv_ash_true,
            iv_b_true,
            iv_c_true]

iv_string_str = ['iv_D',
            'iv_D#',
            'iv_E',
            'iv_F',
            'iv_F#',
            'iv_G',
            'iv_G#',
            'iv_A',
            'iv_A#',
            'iv_B',
            'iv_C',
            'iv_C#',
            'iv_d',
            'iv_d#',
            'iv_e',
            'iv_f',
            'iv_f#',
            'iv_g',
            'iv_g#',
            'iv_a',
            'iv_a#',
            'iv_b',
            'iv_c']

v_string = [v_A_true,
            v_Ash_true,
            v_B_true,
            v_C_true,
            v_Csh_true,
            v_D_true,
            v_Dsh_true,
            v_E_true,
            v_F_true,
            v_Fsh_true,
            v_G_true,
            v_Gsh_true,
            v_a_true,
            v_ash_true,
            v_b_true,
            v_c_true,
            v_csh_true,
            v_d_true,
            v_dsh_true,
            v_e_true,
            v_f_true,
            v_fsh_true,
            v_g_true]

v_string_str = ['v_A',
            'v_A#',
            'v_B',
            'v_C',
            'v_C#',
            'v_D',
            'v_D#',
            'v_E',
            'v_F',
            'v_F#',
            'v_G',
            'v_G#',
            'v_a',
            'v_a#',
            'v_b',
            'v_c',
            'v_c#',
            'v_d',
            'v_d#',
            'v_e',
            'v_f',
            'v_f#',
            'v_g']

vi_string = [vi_E_true,
            vi_F_true,
            vi_Fsh_true,
            vi_G_true,
            vi_Gsh_true,
            vi_A_true,
            vi_Ash_true,
            vi_B_true,
            vi_C_true,
            vi_Csh_true,
            vi_D_true,
            vi_Dsh_true,
            vi_e_true,
            vi_f_true,
            vi_fsh_true,
            vi_g_true,
            vi_gsh_true,
            vi_a_true,
            vi_ash_true,
            vi_b_true,
            vi_c_true,
            vi_csh_true,
            vi_d_true]

vi_string_str = ['vi_E',
            'vi_F',
            'vi_F#',
            'vi_G',
            'vi_G#',
            'vi_A',
            'vi_A#',
            'vi_B',
            'vi_C',
            'vi_C#',
            'vi_D',
            'vi_D#',
            'vi_e',
            'vi_f',
            'vi_f#',
            'vi_g',
            'vi_g#',
            'vi_a',
            'vi_a#',
            'vi_b',
            'vi_c',
            'vi_c#',
            'vi_d']


class StandardBounds():
    def __init__(self):
        
        vi_bounds = self.bounds(vi_string)
        v_bounds = self.bounds(v_string)
        iv_bounds = self.bounds(iv_string)
        iii_bounds = self.bounds(iii_string)
        ii_bounds = self.bounds(ii_string)
        i_bounds = self.bounds(i_string)

        self.bounds_list = [i_bounds, ii_bounds, iii_bounds, iv_bounds, v_bounds, vi_bounds]


    def bounds(self, x_string_conv):
        # get middle valu between each key on a string
        x_range_shifted = np.roll(x_string_conv, 1)
        x_range_mid = (x_string_conv[1:] + x_range_shifted[1:]) / 2

        # get the lowest bound
        x_bound_0 = 2 * x_string_conv[0] - x_range_mid[0]

        # get the highest bound
        x_bound_1 = 2 * x_string_conv[-1] - x_range_mid[-1]

        # complete bounds
        x_bound_floor = np.insert(x_range_mid, 0, x_bound_0)
        x_bound_ceiling = np.insert(x_range_mid, len(x_range_mid), x_bound_1)

        # generate bounds list
        bound_list = [[a, b] for a, b in zip(x_bound_floor, x_bound_ceiling)]
        bound_list = np.array(bound_list)

        return bound_list

class StringPicker():
    def __init__(self):

        self.key_list  = []
        self.key_str_list = []
        self.mode_list = []

    def click_evi(self, checked):
        if checked == True:
            self.key_list.append(i_string)
            self.key_str_list.append(i_string_str)
            self.mode_list.append('evi')
            print(self.key_list)

        elif checked == False:
            try:
                self.key_list.remove(i_string)
                self.key_str_list.remove(i_string_str)
                self.mode_list.remove('evi')
            except:
                pass

    def click_b(self, checked):
        if checked == True:
            self.key_list.append(ii_string)
            self.key_str_list.append(ii_string_str)
            self.mode_list.append('b')

        elif checked == False:
            try:
                self.key_list.remove(ii_string)
                self.key_str_list.remove(ii_string_str)
                self.mode_list.remove('b')
            except:
                pass

    def click_g(self, checked):
        if checked == True:
            self.key_list.append(iii_string)
            self.key_str_list.append(iii_string_str)
            self.mode_list.append('g')

        elif checked == False:
            try:
                self.key_list.remove(iii_string)
                self.key_str_list.remove(iii_string_str)
                self.mode_list.remove('g')
            except:
                pass

    def click_d(self, checked):
        if checked == True:
            self.key_list.append(iv_string)
            self.key_str_list.append(iv_string_str)
            self.mode_list.append('d')

        elif checked == False:
            try:
                self.key_list.remove(iv_string)
                self.key_str_list.remove(iv_string_str)
                self.mode_list.remove('d')
            except:
                pass

    def click_a(self, checked):
        if checked == True:
            self.key_list.append(v_string)
            self.key_str_list.append(v_string_str)
            self.mode_list.append('a')

        elif checked == False:
            try:
                self.key_list.remove(v_string)
                self.key_str_list.remove(v_string_str)
                self.mode_list.remove('a')
            except:
                pass

    def click_ei(self, checked):
        if checked == True:
            self.key_list.append(vi_string)
            self.key_str_list.append(vi_string_str)
            self.mode_list.append('ei')

        elif checked == False:
            try:
                self.key_list.remove(vi_string)
                self.key_str_list.remove(vi_string_str)
                self.mode_list.remove('ei')
            except:
                pass

class AutoScroll(QThread):
    update = Signal(object)
    idx_signal = Signal(int)

    def __init__(self, step_idx):
        super().__init__()

        self.step_idx = step_idx
        self.note_idx = 0
        self.idx_signal.connect(self.run)

    # @Slot(int)
    def run(self, note_idx):
        self.note_idx = note_idx

        if int(float(self.note_idx) % float(self.step_idx)) == 0 and self.note_idx != 0:
            self.update.emit(True)

            print(f'% is {int(float(self.note_idx) % float(self.step_idx))}')
            print(f'Current index is: {self.note_idx}')
            print(f'Step index is: {self.step_idx}')
            print('Autoscroll move emited')

class CalibrateGuitar(QThread):
    finished = Signal(object)

    def __init__(self, string):
        super().__init__()
        BUFFER_SIZE = 2048
        self.buffer_size = BUFFER_SIZE
        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = 44100

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=BUFFER_SIZE,
                        input_device_index=2)
        
        # Initialize aubio pitch detection
        self.pDetection = aubio.pitch("default", BUFFER_SIZE, BUFFER_SIZE, RATE)
        self.pDetection.set_unit("Hz")
        self.pDetection.set_silence(-70)
        self.pDetection.set_tolerance(0.8)

        self.time_to_average = 0.2
        self.time_buffer = int(RATE / BUFFER_SIZE * self.time_to_average)
        self.pitch_buffer = []
        self.good_sample_count = 12
        self.fq_threshold = 60

        if string == 'evi':
            self.string_value = i_string
        if string == 'b':
            self.string_value = ii_string
        if string == 'g':
            self.string_value = iii_string
        if string == 'd':
            self.string_value = iv_string
        if string == 'a':
            self.string_value = v_string
        if string == 'ei':
            self.string_value = vi_string

        self._running = True

    def run(self):
        self.get_new_bounds()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.finished.emit(self.result)

    def get_new_bounds(self):
        self.string_tuner()
        self.converted = self.fq_converter(recorded = self.good_sample_mode, string=self.string_value)
        self.result = self.bounds(self.converted)

    def record_pitch(self):
        pitch_list = []

        while len(pitch_list) <= self.time_buffer:
            # Get audio input
            audio_data = np.frombuffer(self.stream.read(self.buffer_size), dtype=np.float32)

            # Detect pitch (note) from audio input
            pitch = self.pDetection(audio_data)[0]

            #Make a list
            if pitch is not None and pitch >= self.fq_threshold:
                pitch_list.append(int(pitch))

        pitch_buffer_mode = statistics.mode(pitch_list)

        return pitch_buffer_mode
    
    def string_tuner(self):
        # record with a while loop untill x number of samples is collected
        good_samples = []

        while len(good_samples) < self.good_sample_count:
            
            # record
            sample = self.record_pitch()
            good_samples.append(sample)

        # get the mean of the sample
        self.good_sample_mode = statistics.mode(good_samples)

    def fq_converter(self, recorded, string):
        diff = recorded - string[0]
        string_array = np.array(string)
        conv_string = string_array - diff
        return conv_string

    def bounds(self, x_string_conv):
        # get middle valu between each key on a string
        x_range_shifted = np.roll(x_string_conv, 1)
        x_range_mid = (x_string_conv[1:] + x_range_shifted[1:]) / 2

        # get the lowest bound
        x_bound_0 = 2 * x_string_conv[0] - x_range_mid[0]

        # get the highest bound
        x_bound_1 = 2 * x_string_conv[-1] - x_range_mid[-1]

        # complete bounds
        x_bound_floor = np.insert(x_range_mid, 0, x_bound_0)
        x_bound_ceiling = np.insert(x_range_mid, len(x_range_mid), x_bound_1)

        # generate bounds list
        bound_list = [[a, b] for a, b in zip(x_bound_floor, x_bound_ceiling)]
        bound_list = np.array(bound_list)

        return bound_list

class SoundProcessing(QThread):
    update = Signal(object)

    def __init__(self, mode_list, bound_list, note_list):
        super().__init__()
        BUFFER_SIZE = 2048
        self.buffer_size = BUFFER_SIZE
        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = 44100

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=BUFFER_SIZE,
                        input_device_index=2)
        
        # Initialize aubio pitch detection
        self.pDetection = aubio.pitch("default", BUFFER_SIZE, BUFFER_SIZE, RATE)
        self.pDetection.set_unit("Hz")
        self.pDetection.set_silence(-70)
        self.pDetection.set_tolerance(0.8)

        self.time_to_average = 0.2
        self.time_buffer = int(RATE / BUFFER_SIZE * self.time_to_average)
        self.pitch_buffer = []
        self.good_sample_count = 12
        self.fq_threshold = 60

        self.mode_list = mode_list
        self.bound_list = bound_list
        self.note_list = note_list

        self._running = True

    def run(self):
        for note in self.note_list:
            self._running = True

            while self._running:
                recorded = self.record_pitch()

                # test if the current pitch matches a key in each string
                if 'evi' in self.mode_list:
                    i_recorded_key = self.fq_to_key(pitch=recorded, 
                                                    string=i_string_str, 
                                                    bounds=self.bound_list[0])

                if 'b' in self.mode_list:
                    ii_recorded_key = self.fq_to_key(pitch=recorded, 
                                                    string=ii_string_str, 
                                                    bounds=self.bound_list[1])

                if 'g' in self.mode_list:
                    iii_recorded_key = self.fq_to_key(pitch=recorded, 
                                                    string=iii_string_str, 
                                                    bounds=self.bound_list[2])


                if 'd' in self.mode_list:
                    iv_recorded_key = self.fq_to_key(pitch=recorded,
                                                    string=iv_string_str, 
                                                    bounds=self.bound_list[3])


                if 'a' in self.mode_list:
                    v_recorded_key = self.fq_to_key(pitch=recorded, 
                                                    string=v_string_str, 
                                                    bounds=self.bound_list[4])


                if 'ei' in self.mode_list:
                    vi_recorded_key = self.fq_to_key(pitch=recorded, 
                                                    string=vi_string_str, 
                                                    bounds=self.bound_list[5])


                if note[0] == 'i' and note[1] != 'i':
                    if i_recorded_key == note:
                        self.update.emit(True)
                        self._running = False
                    else: self.update.emit(False)

                elif note[0] == 'i' and note[1] == 'i' and note[2] != 'i':
                    if ii_recorded_key == note:
                        self.update.emit(True)
                        self._running = False
                    else: self.update.emit(False)

                elif note[0] == 'i' and note[1] == 'i' and note[2] == 'i':
                    if iii_recorded_key == note:
                        self.update.emit(True)
                        self._running = False
                    else: self.update.emit(False)

                elif note[0] == 'i' and note[1] == 'v':
                    if iv_recorded_key == note:
                        self.update.emit(True)
                        self._running = False
                    else: self.update.emit(False)

                elif note[0] == 'v' and note[1] != 'i':
                    if v_recorded_key == note:
                        self.update.emit(True)
                        self._running = False
                    else: self.update.emit(False)

                elif note[0] == 'v' and note[1] == 'i':
                    if vi_recorded_key == note:
                        self.update.emit(True)
                        self._running = False
                    else: self.update.emit(False)

                else:
                    continue

        self._running = False

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def stop(self):
        self._running = False
        self.wait()

    def fq_to_key(self, pitch, string, bounds):
        floor = bounds[:, 0]
        ceiling = bounds[:, 1]

        print(pitch)

        true_array = np.logical_and(floor <= pitch, pitch <= ceiling)
        index = np.where(true_array == True)[0]

        if len(index) > 0:
            key = string[index[0]]
        else:
            key = ['not_key']

        return key
    
    def record_pitch(self):
        pitch_list = []

        while len(pitch_list) <= self.time_buffer:
            # Get audio input
            audio_data = np.frombuffer(self.stream.read(self.buffer_size), dtype=np.float32)

            # Detect pitch (note) from audio input
            pitch = self.pDetection(audio_data)[0]

            #Make a list
            if pitch is not None and pitch >= self.fq_threshold:
                pitch_list.append(int(pitch))

        pitch_buffer_mode = statistics.mode(pitch_list)

        return pitch_buffer_mode