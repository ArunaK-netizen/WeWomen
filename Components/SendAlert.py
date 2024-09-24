from kivy.graphics import RoundedRectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import threading
from kivy.uix.button import Button
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv



class EmergencyButton(BoxLayout):
    def __init__(self, **kwargs):
        super(EmergencyButton, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (20, 20)
        self.size_hint = (None, None)
        self.size = (Window.size[1] / 2, 200)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.20}

        with self.canvas.before:
            Color(240 / 255, 241 / 255, 255 / 255, 1)
            self.background = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(pos=self.update_background, size=self.update_background)

        # Title Label
        title = Label(
            text="Emergency Call",
            size_hint=(1, None),
            height=50,
            font_size='18sp',
            bold=True,
            pos_hint={'x': -0.25, 'center_y': 0},
            font_name='./Fonts/lexenddeca.ttf',
            color=(0,0,0, 1),
        )

        # Predefined Text Label
        text_box = Label(
            text="This is the predefined text inside the box.\n"
                 "It serves as the body content.",
            size_hint=(1, 1),
            font_size='14sp',
            color=(0,0,0, 1),
            halign='left',
            valign='top',
            font_name='./Fonts/poppins.ttf'
        )
        text_box.bind(size=text_box.setter('text_size'))

        # Button at Bottom Right
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        button_layout.add_widget(Label(size_hint_x=1))  # Spacer to push button to right
        self.action_button = Button(
            text="Send",
            size=(150, 40),
            background_color=(240 / 255, 241 / 255, 255 / 255, 1),
            color=(86 / 255, 100 / 255, 245 / 255, 1),
            background_normal='',
            font_name='./Fonts/lexenddeca.ttf'

        )
        button_layout.add_widget(self.action_button)

        self.add_widget(title)
        self.add_widget(text_box)
        self.add_widget(button_layout)
        self.count = 0

    def update_background(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size