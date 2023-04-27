#-------------------------------------------------------------------------------
# Name:        BeepBoopKeyboardSynth
# Purpose:     Use Keyboard input to return tones
#
# Author:     Jayger
#
# Created:     26/04/2023
# Copyright:   (c) Yoozer 2023
# Licence:     <License to Thrill>
#-------------------------------------------------------------------------------

# So far this program hates bluetooh.f I think the headset sleeps between beeps or something

import numpy as np
# NumPy is a Python library for numerical computing that provides a powerful
# array object for efficiently storing and manipulating large arrays of
# homogeneous data. Via pip at cmd-> <python -m pip install pyaudio>

import pyaudio
# A Python library for working with audio. It provides Python bindings for
# the PortAudio library, which allows you to play and record audio
# on a variety of platforms. Via Pip at cmd-> <python -m pip install pyaudio>

import pynput
from pynput import keyboard
# This imports the pynput library and its keyboard module, which is used to listen for keyboard events.
# This module MIGHT be more friendly cross platform

import time
# import threading  # Might not be needed
# time and threading modules are part of python and should come
# natively. no extra installation package is neccessary

# Define note frequencies
# This is the dictionary of frequency values that will be assigned a letter value correlating to keyboard characters
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

# sampling frequency
fs = 44100

amplitude = 1                 # adjusts the amplitude of the sine wave
duration = 0.1                # How long the tone plays



# Initialize PyAudio
p = pyaudio.PyAudio()

# Define the sine_oscillator function
def sine_oscillator(freq, duration):

# This code defines a function sine_oscillator which takes two arguments freq and duration.
# It generates a sine wave with a frequency of freq and a duration of duration.
# It then opens an audio stream using pyaudio, plays the generated sound, and closes the stream.
# If an error occurs while opening the stream, it prints the error message.

    # Generate the sine wave
    step_size = 2*np.pi*freq/fs   # angular frequency or step size = (2*pi*f)/sample_rate

    samples = (amplitude*np.sin(step_size*np.arange(p.get_sample_size(format=pyaudio.paFloat32)*fs*duration))).astype(np.float32)
    # np.arange(p.get_sample_size(format=pyaudio.paFloat32) creates an array with length equal to number of samples in the audio signal

    # Open the audio stream
    try:
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)
        # Play the sound
        stream.write(0.1*samples)

        # Close the stream
        stream.stop_stream()
        stream.close()
    except OSError as e:
        print(f"Error: {e}")

# Define the keyboard listener function
# This code creates a keyboard.Listener object which listens for keyboard events and calls the on_press function when a key is pressed.
# It then starts listening for events by calling the .join() method on the listener object, which blocks the main thread until the listener is stopped.
# This allows the program to run continuously and respond to user input.

def on_press(key):
    try:
        if key.char in NOTE_FREQS:
            sine_oscillator(NOTE_FREQS[key.char], duration)   # sine_oscillator (from pyaudio)(NOTE_FREQS[key], duration)
        elif key.char == 'q':
            # Stop the keyboard listener and terminate the program
            print('\nExiting Program! Thanks for Beep Booping!')  # Farewell message
            listener.stop()
            p.terminate()
            exit()
    except AttributeError:
        pass

# begin keyboard listener function
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
    time.sleep(0.01)
#  W ith statement is used to ensure that the Listener object is cleanly closed when the program exits or raises an exception.
# The listener.join() method is used to start listening for events and block the main thread until the listener is stopped.
