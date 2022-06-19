<<<<<<< HEAD
from re import A
=======
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
<<<<<<< HEAD
from kivy.graphics import Ellipse, Color, Bezier, Line, Triangle
import copy
=======
from kivy.graphics import Ellipse, Color, Bezier, Triangle
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728

from kivy.graphics import Line
import math
from math_func import Geometric, Matrix
geo = Geometric()

<<<<<<< HEAD
import math
from math_func import Geometric, Matrix
geo = Geometric()

=======
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728

class Condition(Widget):
      
    def __init__(self, **kwargs):
        super(Condition, self).__init__(**kwargs)
        
        self.count = 0
<<<<<<< HEAD
        self.radius = 50
        self.labels =[]

        self.elps = []     
        self.active_elp = None

        self.connector = None
        self.active_conn = None

        self.start_draw_bezie = False
        self.bezierline_array =[]
        self.bezierline_conn_array = []
        self.bezierline_conn_move = False
        self.active_bezierline_conn = None

        self.triangle_array = []
        self.check_elps = None
        self.check_elps_line = None

=======
        self.radius = 50                           #размер радиуса элипсов состояний
        self.labels =[]                            #инициализация списка подписей нумерации элипсов состояний 
        self.elps = []                             #инициализация списка элипсов состояний
        self.active_elp = None
        self.connector = None
        self.active_conn = None
        self.start_draw_bezie = False
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
        # отслеживание курсора мышки
        Window.bind(mouse_pos=self.on_motion)


    def on_motion(self, window, touch):
<<<<<<< HEAD
        """Метод отслеживания перемещения мышки по рабочей области.
        """
=======
        
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
        if self.active_elp:           
            # если курсор выходит за радиус элепса + 10 рх
            if not geo.cross_cursor(self.active_elp.pos, touch, self.radius, dopusk=20):
                # удаление конекторов
                for conn in self.connector: self.canvas.remove(conn)
                # очистка переменных
                self.connector = None
                self.active_elp = None
                self.active_conn = None
            else:
                if not self.active_conn:
                    # если попадаем в конектор
                    for i, conn in enumerate(self.connector):
                        if geo.cross_cursor(conn.pos, touch, 5, dopusk=5):
<<<<<<< HEAD
=======
                            
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
                            self.active_conn = conn
                            Window.set_system_cursor("hand")
                else:
                    if not geo.cross_cursor(self.active_conn.pos, touch, 5, dopusk=5):
<<<<<<< HEAD
=======
                        
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
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
<<<<<<< HEAD
            if not self.active_elp and self.bezierline_conn_array != []:
                for bizier_conn in self.bezierline_conn_array:
                    if geo.cross_cursor(bizier_conn.pos, touch, 10, dopusk=5):
                        Window.set_system_cursor("hand")
                        self.bezierline_conn_move = True
                        self.active_bezierline_conn = bizier_conn
                    else:
                        Window.set_system_cursor("arrow")
                        self.bezierline_conn_move = False
                        self.active_bezierline_conn = None
                        


=======
       
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
    def on_touch_down(self, touch):
        #блокировка при соединении элипсов
        if self.active_conn:
            self.start_draw_bezie = True
            # сохранение позиции коннектора от которова производится соединение
            touch.ud['position_active_conn'] = self.active_conn.pos
            # сохранение номера элипса от которова производится соединение
            touch.ud['number_start_elp'] = self.elps.index(self.active_elp)
<<<<<<< HEAD
            # отображение "временной" линии Безье и ее центра
            with self.canvas:
                Color(1,0,0)
                self.bezierline = Bezier()
                self.bezierline_conn = Ellipse(size=(5,5) )
        # выделение состояния
        if self.active_elp and self.active_elp != self.check_elps:
            if self.check_elps: self.canvas.remove(self.check_elps_line)
            with self.canvas:
                Color(1,1,0)
                self.check_elps_line = Line(circle=(self.active_elp.pos[0]+self.radius, self.active_elp.pos[1]+self.radius, self.radius),width=3)
                self.check_elps = self.active_elp
        elif not self.active_elp :
            if self.check_elps: 
                self.canvas.remove(self.check_elps_line)
                self.check_elps = None
            if self.active_bezierline_conn:
                print('Conn active')
        
      
=======
            # отображение "временной" линии Безье
            with self.canvas:
                self.bezierline = Bezier()
            
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):

        # при условии рисования линии Безье
        if self.start_draw_bezie:
            self.start_draw_bezie = False

            # если конец линии Безье не соединен с коннектором
<<<<<<< HEAD
            if self.active_conn:
                # сохранение номера элипса с которым производится соединение
                touch.ud['number_finish_elp'] = self.elps.index(self.active_elp)
                # запись координат начало и конца линии Безье
                point_triangle = geo.get_triangle_bezie_line(self.bezierline.points[0], self.bezierline.points[1], self.active_conn.pos[0]+5,self.active_conn.pos[1]+5)
                with self.canvas:
                    Color(1,1,0)
                    self.triangle_now = Triangle(points = point_triangle)
                    self.bezierline_now = Bezier(points=[self.bezierline.points[0], self.bezierline.points[1], touch.ud['bezie_3_point'][0], touch.ud['bezie_3_point'][1],self.active_conn.pos[0]+5,self.active_conn.pos[1]+5])
                    self.bezierline_conn_now = Ellipse(pos = touch.ud['bezie_3_point'], size=(5,5) )
                self.bezierline_array.append(self.bezierline_now)
                self.bezierline_conn_array.append(self.bezierline_conn)
                self.triangle_array.append(self.triangle_now)
                # список номеров элепсов, которые соединяет линия Безье
                conection = [touch.ud['number_start_elp'],touch.ud['number_finish_elp'] ]
            
            # удаление "временной" линии Безье
            self.canvas.remove(self.bezierline)
            self.canvas.remove(self.bezierline_conn)
                
=======
            if not self.active_conn:
                # удаление "временной" линии Безье
                self.canvas.remove(self.bezierline)
            else:
                # сохранение номера элипса с которым производится соединение
                touch.ud['number_finish_elp'] = self.elps.index(self.active_elp)
                # запись координат начало и конца линии Безье
                self.bezierline.points = [self.bezierline.points[0], self.bezierline.points[1], self.active_conn.pos[0]+5,self.active_conn.pos[1]+5]
                # список номеров элепсов, которые соединяет линия Безье
                conection = [touch.ud['number_start_elp'],touch.ud['number_finish_elp'] ]
                print(conection)
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
 
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        #на рефакирпе сделатьпередачу через touch.ud["select_elp"] и self.collide_point

        # в случае если рисуется линия Безье
        if self.start_draw_bezie:
            # получение координат началалинии Безье            
            x, y = touch.ud['position_active_conn']
<<<<<<< HEAD
            points_bezierline = [x+5 ,y+5, touch.x, touch.y]
            # перерисовка линии Безье
            len_bezierline, points_bezier_conn = geo.middle_point(points_bezierline)
            touch.ud['bezie_3_point']= points_bezier_conn
            #print(  points_bezierline, '--------', points_bezier_conn )
            if len_bezierline > 20:
                self.bezierline_conn.pos = points_bezier_conn
            self.bezierline.points = points_bezierline
        
        elif self.bezierline_conn_move:
            # позиция выбранной точки линии бизье в списке
            index = self.bezierline_conn_array.index(self.active_bezierline_conn)
            x0, y0 ,x1, y1 = *self.active_bezierline_conn.pos, touch.x, touch.y
            # разница между курсором и точки линии безье 
            ox = x1-x0-10
            oy = y1-y0-10
            #получение линии безье, которая будет менятся
            bezierline = self.bezierline_array[index]
            # новое положение середины линии безье
            points = [bezierline.points[0],bezierline.points[1],bezierline.points[2]+ox,bezierline.points[3]+oy,bezierline.points[4],bezierline.points[5]]
            self.bezierline_array[index].points = points
            # новое положение точки линии безье
            opp = [x1-10, y1-10]
            self.bezierline_conn_array[index].pos = opp
            print(self.active_bezierline_conn.pos, '///', touch.x, '///', touch.y, index)
            #изменение стрелки
            point_triangle = geo.get_triangle_bezie_line(points[2],points[3],points[4],points[5])
            self.triangle_array[index].points = point_triangle
                            
=======
            # перерисовка линии Безье
            self.bezierline.points = [x+5 ,y+5, touch.x, touch.y]
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
        # перемещение элипса
        else:
            if self.active_elp:
                # позиция выбранного элипса  в списке
                index = self.elps.index(self.active_elp)
                # получаем координаты для пересчета движения       
                x0, y0 ,x1, y1 = *self.active_elp.pos, touch.x, touch.y
                # разница между курсором и центром элипса
                ox = x1-x0-self.radius
                oy = y1-y0-self.radius
                # новое положение состояния
                self.active_elp.pos = [touch.x-self.radius, touch.y-self.radius]
<<<<<<< HEAD
                # новое положение обводки
                points = self.check_elps_line.points[:]
                for i in range(len(points)):
                    if not i % 2:
                        points[i] += ox
                        points[i + 1] += oy
                self.check_elps_line.points = points
=======
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
                # перемещение конекторов            
                for conn in self.connector:
                    conn.pos = (conn.pos[0]+ox, conn.pos[1]+oy)
                # перемещение подписи
                self.labels[index].pos = (self.labels[index].pos[0]+ox, self.labels[index].pos[1]+oy)

<<<<<<< HEAD


                #print(x0, y0 ,x1, y1)

=======
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
        return super().on_touch_down(touch)

class LaplaceApp(App):
    def build(self):
        parent = Widget()
        self.painter = Condition()
        parent.add_widget(self.painter)

        parent.add_widget(Button(text = 'Добавить\n состояние', halign='center', on_press=self.add_condition, size =(100,50)))
        parent.add_widget(Button(text = 'Удалить\n состояние', halign='center', on_press=self.del_condition, pos  = (105,0), size =(100,50)))

<<<<<<< HEAD
        #self.matrix = Matrix()
=======
        self.matrix = Matrix()
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
        
        return parent

    def add_condition(self, instance):
        with self.painter.canvas:
            Color(1,1,1)
            self.painter.elps.append(Ellipse(pos=(200,200), size=(2*self.painter.radius,2*self.painter.radius),))
            self.painter.labels.append(Label(text=str(self.painter.count), font_size = 60, halign='left', pos=(200,200), color=(0,0,0)))
<<<<<<< HEAD
        #self.matrix.extension()
=======
        self.matrix.extension()
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728
        self.painter.count += 1

    def del_condition(self, instance):
        if self.painter.elps and self.painter.check_elps:
            #получаем инднкс выбранного состояния
            index_elp = self.painter.elps.index(self.painter.check_elps)
            #удаляем из спсиска
            self.painter.elps.pop(index_elp)
<<<<<<< HEAD
            self.painter.labels.pop(index_elp)
            #удаляем из канваса состаяние и выделитель
            self.painter.canvas.remove(self.painter.check_elps)
            self.painter.check_elps = None
            self.painter.canvas.remove(self.painter.check_elps_line)
            self.painter.count -= 1
            self.change_lable_index()
            #self.matrix.compression()
    
    def change_lable_index(self):
        index = 0
        for label in self.painter.labels:
            label.text = str(index)
            index += 1
=======
            #удаляем из канваса состаяние и выделитель
            self.painter.canvas.remove(self.painter.check_elps)
            self.painter.canvas.remove(self.painter.line)
            self.painter.count -= 1
            self.matrix.compression()
>>>>>>> 007e00df46efe58f7abc534dd676b7444324b728

if __name__ == '__main__':
    LaplaceApp().run()