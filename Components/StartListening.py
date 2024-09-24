from kivy.graphics import RoundedRectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
import threading
from kivy.uix.button import Button
import sounddevice as sd
import numpy as np
import soundfile as sf
import sys
import os
import tempfile
from kivy.clock import Clock
from threading import Lock, Thread
import traceback

class CustomTextBox(BoxLayout):
    def __init__(self, **kwargs):
        super(CustomTextBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (20, 20)
        self.size_hint = (None, None)
        self.size = (Window.size[1] / 2, 200)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.7}

        # Background with RoundedRectangle
        with self.canvas.before:
            Color(240 / 255, 241 / 255, 255 / 255, 1)
            self.background = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(pos=self.update_background, size=self.update_background)

        # Title Label
        title = Label(
            text="Start Listening",
            size_hint=(1, None),
            height=50,
            font_size='18sp',
            bold=True,
            pos_hint={'x': -0.26, 'center_y': 0},
            font_name='./Fonts/lexenddeca.ttf',
            color=(0, 0, 0, 1),
        )

        # Predefined Text Label
        text_box = Label(
            text="This is the predefined text inside the box.\n"
                 "It serves as the body content.",
            size_hint=(1, 1),
            font_size='14sp',
            color=(0, 0, 0, 1),
            halign='left',
            valign='top',
            font_name='./Fonts/poppins.ttf'
        )
        text_box.bind(size=text_box.setter('text_size'))

        # Button at Bottom Right
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        button_layout.add_widget(Label(size_hint_x=1))  # Spacer to push button to right
        self.action_button = Button(
            text="Start Listening",
            size=(150, 40),
            background_color=(240 / 255, 241 / 255, 255 / 255, 1),
            color=(86 / 255, 100 / 255, 245 / 255, 1),
            background_normal='',
            font_name='./Fonts/lexenddeca.ttf'
        )
        button_layout.add_widget(self.action_button)
        self.action_button.bind(on_press=self.start_listening)

        # Add components to the layout
        self.add_widget(title)
        self.add_widget(text_box)
        self.add_widget(button_layout)

        # Initialize recording attributes
        self.count = 0
        self.fs = 44100  # Sample rate
        self.chunk_size = 1024  # Size of each chunk (number of samples)
        self.recording = np.array([], dtype=np.int16)
        self.running = False

        # Initialize threading lock
        self.lock = Lock()

        # Queue for audio chunks
        self.chunk_queue = []

    def update_background(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

    def start_listening(self, instance):
        if self.count % 2 == 0:
            self.action_button.text = "Stop Listening"
            self.running = True
            self.stream = sd.InputStream(
                samplerate=self.fs,
                channels=1,  # Change channels to 1 for mono audio
                callback=self.audio_callback,
                blocksize=self.chunk_size
            )
            self.stream.start()
            self.process_thread = Thread(target=self.process_audio_queue)
            self.process_thread.start()
        else:
            self.action_button.text = "Start Listening"
            self.stop_listening()
        self.count += 1

    def stop_listening(self):
        if self.running:
            self.stream.stop()
            self.stream.close()
            self.running = False
            if self.process_thread.is_alive():
                self.process_thread.join()
            print("Stopped listening.")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)

        # Use lock to avoid concurrency issues
        with self.lock:
            if self.recording.size == 0:
                self.recording = np.zeros((0, indata.shape[1]))

            # Append the incoming audio data to the recording buffer
            self.recording = np.concatenate((self.recording, indata), axis=0)

            # Add the chunk to the queue for processing
            self.chunk_queue.append(indata.copy())

    def process_audio_queue(self):
        while self.running:
            if self.chunk_queue:
                chunk = self.chunk_queue.pop(0)
                self.process_audio_chunk(chunk)

    def process_audio_chunk(self, chunk):
        try:
            # Save the audio chunk to a temporary WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
                sf.write(temp_wav_file.name, chunk, self.fs)  # Write chunk to a WAV file
                temp_filename = temp_wav_file.name
            print(temp_filename)
            from ScreamDetector import callerFunction
            output = callerFunction(temp_filename)
            if(output == 1):
                print("Scream Detected")
            else:
                print("Scream Not Detected")




        except Exception as e:
            print(f"Error processing audio chunk: {e}")
            traceback.print_exc()

        finally:
            # Clean up the temp file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

    def update_ui(self, message):
        # This function can be used to update the UI safely on the main thread
        print(message)
        # Here you can add code to update any other UI components based on the message
