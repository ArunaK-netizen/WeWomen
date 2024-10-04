from kivy.graphics import RoundedRectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
import threading
import numpy as np
import os
from scipy.fftpack import fft
from kivy.uix.button import Button
import sounddevice as sd
import sys
from kivy.uix.popup import Popup
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

        # List to store last five detected frequencies
        self.detected_frequencies = []
        self.scream_detected = False  # Flag to indicate if a scream has been detected

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

    def stop_listening(self, dt=None):
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

        with self.lock:
            if self.recording.size == 0:
                self.recording = np.zeros((0, indata.shape[1]))

            self.recording = np.concatenate((self.recording, indata), axis=0)

            self.chunk_queue.append(indata.copy())

    def process_audio_queue(self):
        while self.running:
            if self.chunk_queue:
                chunk = self.chunk_queue.pop(0)
                self.process_audio_chunk(chunk)

    def process_audio_chunk(self, chunk):
        try:
            data_int = np.frombuffer(chunk, dtype=np.int16)
            fft_data = fft(data_int)
            magnitude = np.abs(fft_data)

            dominant_frequency = np.argmax(magnitude[:len(magnitude) // 2])
            frequency = dominant_frequency * self.fs / len(data_int)

            print(f"Detected Frequency: {frequency} Hz")

            # Store the detected frequency
            self.detected_frequencies.append(frequency)
            if len(self.detected_frequencies) > 5:
                self.detected_frequencies.pop(0)  # Keep only the last 5 frequencies

            # Check if the last five frequencies fall in the scream range (500 Hz to 4000 Hz)
            if len(self.detected_frequencies) == 5 and all(1300 <= f <= 4000 for f in self.detected_frequencies):
                self.scream_detected = True  # Set the flag when a scream is detected
                Clock.schedule_once(self.stop_listening)  # Schedule stop_listening to run in the main thread
                self.show_scream_popup()

        except Exception as e:
            print(f"Error processing audio chunk: {e}")
            traceback.print_exc()

    def show_scream_popup(self):
        Clock.schedule_once(self.create_scream_popup)

    def create_scream_popup(self, dt):
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Label(text="Scream Detected!", font_size=20))

        self.close_button = Button(text="Close", size_hint=(1, None), height=40)
        popup_content.add_widget(self.close_button)

        self.popup = Popup(title="Alert", content=popup_content, size_hint=(None, None), size=(400, 200))

        self.close_button.bind(on_press=self.close_popup)
        Clock.schedule_once(self.auto_close_popup, 5)

        self.popup.open()

    def close_popup(self, instance):
        if self.popup:
            self.popup.dismiss()

    def auto_close_popup(self, dt):
        if self.popup and self.popup.content:
            self.popup.dismiss()
            self.send_alert()

    def send_alert(self):

        from Screens.AddContactScreen import AddContactScreen
        temp = AddContactScreen()
        user_id_file = './user_id.txt'
        userid = ''
        if os.path.exists(user_id_file):
            with open(user_id_file, 'r') as f:
                userid = f.read().strip()
        contact_list = temp.fetch_contacts()
        for i in contact_list:
            from smsTest import send_message
            send_message(i['phone_number'], i['message'])
