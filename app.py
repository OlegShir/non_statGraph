from kivy.app import runTouchApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from random import random as R
Builder.load_string('''
<Drawing>:
    canvas:
        Color:
            rgba: 1, 0, 0, 0.4
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: 1, 1, 1, 1
''')

class Drawing(Widget):
    def __init__(self, shape=00, **kw):
        super(Drawing, self).__init__(**kw)
        self.size_hint = (None, None)
        with self.canvas:
            pts = [*self.center, 100, 0, 359 * R(), 200]
            if shape==1:
                self.line = Line(circle=pts)
                self.name = 'circle'
            elif shape==2:
                self.line = Line(rectangle=pts[2:])
                self.name = 'rectangle'
            else:
                self.line = Line(points=pts)
                self.name = 'points'


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            print(self.name)
        self.old = self.pos[:]

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        points = self.line.points[:]
        ox = touch.x - self.old[0]
        oy = touch.y - self.old[1]
        for i in range(len(points)):
            if not i % 2:
                points[i] += ox
                points[i + 1] += oy
        self.line.points = points
        self.old = touch.pos
        self.pos = [self.pos[0] + ox, self.pos[1] + oy]


box = BoxLayout()
for i in [0, 1, 2]:
    box.add_widget(Drawing(shape=i, pos=[200 * R(), 100 * R()]))
runTouchApp(box)