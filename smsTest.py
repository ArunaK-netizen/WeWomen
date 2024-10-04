from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from firebase_admin import credentials, db
import firebase_admin
import uuid
import os
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout

# Set the window background color (optional)
Window.clearcolor = (1, 1, 1, 1)  # White background

# Firebase initialization
cred = credentials.Certificate('firebase-cred.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://wewomen-54c01-default-rtdb.firebaseio.com/'
})

# Path to store user ID
user_id_file = 'user_id.txt'


# Function to load or generate user_id
def get_user_id():
    if os.path.exists(user_id_file):
        with open(user_id_file, 'r') as f:
            return f.read().strip()
    else:
        new_user_id = str(uuid.uuid4())
        with open(user_id_file, 'w') as f:
            f.write(new_user_id)
        return new_user_id


# Get the user_id (existing or newly generated)
user_id = get_user_id()


# AddContactsScreen to input name and phone number
class AddContactScreen(Screen):
    def __init__(self, **kwargs):
        super(AddContactScreen, self).__init__(**kwargs)

        # AnchorLayout to center the content
        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')

        # BoxLayout to hold the inputs and button
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint=(None, None), size=(300, 250))

        # Name input
        self.name_input = TextInput(
            hint_text="Enter Name",
            multiline=False,
            size_hint=(None, None),
            height=40,
            width=300,
            background_color=(1, 1, 1, 1),  # White background
            foreground_color=(0, 0, 0, 1),  # Black text
            font_name='./Fonts/poppins.ttf'
        )
        layout.add_widget(self.name_input)

        # Phone number input
        self.phone_input = TextInput(
            hint_text="Enter Phone Number",
            multiline=False,
            size_hint=(None, None),
            height=40,
            width=300,
            background_color=(1, 1, 1, 1),  # White background
            foreground_color=(0, 0, 0, 1),  # Black text
            font_name = './Fonts/poppins.ttf'
        )
        layout.add_widget(self.phone_input)

        # Save button
        save_button = Button(
            text="Save Contact",
            size_hint=(None, None),
            height=40,
            width=300,
            background_color=(86 / 255, 100 / 255, 245 / 255, 1),  # Blue button
            color=(1, 1, 1, 1),  # White text
            font_name='./Fonts/poppins.ttf'
        )
        save_button.bind(on_press=self.save_contact)
        layout.add_widget(save_button)

        # Back button
        back_button = Button(
            text="Back",
            size_hint=(None, None),
            height=40,
            width=300,
            background_color=(86 / 255, 100 / 255, 245 / 255, 1),  # Grey button
            color=(1, 1, 1, 1),  # White text
            font_name='./Fonts/poppins.ttf'
        )
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        # Add the BoxLayout to AnchorLayout to center it
        anchor_layout.add_widget(layout)
        self.add_widget(anchor_layout)

    def save_contact(self, instance):
        name = self.name_input.text
        phone = self.phone_input.text

        # Make sure both fields are not empty
        if name and phone:
            # Store contact in Firebase
            user_ref = db.reference(f'contacts/{user_id}')
            user_ref.push({
                'name': name,
                'phone': phone
            })
            print(f"Saved {name} with phone number {phone} to Firebase.")
        else:
            print("Please enter both name and phone number.")

    # Function to navigate back to the previous screen
    def go_back(self, instance):
        self.manager.current = self.manager.previous()

    def fetch_contacts(self):
        user_ref = db.reference(f'contacts/{user_id}')  # Reference to the user's contacts
        contacts_data = user_ref.get()  # Get all contacts for the user

        contact_list = []
        if contacts_data:  # Check if there's any data
            for key, contact in contacts_data.items():

                contact_list.append(contact)  # Append each contact to the list
        else:

            print("No contacts found.")

        return contact_list


