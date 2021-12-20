from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Ellipse
from kivy.graphics import Color
from kivy.graphics import Line
import math
from math_func import Geometric

geo = Geometric()


class Condition(Widget):
      
    def __init__(self, **kwargs):
        super(Condition, self).__init__(**kwargs)
        
        self.count = 0
        self.radius = 50
        self.elps = []
        self.check_elps = None
        self.line = None
        self.active_elp = None

        Window.bind(mouse_pos=self.on_motion)
    
    def on_motion(self, window, pos):
        for elp in self.elps:
            if geo.cross_cursor_ellipse(elp.pos, pos, self.radius):
                if not self.line:
                    with self.canvas:
                        Color(1,0,0)
                        self.line = Line(circle = (elp.pos[0]+50, elp.pos[1]+50, self.radius-2), width = 2)
                        
                self.active_elp = elp
        
        if self.active_elp:
            if math.sqrt((x1- self.active_elp.pos[0]-self.radius)**2+(y1-self.active_elp.pos[1]-self.radius)**2) > self.radius:
                self.active_elp = None
                self.canvas.remove(self.line)
                self.line = None


    def on_touch_down(self, touch):
        '''
        if self.active_elp:
            if self.line:
                self.canvas.remove(self.line)
            with self.canvas:
                Color(1,1,0)
                self.line = Line(circle = (self.active_elp.pos[0]+50, self.active_elp.pos[1]+50, self.radius-2), width = 2)
                self.check_elps = self.active_elp
        return super().on_touch_down(touch)
        '''

    def on_touch_move(self, touch):
        #на рефакирпе сделатьпередачу через touch.ud["select_elp"] и self.collide_point
        if self.active_elp:
            elp = self.active_elp
            x0, y0 ,x1, y1 = elp.pos[0], elp.pos[1], touch.x, touch.y
            # разница между курсором и центром круга
            ox = x1-x0-self.radius
            oy = y1-y0-self.radius
            # новое положение состояния
            elp.pos = [touch.x-self.radius, touch.y-self.radius]
            # перемещение выделителя
            points = self.line.points[:]
            for i in range(len(points)):
                if not i % 2:
                    points[i] += ox
                    points[i + 1] += oy
                self.line.points = points
        return super().on_touch_down(touch)


class LaplaceApp(App):
    def build(self):
        parent = Widget()
        self.painter = Condition()
        parent.add_widget(self.painter)

        parent.add_widget(Button(text = 'Добавить\n состояние', halign='center', on_press=self.add_condition, size =(100,50)))
        parent.add_widget(Button(text = 'Удалить\n состояние', halign='center', on_press=self.del_condition, pos  = (105,0), size =(100,50)))
        parent.add_widget(Button(text = 'Добавить\n переход', halign='center', on_press=self.add_connection, pos  = (210,0), size =(100,50)))
        
        return parent

    def add_condition(self, instance):
        with self.painter.canvas:
            Color(1,1,1)
            self.painter.elps.append(Ellipse(pos=(200,200), size=(2*self.painter.radius,2*self.painter.radius)))
            self.painter.count += 1

    def del_condition(self, instance):
        if self.painter.elps and self.painter.check_elps:
            #получаем инднкс выбранного состояния
            index_elp = self.painter.elps.index(self.painter.check_elps)
            #удаляем из спсиска
            self.painter.elps.pop(index_elp)
            #удаляем из канваса состаяние и выделитель
            self.painter.canvas.remove(self.painter.check_elps)
            self.painter.canvas.remove(self.painter.line)
            self.painter.count -= 1

    def add_connection(self, instance):
        if self.painter.check_elps:
            pass

 
if __name__ == '__main__':
    LaplaceApp().run()