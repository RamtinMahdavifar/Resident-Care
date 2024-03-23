import numpy as np
import pygame
import os, sys

from contextlib import contextmanager

# Initialize the mixer module for audio playback
pygame.mixer.init()


def beep(frequency: int, duration: int) -> None:
    """
    Play a beep sound at a specified frequency and duration.

    Parameters:
    frequency (int): The frequency of the beep in Hertz.
    duration (int): The duration of the beep in milliseconds.
    """
    # Constants
    sample_rate = 44100  # Sample rate in Hertz

    # Conversion factor from milliseconds to seconds
    milliseconds_to_seconds = 1000.0

    channels = 2  # Number of audio channels
    bits_per_sample = 16  # Number of bits per audio sample
    # Maximum value for a sample
    max_sample_value = 2 ** (bits_per_sample - 1) - 1

    # Generate a sound buffer with the given frequency
    n_samples = int(round(duration * sample_rate / milliseconds_to_seconds))
    buf = np.zeros((n_samples, channels), dtype=np.int16)

    for s in range(n_samples):
        t = float(s) / sample_rate  # time in seconds

        # Generate the sound for both left and right channels
        sample_value = int(
            round(max_sample_value * np.sin(2 * np.pi * frequency * t)))
        buf[s][0] = sample_value  # left channel
        buf[s][1] = sample_value  # right channel

    sound = pygame.sndarray.make_sound(buf)

    # Play the sound
    sound.play(-1)
    pygame.time.delay(duration)
    sound.stop()


def remove_temp_files(file_path: str) -> None:
    """
    Remove temporary files created during the process.

    Parameters:
    file_path (str): The path to the file to remove.
    """
    os.remove(file_path)


@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
