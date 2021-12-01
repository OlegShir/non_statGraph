from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Ellipse
from kivy.graphics import Color
import math


class Condition(Widget):
    
    def __init__(self, **kwargs):
        self.count = 0
        self.radius = 50
        self.elli = []
        super(Condition, self).__init__(**kwargs)
        self.inside = GridLayout()
        self.inside.cols = 2
        

        self.btn1 = Button(text='Добавит\n состояние')
        self.btn1.bind(on_press=self.add_condition)
        self.add_widget(self.btn1)

        self.btn2 = Button(text='Удалить состояние')
        self.btn2.bind(on_press=self.del_condition)
        self.add_widget(self.btn2)
 
     
    def on_touch_move(self, touch):

        for el in self.elli:
            x0, y0 ,x1, y1 = el.pos[0], el.pos[1], touch.x, touch.y
            if math.sqrt((x1-x0-self.radius)**2+(y1-y0-self.radius)**2) <= self.radius:
                el.pos = [touch.x-self.radius, touch.y-self.radius]
        return super().on_touch_down(touch)


    def add_condition(self, instance):
        with self.canvas:
            self.elli.append(Ellipse(pos=(200,200), size=(2*self.radius,2*self.radius)))
            print(self.elli[0].pos)

            self.count += 1

    def del_condition(self, instance):
        pass
 



class LaplaceApp(App):
    def build(self):
        return Condition()


if __name__ == '__main__':
    LaplaceApp().run()