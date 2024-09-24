from kivy import app
from kivy.graphics import RoundedRectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
class RoundedBox(BoxLayout):
    def __init__(self, **kwargs):
        super(RoundedBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (10, 20, 10, 10)  # Padding inside the box
        self.spacing = 10

        with self.canvas.before:
            Color(1, 1, 1, 1)  # Background color
            self.rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[15]
            )
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Title and body inside the box
        self.title_label = Label(
            text='Title',
            font_size='20sp',
            size_hint_y=None,
            height=40
        )
        self.body_text_input = TextInput(
            text='Body text here...',
            size_hint_y=None,
            height=100,
            multiline=True
        )

        self.add_widget(self.title_label)
        self.add_widget(self.body_text_input)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size