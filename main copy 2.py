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

        self.labels =[]
            

        self.elps = []     
        self.active_elp = None

        self.connector = None
        self.active_conn = None
        

        Window.bind(mouse_pos=self.on_motion)
    
    def on_motion(self, window, touch):
        print(window)

        if self.active_elp:
           
            # если курсор выходит за радиус элепса + 10 рх
            if not geo.cross_cursor(self.active_elp.pos, touch, self.radius, dopusk=20):
                # удаление конекторов
                for conn in self.connector: self.canvas.remove(conn)
                self.connector = None
                self.active_elp = None
                self.active_conn =None
            else:
                if not self.active_conn:
                    # если попадаем в конектор
                    for i, conn in enumerate(self.connector):
                        if geo.cross_cursor(conn.pos, touch, 5, dopusk=5):
                            
                            self.active_conn = conn
                            Window.set_system_cursor("hand")
                else:
                    if not geo.cross_cursor(self.active_conn.pos, touch, 5, dopusk=5):
                        self.active_conn = None
                        Window.set_system_cursor("arrow")
                
        else:
            for elp in self.elps:
                # ищем пересечение                
                if geo.cross_cursor(elp.pos, touch, self.radius):
                    # рисуем коннекторы
                    if not self.connector:
                        self.connector = []
                        center_conn = geo.connector_pos(elp.pos)
                        with self.canvas:
                            Color(1,0,0)
                            for conn in center_conn:
                                self.connector.append(Ellipse(pos=(conn[0],conn[1]), size=(self.radius-40,self.radius-40)))
                    # запоминаем выбранное состояние            
                    self.active_elp = elp
            
        


    def on_touch_down(self, touch):
        if self.active_conn:
            touch.ud["conect"] = True








    def on_touch_move(self, touch):
        #на рефакирпе сделатьпередачу через touch.ud["select_elp"] и self.collide_point
        if self.active_elp:
            i = self.elps.index(self.active_elp)
            # получаем координаты для пересчета движения       
            x0, y0 ,x1, y1 = *self.active_elp.pos, touch.x, touch.y
            # разница между курсором и центром элипса
            ox = x1-x0-self.radius
            oy = y1-y0-self.radius
            # новое положение состояния
            self.active_elp.pos = [touch.x-self.radius, touch.y-self.radius]
            # перемещение конекторов            
            for conn in self.connector:
                conn.pos = (conn.pos[0]+ox, conn.pos[1]+oy)
            # перемещение подписи
            self.labels[i].pos = (self.labels[i].pos[0]+ox, self.labels[i].pos[1]+oy)
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
            self.painter.elps.append(Ellipse(pos=(200,200), size=(2*self.painter.radius,2*self.painter.radius),))
            self.painter.labels.append(Label(text=str(self.painter.count), font_size = 60, halign='left', pos=(200,200), color=(0,0,0)))
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