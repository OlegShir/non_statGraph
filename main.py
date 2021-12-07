from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Ellipse
from kivy.graphics import Color
from kivy.graphics import Line
import math


class Condition(Widget):
    
    def __init__(self, **kwargs):
        super(Condition, self).__init__(**kwargs)

        self.count = 0
        self.radius = 50
        self.elli = []
        self.label = []
   

    def on_touch_move(self, touch):

        for el in self.elli:
            x0, y0 ,x1, y1 = el.pos[0], el.pos[1], touch.x, touch.y
            if math.sqrt((x1-x0-self.radius)**2+(y1-y0-self.radius)**2) <= self.radius:
                el.pos = [touch.x-self.radius, touch.y-self.radius]
        return super().on_touch_down(touch)


    def on_touch_down(self, touch):
        
        el = self.definition(touch)
        if el:
            with self.canvas:
                Color(1,1,0)
                Line(circle = (el.pos[0]+50,el.pos[1]+50, self.radius-2), width = 2)

        return super().on_touch_down(touch)

    def definition(self, touch):
        
        for el in self.elli:
            x0, y0 ,x1, y1 = el.pos[0], el.pos[1], touch.x, touch.y
            if math.sqrt((x1-x0-self.radius)**2+(y1-y0-self.radius)**2) <= self.radius:
                return el
            else:
                return False


class LaplaceApp(App):
    def build(self):
        parent = Widget()
        self.painter = Condition()
        parent.add_widget(self.painter)

        parent.add_widget(Button(text = 'Добавить\n состояние', halign='center', on_press=self.add_condition, size =(100,50)))
        parent.add_widget(Button(text = 'Удалить\n состояние', halign='center', on_press=self.add_condition, pos  = (105,0), size =(100,50)))
        
        return parent

    def add_condition(self, instance):
        with self.painter.canvas:
            Color(1,1,1)
            self.painter.elli.append(Ellipse(pos=(200,200), size=(2*self.painter.radius,2*self.painter.radius)))
            self.painter.count += 1

    def del_condition(self, instance):
        pass
 
if __name__ == '__main__':
    LaplaceApp().run()