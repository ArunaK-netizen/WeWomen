from kivy.graphics import RoundedRectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button


class addContacts(BoxLayout):
    def __init__(self, **kwargs):
        super(addContacts, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (20, 20)
        self.size_hint = (None, None)
        self.size = (Window.size[1] / 2, 200)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.45}

        with self.canvas.before:
            Color(240 / 255, 241 / 255, 255 / 255, 1)
            self.background = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(pos=self.update_background, size=self.update_background)

        # Title Label
        title = Label(
            text="Add Contacts",
            size_hint=(1, None),
            height=50,
            font_size='18sp',
            bold=True,
            pos_hint={'x': -0.28, 'center_y': 0},
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
            text="Add",
            size=(150, 40),
            background_color=(240 / 255, 241 / 255, 255 / 255, 1),
            color=(86 / 255, 100 / 255, 245 / 255, 1),
            background_normal='',
            font_name='./Fonts/lexenddeca.ttf'
        )
        self.action_button.bind(on_press=self.go_to_add_contact)

        button_layout.add_widget(self.action_button)

        self.add_widget(title)
        self.add_widget(text_box)
        self.add_widget(button_layout)
        self.count = 0

    def update_background(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

    def go_to_add_contact(self, instance):
        # Switch to AddContactsScreen
        if self.parent and self.parent.parent:
            self.parent.parent.manager.current = 'contact_add_screen'
        else:
            print("ScreenManager not found")
