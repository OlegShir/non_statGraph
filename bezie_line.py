from kivy.graphics import Bezier, Ellipse, Color, Triangle
import math

class Bezier_line():
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        self.size_radius_ellips = (5,5)
        self.size_arrow = 10
        self.position = []
        self.bezierline = None
        self.triangle = None
        self.bezierline_conn = None
        self.control_point = []
        
    def start_create_bezier_line(self):
        with self.canvas:
            Color(1,0,0)
            self.bezierline = Bezier()
            self.triangle = Triangle()
            self.bezierline_conn = Ellipse(size=self.size_radius_ellips)

    def stop_create_bzezier_line(self, end_x, end_y): 
        x0, y0, _, _, _, _ = self.position
        self.drawing_bezier_line([x0, y0, end_x+5, end_y+5])

    def drawing_bezier_line(self, array_points:list):
        '''Определение середины отрезка'''
        x0, y0, x1, y1 = array_points
        x_mid = (x1+x0)/2
        y_mid = (y1+y0)/2

        self.control_point = [x_mid-5, y_mid-5]
        self.position = [x0, y0, x_mid, y_mid, x1, y1]
        self.bezierline.points = self.position
        self.bezierline_conn.pos = self.control_point
        
        if math.sqrt((x1-x0)**2+(y1-y0)**2) > 20:
            points_triangle = self.create_arrow_position(x0, y0, x1, y1)
            self.triangle.points = points_triangle


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

    def remove(self):
        self.canvas.remove(self.bezierline)
        self.canvas.remove(self.triangle)
        self.canvas.remove(self.bezierline_conn)
        self.triangle = Triangle()
    