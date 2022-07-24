from kivy.app import App
from modules.control_buttons import ControlButtons


class LaplaceApp(App):
    def build(self):
        return ControlButtons()


if __name__ == '__main__':
    LaplaceApp().run()
