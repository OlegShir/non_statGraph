from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.graphics import Color
import math


class Condition(Widget):
    
    

    def __init__(self, **kwargs):
        self.radius = 100
        super(Condition, self).__init__(**kwargs)

        with self.canvas:
            self.elli = Ellipse(pos=(0,0), size=(self.radius,self.radius))


    def on_touch_move(self, touch):
        x0, y0 ,x1, y1 =self.elli.pos[0], self.elli.pos[1], touch.pos[0],touch.pos[1]
        print(x0, y0 ,x1, y1)
        if self.in_circle(x0,x1,y0,y1):
            
            self.elli.pos = touch.pos
        return super().on_touch_down(touch)

    def in_circle(self, x0,x1,y0,y1) -> bool:
        if math.sqrt((x1-x0-50)**2+(y1-y0-50)**2) <= self.radius/2:
            print('y')
            return True
        else:
            print('n')

            return False



class LaplaceApp(App):
    def build(self):
        return Condition()


if __name__ == '__main__':
    LaplaceApp().run()