from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector


class Condition(Widget):
    def on_touch_down(self, touch):
        print('f', touch)
        return super().on_touch_down(touch)


class LaplaceApp(App):
    def build(self):
        return Condition()


if __name__ == '__main__':
    LaplaceApp().run()