from kivy.graphics import Bezier, Ellipse, Color, Triangle
from kivy.uix.label import Label
import math
from settings import *


class Bezier_line():
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        self.size_radius_ellips = (RADIUS_BEZIER_POINT, RADIUS_BEZIER_POINT)
        self.size_arrow = SIZE_ARROW

        self.position_bezie = []
        self.points_control = []
        self.points_triangle = []

        self.bezierline = None
        self.triangle = None
        self.bezierline_conn = None

        self.law_param: list or bool = False
        # создание контейнера для хранения надписей законов распределения
        self.label_bezie = self.create_label()

    def start_create_bezier_line(self):
        # принажатии на коннектор создаются экземпляры
        with self.canvas:
            Color(rgb=COLOR_DEFAULD)
            self.bezierline = Bezier()
            self.triangle = Triangle(points=[0, 0, 0, 0, 0, 0])
            self.bezierline_conn = Ellipse(size=self.size_radius_ellips)

    def end_create_bzezier_line(self, end_x, end_y):
        """Метод необходим для корректировки конца линии Бизье"""
        x0, y0, _, _, _, _ = self.position_bezie
        self.drawing_bezier_line(
            [x0, y0, end_x+RADIUS_CONNECTOR, end_y+RADIUS_CONNECTOR], 'draw straight line')

    def start_create_bzezier_line(self, start_x, start_y):
        """Метод необходим для корректировки конца линии Бизье"""
        _, _, _, _, x1, y1 = self.position_bezie
        self.drawing_bezier_line(
            [start_x+RADIUS_CONNECTOR, start_y+RADIUS_CONNECTOR, x1, y1], 'draw straight line')

    def drawing_bezier_line(self, array_points: list, terms):
        # в случае если ресуется прямая лния
        if terms == 'draw straight line':
            if len(array_points) == 2:
                x0, y0, _, _, _, _ = self.position_bezie
                x1, y1 = array_points
            else:
                x0, y0, x1, y1 = array_points
            x_mid = (x1+x0)/2
            y_mid = (y1+y0)/2
            self.points_control = [
                x_mid-RADIUS_BEZIER_POINT, y_mid-RADIUS_BEZIER_POINT]
        # в случае перересовывания во время изменения средней точки
        elif terms == 'change middle point':
            # положение курсора
            touch_x, touch_y = array_points
            # старое положение средней точки
            x_old, y_old = self.points_control
            # разница между курсором и точкой линии безье
            ox = 2*(touch_x-x_old - 5)
            oy = 2*(touch_y-y_old - 5)
            # новое положение средней точки
            self.points_control = [touch_x - 5, touch_y - 5]
            x0, y0, x, y, x1, y1 = self.position_bezie
            x_mid = x + ox
            y_mid = y + oy
        # в случае перересовывания во время изменения начальной точки
        elif terms == 'change start point':
            ox, oy = array_points
            x_old, y_old, x, y, x1, y1 = self.position_bezie
            xx, yy = self.points_control
            x0 = x_old + ox
            y0 = y_old + oy
            x_mid = x + ox
            y_mid = y + oy
            self.points_control = [xx+0.75*ox, yy+.75*oy]
        # в случае перересовывания во время изменения конечная точки
        elif terms == 'change finish point':
            ox, oy = array_points
            x0, y0, x, y, x_old, y_old = self.position_bezie
            xx, yy = self.points_control
            x1 = x_old + ox
            y1 = y_old + oy
            x_mid = x + ox
            y_mid = y + oy
            self.points_control = [xx+.75*ox, yy+.75*oy]
        elif terms == 'in':
            x1, y1 = array_points
            x0, y0, x_mid, y_mid, _, _ = self.position_bezie
            x1 += RADIUS_CONNECTOR
            y1 += RADIUS_CONNECTOR            
        elif terms == 'out':
            x0, y0 = array_points
            _, _, x_mid, y_mid, x1, y1 = self.position_bezie
            x0 += RADIUS_CONNECTOR
            y0 += RADIUS_CONNECTOR
            
        self.position_bezie = [x0, y0, x_mid, y_mid, x1, y1]
        self.bezierline.points = self.position_bezie
        self.bezierline_conn.pos = self.points_control
        self.label_bezie.pos = [x_mid, y_mid]

        if math.sqrt((x1-x0)**2+(y1-y0)**2) > 20:
            self.points_triangle = self.create_arrow_position(
                x_mid, y_mid, x1, y1)
            self.triangle.points = self.points_triangle

        return [x0, y0, x_mid, y_mid, x1, y1]

    def create_arrow_position(self, x_start_bezie, y_start_bezie, x_finish_bezie, y_finish_bezie):
        '''Построение стрелок для линий Безье'''
        # базовый треугольник
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
        # -----------------------
        # определение угла поворота
        angle = self.angle_coefficient(
            x_start_bezie, y_start_bezie, x_finish_bezie, y_finish_bezie)
        # определение новых точек поворота
        x2, y2 = self.turn_point_to_angle(x2, y2, x1, y1, angle)
        x3, y3 = self.turn_point_to_angle(x3, y3, x1, y1, angle)

        return [x1, y1, x2, y2, x3, y3]

    def angle_coefficient(self, x0, y0, x1, y1):
        '''Определения углового коэффициента отрезка.'''
        c = 0
        # если отрезок уходит во 2 или 3 четверть
        if x1 < x0:
            c = math.pi
        if x0 == x1:
            return 0
        return math.atan((y1-y0)/(x1-x0))+c

    def turn_point_to_angle(self, x, y, x_centr, y_center, angle_rad):
        '''Поворот точки на требуемый угол относительно выбранного угла.'''
        new_x = (x - x_centr) * math.cos(angle_rad) - \
            (y - y_center) * math.sin(angle_rad) + x_centr
        new_y = (x - x_centr) * math.sin(angle_rad) + \
            (y - y_center) * math.cos(angle_rad) + y_center

        return new_x, new_y

    def change_color(self, color):
        self.remove()
        with self.canvas:
            Color(rgb=color)
            self.bezierline = Bezier(points=self.position_bezie)
            self.triangle = Triangle(points=self.points_triangle)
            self.bezierline_conn = Ellipse(
                pos=self.points_control, size=self.size_radius_ellips)

    def create_label(self) -> Label:
        # создание бирки для линии Безье
        with self.canvas:
            label = Label(text='',
                          font_size=FONT_SIZE_LABEL_BEZIE,
                          halign='center',
                          pos=(0, 0),
                          color=COLOR_TEXT
                          )
        return label

    def set_value_label(self, array: list or bool) -> None:
        '''Метод перерисовывает бирку с законом распределения для линии Безье'''
        # проверка правильности получаемых даннных
        if array:
            # сохраняем параметры закона в классе
            self.law_param = array
            # далее производится форматирование текста для бирки
            key, param = array
            symbols = LAW_SYMBOLS.get(key)
            param_symbols = LAW_PARAM.get(key)
            text = f'{symbols}\n'
            for i in range(len(param_symbols)):
                text += f'{param_symbols[i]}{param[i]} '
            self.label_bezie.text = text

    def save_props(self):
        self.save_props_val = [self.bezierline.points,
                               self.bezierline_conn.pos,
                               self.triangle.points,
                               self.label_bezie.pos,
                               self.position_bezie,
                               self.points_control,
                               self.points_triangle
                               ]

    def load_props(self):
        if self.save_props_val:
            self.bezierline.points = self.save_props_val[0] 
            self.bezierline_conn.pos = self.save_props_val[1]
            self.triangle.points = self.save_props_val[2]
            self.label_bezie.pos = self.save_props_val[3]
            self.position_bezie = self.save_props_val[4]
            self.points_control = self.save_props_val[5]
            self.points_triangle = self.save_props_val[6]
    
    def remove(self):
        self.canvas.remove(self.bezierline)
        self.canvas.remove(self.triangle)
        self.canvas.remove(self.bezierline_conn)

    def __del__(self):
        self.remove()
