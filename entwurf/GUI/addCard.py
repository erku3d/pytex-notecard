
#!/usr/bin/env python3

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.label import Label


class addCard(App):
    def build(self):
        return Label(text="hinzufügen")


if __name__ == '__main__':
    pytex_notecardApp().run()



