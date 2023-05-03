import numpy as np
import pyaudio
import pynput
from pynput import keyboard
import time

sampling_freq = 44100
amplitude = 1

beat_duration = .5
BPM = 140      # Beats per minute
BPS = BPM/60   # beats per second

print('BPM is:', BPM)

whole_note = BPS
half_note = BPS/2
quarter_note = BPS/4
eigth_note = BPS/8
sixteenth_note = BPS/16

hold = 0  # GLOBAL
print(hold)

duration = 0.1  # in seconds
# Define note frequencies
NOTE_FREQS = {
    # A row
    "a": 220.00,   # A3
    "s": 246.94,   # B3
    "d": 277.18,   # C#4/Db4
    "f": 293.66,   # D4
    "g": 329.63,   # E4
    "h": 369.99,   # F#4/Gb4
    "j": 392.00,   # G4
    "k": 440.00,   # A4
    "l": 493.88,   # B4
    ";": 554.37,   # C#5/Db5
    "'": 587.33    # D5
}

DUR = {
    "1": whole_note,    # whole note
    "2": half_note,   # half note
    "4": quarter_note,  # quarter note
    "8": eigth_note,  # either note
    "9": sixteenth_note  # 16th note
}


# Generate the sine wave
def oscillator_sine(fs, amp, freq, dur):
    # Set parameters for the sine wave

    time_array = np.arange(0, dur, 1 / fs)
    sine_wave = np.sin(2 * np.pi * freq * time_array)

    # Apply fade-out effect
    fade_out_duration = 0.05  # in seconds
    fade_out_samples = int(fade_out_duration * fs)
    fade_out_array = np.linspace(1, 0, fade_out_samples)
    sine_wave[-fade_out_samples:] *= fade_out_array

    return sine_wave


# Define the callback function for when a key is pressed
def on_press(key):
    global hold, duration
    try:
        # Print the key that was pressed
        print('\nKey {0} pressed.'.format(key.char))
        if key.char == 'q':
            print('\nQ press detected to exit! Thanks for BeepBooping!')
            listener.stop()
        elif key.char in DUR.keys():
            duration = DUR[key.char]
        else:
            freq = NOTE_FREQS[key.char]
            hold = 1
            sine_wave = oscillator_sine(sampling_freq, amplitude, freq, duration)
            stream.write(sine_wave.astype(np.float32).tobytes())
            hold = 0
    except KeyError:
        # If a special key (e.g., shift, ctrl) was pressed, print its name
        print('Key {0} pressed.'.format(key))


# Play the sine wave
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sampling_freq, output=True)

# Create a listener for keyboard events
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

# Close the audio stream
stream.stop_stream()
stream.close()
p.terminate()
