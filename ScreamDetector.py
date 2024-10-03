import numpy as np
import pyaudio
import struct
from scipy.fftpack import fft

# Audio parameters
CHUNK = 1024  # Number of data points to read at a time
RATE = 44100  # Sampling rate (samples per second)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream to microphone
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Listening...")

while True:
    # Read microphone audio data
    data = stream.read(CHUNK)

    # Convert the audio data to integers
    data_int = struct.unpack(str(CHUNK) + 'h', data)

    # Apply FFT to the audio data to find the frequency spectrum
    fft_data = fft(data_int)

    # Get the magnitude of the FFT
    magnitude = np.abs(fft_data)

    # Find the frequency with the maximum magnitude
    dominant_frequency = np.argmax(magnitude)

    # Convert the dominant frequency bin to an actual frequency in Hz
    frequency = dominant_frequency * RATE / CHUNK

    print(f"Dominant frequency: {frequency:.2f} Hz")

# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()
