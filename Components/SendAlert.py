from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import RoundedRectangle, Color
from kivy.core.window import Window
import firebase_admin
from firebase_admin import credentials, db
from kivy.utils import platform
from Screens.AddContactScreen import user_id
# Initialize Firebase (make sure to set this up properly)
cred = credentials.Certificate('firebase-cred.json')


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
            text="Send",
            size=(150, 40),
            background_color=(240 / 255, 241 / 255, 255 / 255, 1),
            color=(86 / 255, 100 / 255, 245 / 255, 1),
            background_normal='',
            font_name='./Fonts/lexenddeca.ttf'
        )
        self.action_button.bind(on_press=self.send_sms_to_contacts)
        button_layout.add_widget(self.action_button)

        self.add_widget(title)
        self.add_widget(text_box)
        self.add_widget(button_layout)

    def update_background(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

    def send_sms_to_contacts(self, instance):
        contacts_ref = db.reference(f'contacts/{user_id}')
        contacts = contacts_ref.get()

        if contacts:

            message = "Emergency! I need help!"
            for contact in contacts.values():
                phone = contact['phone']
                self.send_sms(phone, message)

    def send_sms(self, phone_number, message):
        if platform == 'android':
            from pyjnius import autoclass
            SmsManager = autoclass('android.telephony.SmsManager')
            sms = SmsManager.getDefault()
            sms.sendTextMessage(phone_number, None, message, None, None)
            print(f"SMS sent to {phone_number}: {message}")
        else:
            print("SMS sending is only supported on Android.")

# Note: Ensure you handle permissions for sending SMS in your Kivy app.
