from kivy.graphics import Bezier, Ellipse, Color, Triangle
import math
from settings import *

class Bezier_line():
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        self.size_radius_ellips = (5,5)
        self.size_arrow = 10

        self.position_bezie = []
        self.points_control = []
        self.points_triangle = []

        self.bezierline = None
        self.triangle = None
        self.bezierline_conn = None
        
    def start_create_bezier_line(self):
        with self.canvas:
            Color(rgb=COLOR_DEFAULD)
            self.bezierline = Bezier()
            self.triangle = Triangle()
            self.bezierline_conn = Ellipse(size=self.size_radius_ellips)

    def end_create_bzezier_line(self, end_x, end_y): 
        x0, y0, _, _, _, _ = self.position_bezie
        self.drawing_bezier_line([x0, y0, end_x+5, end_y+5],'draw straight line')

    def drawing_bezier_line(self, array_points:list, terms):
        # в случае если ресуется прямая лния
        if terms == 'draw straight line':
            x0, y0, x1, y1 = array_points
            x_mid = (x1+x0)/2
            y_mid = (y1+y0)/2
            self.points_control = [x_mid-5, y_mid-5]
        # в случае перересовывания во время изменения средней точки
        elif terms == 'change middle point':
            # положение курсора
            touch_x, touch_y = array_points
            # старое положение средней точки
            x_old, y_old = self.points_control
            # разница между курсором и точкой линии безье
            ox = 2*(touch_x-x_old -5)
            oy = 2*(touch_y-y_old -5)
            # новое положение средней точки
            self.points_control = [touch_x - 5, touch_y -5]
            x0, y0, x, y, x1, y1 = self.position_bezie
            x_mid = x + ox
            y_mid = y + oy
        # в случае перересовывания во время изменения начальной точки
        elif terms == 'change start point':
            ox, oy = array_points
            x_old, y_old, x, y, x1, y1 = self.position_bezie

            x0 = x_old + ox 
            y0 = y_old + oy 
            x_mid = x + ox
            y_mid = y + oy
            print(x0, y0, x_mid, y_mid, x1, y1)

        self.position_bezie = [x0, y0, x_mid, y_mid, x1, y1]
        self.bezierline.points = self.position_bezie
        self.bezierline_conn.pos = self.points_control
        
        if math.sqrt((x1-x0)**2+(y1-y0)**2) > 20:
            self.points_triangle = self.create_arrow_position(x_mid, y_mid, x1, y1)
            self.triangle.points = self.points_triangle

        return [x0, y0, x_mid, y_mid, x1, y1]

    def create_arrow_position(self, x_start_bezie, y_start_bezie, x_finish_bezie, y_finish_bezie):
        '''Построение стрелок для линий Безье'''
        #базовый треугольник
        '''        
        x3,y3 0000
              0   0000
              0       00   
              0         00  x1,y1  
              0       00  
              0   0000 
        x2,y2 0000
        '''
        x1 = x_finish_bezie
        y1 = y_finish_bezie

        x2 = x_finish_bezie - self.size_arrow
        y2 = y_finish_bezie - self.size_arrow

        x3 = x_finish_bezie - self.size_arrow
        y3 = y_finish_bezie + self.size_arrow
        #-----------------------
        #определение угла поворота
        angle = self.angle_coefficient(x_start_bezie, y_start_bezie, x_finish_bezie, y_finish_bezie)
        #определение новых точек поворота
        x2,y2 = self.turn_point_to_angle(x2,y2,x1,y1,angle)
        x3,y3 = self.turn_point_to_angle(x3,y3,x1,y1,angle)
        
        return [x1, y1, x2, y2, x3, y3]

    def angle_coefficient(self, x0, y0, x1, y1):
        '''Определения углового коэффициента отрезка'''
        c = 0
        # если отрезок уходит во 2 или 3 степень
        if x1<x0:
            c = math.pi
        if x0==x1:
            return 0
        return math.atan((y1-y0)/(x1-x0))+c

    def turn_point_to_angle(self, x, y, x_centr, y_center, angle_rad):
        '''Поворот точки на требуемый угол относительно выбранного угла'''
        #angle = math.pi/180*angle
        new_x = (x - x_centr) * math.cos(angle_rad) - (y - y_center) * math.sin(angle_rad) + x_centr
        new_y = (x - x_centr) * math.sin(angle_rad) + (y - y_center) * math.cos(angle_rad) + y_center

        return new_x, new_y

    def change_color(self, color):
        self.remove()
        with self.canvas:
            Color(rgb=color)
            self.bezierline = Bezier(points = self.position_bezie)
            self.triangle = Triangle(points = self.points_triangle)
            self.bezierline_conn = Ellipse(pos = self.points_control, size=self.size_radius_ellips)


    def remove(self):
        self.canvas.remove(self.bezierline)
        self.canvas.remove(self.triangle)
        self.canvas.remove(self.bezierline_conn)

    def delete(self):
        pass
    