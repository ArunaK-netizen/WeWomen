from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
import firebase_admin
from firebase_admin import credentials
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from Components.StartListening import CustomTextBox
from Components.ContactsTextBox import addContacts
from Components.SendAlert import EmergencyButton
from Screens.AddContactScreen import AddContactScreen

# Set the window size (for desktop testing)
Window.size = (360, 700)

# Firebase setup
# cred = credentials.Certificate('./Firebase/firebase-cred.json')
# firebase_admin.initialize_app(cred)
#
# # Define the authentication screen





class MainAppScreen(Screen):
    def __init__(self, **kwargs):
        super(MainAppScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = FloatLayout()

        # Creating the navbar as an instance attribute
        self.navbar = FloatLayout(size_hint_y=None, height=60, width=Window.size[0], pos_hint={'top': 1})

        with self.navbar.canvas.before:
            # Background color
            Color(1, 1, 1, 1)
            self.navbar_background = Rectangle(size=self.navbar.size, pos=self.navbar.pos)

        # Add shadow effect using a semi-transparent rectangle
        with self.navbar.canvas.after:
            # Shadow color with transparency
            Color(0, 0, 0, 0.2)  # Black with 20% opacity
            self.shadow = Rectangle(
                size=(self.navbar.width, 10),  # Width matches navbar, adjust height for shadow depth
                pos=(self.navbar.x, self.navbar.y - 10)
            )

        self.navbar.bind(size=self._update_navbar_rect, pos=self._update_navbar_rect)

        # Logo on the left
        logo_label = Label(
            text="WeWomen",
            font_size='18sp',
            size_hint=(None, None),
            size=(100, 50),
            color=(86 / 255, 100 / 255, 245 / 255, 1),
            pos_hint={'x': 0.05, 'center_y': 0.5},
            font_name='./Fonts/lexenddeca.ttf'
        )

        # Notification icon on the right
        self.notification_button = Image(
            source='notification.png',
            size_hint=(None, None),
            size=(25, 25),
            pos_hint={'right': 0.95, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=False
        )
        self.notification_button.bind(on_touch_down=self.go_to_contacts)

        self.navbar.add_widget(logo_label)
        self.navbar.add_widget(self.notification_button)

        # Add navbar to the layout
        layout.add_widget(self.navbar)

        # Add some main app widgets
        self.username_label = Label(
            text="Welcome to WeWomen!",
            font_size='16sp',
            bold=True,
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.30, 'center_y': 0.88},
            color=(0, 0, 0, 1),
            font_name='./Fonts/lexenddeca.ttf'
        )
        layout.add_widget(self.username_label)

        custom_textbox = CustomTextBox()
        layout.add_widget(custom_textbox)
        add_contacts = addContacts()
        layout.add_widget(add_contacts)
        emergency_call = EmergencyButton()
        layout.add_widget(emergency_call)

        self.add_widget(layout)

    def _update_navbar_rect(self, *args):
        self.navbar_background.size = self.navbar.size
        self.navbar_background.pos = self.navbar.pos

        # Update shadow position and size
        self.shadow.size = (self.navbar.width, 1)  # Adjust height for shadow depth
        self.shadow.pos = (self.navbar.x, self.navbar.y - 10)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_username(self, username):
        self.username_label.text = f"Welcome {username.capitalize()}!"

    def go_to_contacts(self, instance, touch):
        if self.notification_button.collide_point(*touch.pos):
            self.manager.current = 'contacts'  # Navigate to contacts screen



class GreetingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainAppScreen(name='main'))
        # sm.add_widget(AddContactsScreen(name='contact_add_screen'))
        sm.add_widget(AddContactScreen(name='contact_add_screen'))

        return sm

if __name__ == "__main__":
    GreetingApp().run()
