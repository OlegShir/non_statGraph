from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector


class Condition(Widget):
    pass


class Solver(Widget):
    pass


class LaplaceApp(App):
    def build(self):
        return Solver()


if __name__ == '__main__':
    LaplaceApp().run()