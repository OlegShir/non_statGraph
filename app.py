from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle

Window.set_system_cursor('crosshair')

DRAG_START = ()
DRAG_END = ()
DRAGGING = False


class Widget(BoxLayout):
    def __init__(self, **kwargs):
        super(Widget, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.mouse_pos)
        self.bind(pos=self.draw)
        self.bind(size=self.draw)
        self.layout1 = BoxLayout(opacity=1)
        self.add_widget(self.layout1)

    def draw(self, *args):
        self.layout1.canvas.clear()
        with self.canvas.before:
            Color(0.6, 0.6, 0.6, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

    def drawLine(self, mPos):
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0, 1)
            Line(
                points=[DRAG_START[0], DRAG_START[1], mPos[0], mPos[1]],
                width=1.4)

    def mouse_pos(self, window, pos):
        if DRAGGING == True:
            self.drawLine(pos)

    def on_touch_down(self, event):
        global DRAGGING, DRAG_START
        DRAGGING = True
        DRAG_START = event.pos

    def on_touch_up(self, event):
        global DRAGGING, DRAG_END
        DRAGGING = False
        DRAG_END = event.pos


class App(App):
    title = "Kivy Click Drag Line"

    def build(self):
        return Widget()


if __name__ == "__main__":
    App().run()