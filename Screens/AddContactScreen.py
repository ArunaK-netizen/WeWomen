from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

contacts_db = {}

class AddContactsScreen(Screen):
    def __init__(self, **kwargs):
        super(AddContactsScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        # White background
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Logo
        logo_label = Label(
            text="WeWomen",
            font_size='18sp',
            size_hint=(None, None),
            size=(100, 50),
            color=(86 / 255, 100 / 255, 245 / 255, 1),  # Blue color
            pos_hint={'x': 0.05, 'center_y': 0.95},
            font_name='./Fonts/lexenddeca.ttf'
        )
        layout.add_widget(logo_label)

        # Name input
        self.name_input = TextInput(
            hint_text="Enter Contact Name",
            multiline=False,
            font_name="./Fonts/poppins.ttf",
            size_hint=(0.8, None),
            height=40,
            pos_hint={'x': 0.1, 'y': 0.7}
        )
        layout.add_widget(self.name_input)

        # Contact input
        self.contact_input = TextInput(
            hint_text="Enter Contact Number",
            multiline=False,
            font_name="./Fonts/poppins.ttf",
            size_hint=(0.8, None),
            height=40,
            pos_hint={'x': 0.1, 'y': 0.6}
        )
        layout.add_widget(self.contact_input)

        # Add button
        add_button = Button(
            text="Add",
            size_hint=(0.2, None),  # Use size_hint_x for responsive width
            height=50,  # Explicit height
            pos_hint={'x': 0.4, 'y': 0.5},
            background_color=(86 / 255, 100 / 255, 245 / 255, 1),  # Blue color
            color=(1, 1, 1, 1),  # White text
            font_name='./Fonts/lexenddeca.ttf'
        )
        add_button.bind(on_press=self.add_contact)
        layout.add_widget(add_button)

        # Search input
        self.search_input = TextInput(
            hint_text="Search Contact",
            multiline=False,
            font_name="./Fonts/poppins.ttf",
            size_hint=(0.8, None),
            height=40,
            pos_hint={'x': 0.1, 'y': 0.4}
        )
        layout.add_widget(self.search_input)

        # Search button
        search_button = Button(
            text="Search",
            size_hint=(0.2, None),  # Use size_hint_x for responsive width
            height=50,  # Explicit height
            pos_hint={'x': 0.4, 'y': 0.3},
            background_color=(86 / 255, 100 / 255, 245 / 255, 1),  # Blue color
            color=(1, 1, 1, 1),  # White text
            font_name='./Fonts/lexenddeca.ttf'
        )
        search_button.bind(on_press=self.search_contact)
        layout.add_widget(search_button)

        # Contacts list
        self.contacts_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.contacts_layout.bind(minimum_height=self.contacts_layout.setter('height'))
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 200), pos_hint={'x': 0, 'y': 0.05})
        scroll_view.add_widget(self.contacts_layout)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def add_contact(self, instance):
        print("clicked!")
        name = self.name_input.text
        contact = self.contact_input.text
        if name and contact:
            contacts_db[name] = contact
            print(f"Added contact: {name} - {contact}")  # Debug statement
            self.name_input.text = ''
            self.contact_input.text = ''
            self.update_contacts_list()
            self.show_popup("Success", f"Added {name} with contact {contact}")
        else:
            self.show_popup("Error", "Both fields are required")

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, font_name='./Fonts/poppins.ttf'),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

    def search_contact(self, instance):
        search_term = self.search_input.text
        if search_term in contacts_db:
            self.show_popup("Contact Found", f"{search_term}: {contacts_db[search_term]}")
        else:
            self.show_popup("Contact Not Found", "Contact not found")

    def update_contacts_list(self):
        print("Updating contacts list...")  # Debug statement
        self.contacts_layout.clear_widgets()
        for name, contact in contacts_db.items():
            self.contacts_layout.add_widget(Label(
                text=f"{name}: {contact}",
                size_hint_y=None,
                height=40,
                font_name='./Fonts/poppins.ttf'
            ))