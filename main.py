from kivy.app import App
from src.control_buttons import ControlButtons


class LaplaceApp(App):
    def build(self):
        self.icon = 'img\src\Logo.png'
        self.title = 'non-statGraph'
        return ControlButtons()


if __name__ == '__main__':
    LaplaceApp().run()
