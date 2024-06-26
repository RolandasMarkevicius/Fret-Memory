import pyaudio
import numpy as np
import aubio
import random
import statistics
import numpy as np

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


# Initialize audio input
BUFFER_SIZE = 2048
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=BUFFER_SIZE)

# Initialize aubio pitch detection
pDetection = aubio.pitch("default", BUFFER_SIZE, BUFFER_SIZE, RATE)
pDetection.set_unit("Hz")
pDetection.set_silence(-70)
pDetection.set_tolerance(0.8)

time_to_average = 0.2
time_buffer = int(RATE / BUFFER_SIZE * time_to_average)
pitch_buffer = []
good_sample_count = 12
fq_threshold = 60

def record_pitch(time_buffer, threshold):

    pitch_list = []

    while len(pitch_list) <= time_buffer:
        # Get audio input
        audio_data = np.frombuffer(stream.read(BUFFER_SIZE), dtype=np.float32)

        # Detect pitch (note) from audio input
        pitch = pDetection(audio_data)[0]

        #Make a list
        if pitch is not None and pitch >= threshold:
            pitch_list.append(int(pitch))

    pitch_buffer_mode = statistics.mode(pitch_list)

    return pitch_buffer_mode

def string_tuner(good_sample_count, threshold):
    # record with a while loop untill x number of samples is collected
    good_samples = []

    while len(good_samples) < good_sample_count:
        
        # record
        sample = record_pitch(time_buffer=time_buffer, threshold=threshold)
        good_samples.append(sample)

    # get the mean of the sample
    good_sample_mode = statistics.mode(good_samples)

    return good_sample_mode

def fq_converter(recorded, string):
    diff = recorded - string[0]
    string_array = np.array(string)
    conv_string = string_array - diff
    return conv_string

def bounds(x_string_conv):
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

def fq_to_key(pitch, string, bounds):
    floor = bounds[:, 0]
    ceiling = bounds[:, 1]

    true_array = np.logical_and(floor <= pitch, pitch <= ceiling)
    index = np.where(true_array == True)[0]

    if len(index) > 0:
        key = string[index[0]]
    else:
        key = ['not_key']

    return key

vi_bounds = bounds(vi_string)
v_bounds = bounds(v_string)
iv_bounds = bounds(iv_string)
iii_bounds = bounds(iii_string)
ii_bounds = bounds(ii_string)
i_bounds = bounds(i_string)

print(i_bounds)
print(ii_bounds)
print(iii_bounds)
print(iv_bounds)
print(v_bounds)
print(vi_bounds)

mode = input('Hi:) What do you want to practice today? \n(Enter the strings you want to practice): ')
mode_list = mode.split(sep=', ')

key_list  = []
key_str_list = []

for string in mode_list:
    if string == 'i':
        key_list.append(i_string)
        key_str_list.append(i_string_str)
    if string == 'ii':
        key_list.append(ii_string)
        key_str_list.append(ii_string_str)
    if string == 'iii':
        key_list.append(iii_string)
        key_str_list.append(iii_string_str)
    if string == 'iv':
        key_list.append(iv_string)
        key_str_list.append(iv_string_str)
    if string == 'v':
        key_list.append(v_string)
        key_str_list.append(v_string_str)
    if string == 'vi':
        key_list.append(vi_string)
        key_str_list.append(vi_string_str)

# Generate a random key
key_array = np.array(key_list)
key_list = key_array.flatten()

key_str_array = np.array(key_str_list)
key_str_list = key_str_array.flatten()

random_list = list(range(len(key_str_list)))

calibrate = input('Lets calibrate the guitar, Yes/No: ')

if calibrate == 'Yes' or calibrate == 'yes':

    print('Please play open E (vi string)')
    vi_recorded = string_tuner(good_sample_count=good_sample_count, threshold=fq_threshold)
    print(f'Recorded: {vi_recorded}, True: {vi_string[0]}')
    vi_converted = fq_converter(recorded=vi_recorded, string=vi_string)
    vi_bounds = bounds(vi_converted)

    input('Done! Please play open A (v string): ')
    v_recorded = string_tuner(good_sample_count=good_sample_count, threshold=fq_threshold)
    print(f'Recorded: {v_recorded}, True: {v_string[0]}')
    v_converted = fq_converter(recorded=v_recorded, string=v_string)
    v_bounds = bounds(v_converted)

    input('Done! Please play open D (iv string): ')
    iv_recorded = string_tuner(good_sample_count=good_sample_count, threshold=fq_threshold)
    print(f'Recorded: {iv_recorded}, True: {iv_string[0]}')
    iv_converted = fq_converter(recorded=iv_recorded, string=iv_string)
    iv_bounds = bounds(iv_converted)

    input('Done! Please play open G (iii string): ')
    iii_recorded = string_tuner(good_sample_count=good_sample_count, threshold=fq_threshold)
    print(f'Recorded: {iii_recorded}, True: {iii_string[0]}')
    iii_converted = fq_converter(recorded=iii_recorded, string=iii_string)
    iii_bounds = bounds(iii_converted)

    input('Done! Please play open B (ii string): ')
    ii_recorded = string_tuner(good_sample_count=good_sample_count, threshold=fq_threshold)
    print(f'Recorded: {ii_recorded}, True: {ii_string[0]}')
    ii_converted = fq_converter(recorded=ii_recorded, string=ii_string)
    ii_bounds = bounds(ii_converted)

    input('Done! Please play open e (i string): ')
    i_recorded = string_tuner(good_sample_count=good_sample_count, threshold=fq_threshold)
    print(f'Recorded: {i_recorded}, True: {i_string[0]}')
    i_converted = fq_converter(recorded=i_recorded, string=i_string)
    i_bounds = bounds(i_converted)

else:
     vi_bounds = bounds(vi_string)
     v_bounds = bounds(v_string)
     iv_bounds = bounds(iv_string)
     iii_bounds = bounds(iii_string)
     ii_bounds = bounds(ii_string)
     i_bounds = bounds(i_string)

while True:
    try:
        # generate a random key
        random.shuffle(random_list)
        random_int = random_list[0]
        random_key = key_str_list[random_int]

        # print a random key
        print(f'Play: {random_key}')

        recorded_key = 1

        while recorded_key != random_key:
            # get the current pitch
            recorded = record_pitch(time_buffer=time_buffer, threshold=fq_threshold)

            # test if the current pitch matches a key in each string
            if 'i' in mode_list:
                i_recorded_key = fq_to_key(pitch=recorded, string=i_string_str, bounds=i_bounds)
            if 'ii' in mode_list:
                ii_recorded_key = fq_to_key(pitch=recorded, string=ii_string_str, bounds=ii_bounds)
            if 'iii' in mode_list:
                iii_recorded_key = fq_to_key(pitch=recorded, string=iii_string_str, bounds=iii_bounds)
            if 'iv' in mode_list:
                iv_recorded_key = fq_to_key(pitch=recorded, string=iv_string_str, bounds=iv_bounds)
            if 'v' in mode_list:
                v_recorded_key = fq_to_key(pitch=recorded, string=v_string_str, bounds=v_bounds)
            if 'vi' in mode_list:
                vi_recorded_key = fq_to_key(pitch=recorded, string=vi_string_str, bounds=vi_bounds)

            keys = []

            for string in mode_list:
                if string == 'i':
                    keys.append(i_recorded_key)
                if string == 'ii':
                    keys.append(ii_recorded_key)
                if string == 'iii':
                    keys.append(iii_recorded_key)
                if string == 'iv':
                    keys.append(iv_recorded_key)
                if string == 'v':
                    keys.append(v_recorded_key)
                if string == 'vi':
                    keys.append(vi_recorded_key)

            for key in keys:
                if key == random_key:
                    recorded_key = key

        recorded_key = []

    except KeyboardInterrupt:
        break

stream.stop_stream()
stream.close()
p.terminate()