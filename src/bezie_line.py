from kivy.graphics import Bezier, Ellipse, Color, Triangle
from kivy.uix.label import Label
import math
from settings import *


class Bezier_line():
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        self.size_radius_ellips: tuple = (
            RADIUS_BEZIER_POINT, RADIUS_BEZIER_POINT)
        self.size_arrow: int = SIZE_ARROW
        self.position_bezie: list = []
        self.points_control: list = []
        self.points_triangle: list = []
        self.position_label_bezie: list = [0, 0]
        self.bezierline: Bezier = None
        self.triangle: Triangle = None
        self.bezierline_conn: Ellipse = None
        self.law_param: list or bool = False
        # создание контейнера для хранения надписей законов распределения
        self.label_bezie_text: str = ''
        self.label_bezie: Label = self.create_label()

        self.is_loop: bool = False
        self.is_full_law_param: bool = False

    def start_create_bezier_line(self) -> None:
        # принажатии на коннектор создаются экземпляры
        with self.canvas:
            Color(rgb=COLOR_BEZIE_LINE)
            self.bezierline = Bezier()
            self.triangle = Triangle(points=[0, 0, 0, 0, 0, 0])
            self.bezierline_conn = Ellipse(size=self.size_radius_ellips)

    def end_create_bzezier_line(self, end_x: float, end_y: float) -> None:
        """Метод необходим для корректировки конца линии Безье"""
        x0, y0, _, _, _, _ = self.position_bezie
        self.drawing_bezier_line(
            [x0, y0, end_x+RADIUS_CONNECTOR, end_y+RADIUS_CONNECTOR], 'draw straight line')

    def start_create_bzezier_line(self, start_x: float, start_y: float) -> None:
        """Метод необходим для корректировки конца линии Безье"""
        _, _, _, _, x1, y1 = self.position_bezie
        self.drawing_bezier_line(
            [start_x+RADIUS_CONNECTOR, start_y+RADIUS_CONNECTOR, x1, y1], 'draw straight line')

    def drawing_bezier_line(self, array_points: list, terms: str) -> list:
        # в случае если ресуется прямая лния
        if terms == 'draw straight line':
            if len(array_points) == 2:
                x0, y0, _, _, _, _ = self.position_bezie
                x1, y1 = array_points
            else:
                x0, y0, x1, y1 = array_points
            x_mid = (x1+x0)/2
            y_mid = (y1+y0)/2
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
            x0, y0, x, y, x1, y1 = self.position_bezie
            x_mid = x + ox
            y_mid = y + oy
        # в случае перересовывания во время изменения начальной точки
        elif terms == 'change start point':
            ox, oy = array_points
            x_old, y_old, x, y, x1, y1 = self.position_bezie
            x0 = x_old + ox
            y0 = y_old + oy
            if self.is_loop:
                x_mid = x
                y_mid = y
            else:
                x_mid = x + ox
                y_mid = y + oy
        # в случае перересовывания во время изменения конечная точки
        elif terms == 'change finish point':
            ox, oy = array_points
            x0, y0, x, y, x_old, y_old = self.position_bezie
            x1 = x_old + ox
            y1 = y_old + oy
            x_mid = x + ox
            y_mid = y + oy
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
        elif terms == 'loop':
            x0, y0, relative_center_x, relative_center_y, touch_x, touch_y = array_points
            # относительный центр состояния
            xc = relative_center_x + RADIUS_CONDITION
            yc = relative_center_y + RADIUS_CONDITION
            # определение ормированного углового коэффициента между центром состояния и курсором
            angel = self.angle_coefficient2(xc, yc, touch_x, touch_y)
            # перевод в полярную сстему координат
            x1 = RADIUS_CONDITION*math.cos(angel)+xc
            y1 = RADIUS_CONDITION*math.sin(angel)+yc
            # создание петли
            x_mid, y_mid = self.create_loop(x0, y0, x1, y1, xc, yc, angel)
        elif terms == 'finish_loop':
            x0, y0, x_mid, y_mid, _, _ = self.position_bezie
            x1, y1 = array_points

        self.position_bezie = [x0, y0, x_mid, y_mid, x1, y1]
        self.points_control = self.get_coord_point_control(self.position_bezie)
        # перерисрвка
        self.bezierline.points = self.position_bezie
        self.bezierline_conn.pos = self.points_control
        # установка бирки для линии Безье

        self.position_label_bezie = self.points_control
        self.label_bezie.pos = self.position_label_bezie

        if math.sqrt((x1-x0)**2+(y1-y0)**2) > 20:
            self.points_triangle = self.create_arrow_position(
                x_mid, y_mid, x1, y1)
            self.triangle.points = self.points_triangle

        return [x0, y0, x_mid, y_mid, x1, y1]

    def create_arrow_position(self, x_start_bezie: float, y_start_bezie: float, x_finish_bezie: float, y_finish_bezie: float) -> list:
        '''Построение стрелок для линий Безье.'''
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
        # определение угла поворота
        angle = self.angle_coefficient(
            x_start_bezie, y_start_bezie, x_finish_bezie, y_finish_bezie)
        # определение новых точек при повороте
        x2, y2 = self.turn_point_to_angle(x2, y2, x1, y1, angle)
        x3, y3 = self.turn_point_to_angle(x3, y3, x1, y1, angle)

        return [x1, y1, x2, y2, x3, y3]

    def angle_coefficient(self, x0: float, y0: float, x1: float, y1: float) -> float:
        '''Определения углового коэффициента отрезка.'''
        c = 0
        # если отрезок уходит во 2 или 3 четверть
        if x1 < x0:
            c = math.pi
        if x0 == x1:
            return 0
        return math.atan((y1-y0)/(x1-x0))+c

    def angle_coefficient2(self, x0: float, y0: float, x1: float, y1: float) -> float:
        '''Определения нормированного углового коэффициента отрезка
           для полярной сстемы координат.'''
        if x1 >= x0:
            if x1 == x0 and y1 >= y0:
                return math.pi/2
            if x1 == x0 and y1 <= y0:
                return 3*math.pi/2
            if y1 > y0:
                angel = math.atan((y0-y1)/(x0-x1))
            else:
                angel = 2*math.pi + math.atan((y0-y1)/(x0-x1))
        else:
            if x1 == x0:
                return 2*math.pi
            if y1 <= y0:
                angel = math.pi + math.atan((y1-y0)/(x1-x0))
            else:
                angel = math.pi + math.atan((y0-y1)/(x0-x1))

        return angel

    def create_loop(self, x0: float, y0: float, x1: float, y1: float, xc: float, yc: float, angel: float) -> float:
        '''Метод обеспечивает правильную отрисовку петли линии Безье.'''
        # определение угола между прямой, образованной точками начала и конца линии Безье, и
        # и прямой, образованной точками центра состояния и начала линии Безье
        angel_went = self.angle_coefficient2(
            x0, y0, x1, y1)-self.angle_coefficient2(xc, yc, x0, y0)
        # осуществление поворота координатной оси
        if angel_went < 0:
            angel_went += 2*math.pi
        dop_angel = abs(3*math.pi/2 - angel_went)
        if angel_went <= math.pi:
            dop_angel = -(angel_went - math.pi/2)
        # длина отрезка
        d = math.sqrt((x1-x0)**2+(y1-y0)**2)
        x_half = (x1+x0)/2
        y_half = (y1+y0)/2
        # увкличение дуги
        x_mid = 2.4*d*math.cos(angel+dop_angel)+x_half
        y_mid = 2.4*d*math.sin(angel+dop_angel)+y_half

        return x_mid, y_mid

    def get_coord_point_control(self, list_coord: list) -> list:
        '''Метод возвращает координаты точки контроля для линии Безье 
           в соответствии с уравнением квадратичной кривой для t = 1/2.
                       2                  2
           B(t) = (1-t) P0 + 2t(1-t)P1 + t P2'''
        x0, y0, x_mid, y_mid, x1, y1 = list_coord
        x_point_control = (0.5)**2*x0+0.5*x_mid+0.5**2*x1
        y_point_control = (0.5)**2*y0+0.5*y_mid+0.5**2*y1

        return [x_point_control, y_point_control]

    def turn_point_to_angle(self, x: float, y: float, x_centr: float, y_center: float, angle_rad: float, c: int = 1) -> float:
        '''Поворот точки на требуемый угол относительно выбранного угла.'''
        new_x = (x - x_centr) * math.cos(angle_rad) - \
            (y - y_center) * math.sin(angle_rad) + x_centr*c
        new_y = c*(x - x_centr) * math.sin(angle_rad) + \
            (y - y_center) * math.cos(angle_rad) + y_center*c

        return new_x, new_y

    def change_color(self, color: list) -> None:
        '''Метод изменения цвета линии Безье.'''
        self.remove()
        with self.canvas:
            Color(rgb=color)
            self.bezierline = Bezier(points=self.position_bezie)
            self.triangle = Triangle(points=self.points_triangle)
            self.bezierline_conn = Ellipse(
                pos=self.points_control, size=self.size_radius_ellips)
        self.label_bezie = self.create_label()

    def create_label(self) -> Label:
        # создание бирки для линии Безье
        with self.canvas:
            label = Label(text=self.label_bezie_text,
                          font_size=FONT_SIZE_LABEL_BEZIE,
                          halign='center',
                          pos=self.position_label_bezie,
                          color=COLOR_TEXT
                          )
        return label

    def set_value_label(self, array: list or bool) -> None:
        '''Метод перерисовывает бирку с законом распределения для линии Безье.'''
        # проверка правильности получаемых даннных
        if array:
            try:
                # сохраняем параметры закона в классе
                self.law_param = array
                # далее производится форматирование текста для бирки
                key, param = array
                symbols = LAW_SYMBOLS.get(key)
                param_symbols = LAW_PARAM.get(key)
                text = f'{symbols}\n'
                for i in range(len(param_symbols)):
                    self.is_full_law_param = True if param[i] != '' else False
                    text += f'{param_symbols[i]}{param[i]} '
                self.label_bezie_text = text
                self.label_bezie.text = self.label_bezie_text
            except:
                    pass

    def save_props(self) -> None:
        self.save_props_val = [self.bezierline.points,
                               self.bezierline_conn.pos,
                               self.triangle.points,
                               self.label_bezie.pos,
                               self.position_bezie,
                               self.points_control,
                               self.points_triangle
                               ]

    def load_props(self) -> None:
        if self.save_props_val:
            self.bezierline.points = self.save_props_val[0]
            self.bezierline_conn.pos = self.save_props_val[1]
            self.triangle.points = self.save_props_val[2]
            self.label_bezie.pos = self.save_props_val[3]
            self.position_bezie = self.save_props_val[4]
            self.points_control = self.save_props_val[5]
            self.points_triangle = self.save_props_val[6]

    def remove(self) -> None:
        self.canvas.remove(self.bezierline)
        self.canvas.remove(self.triangle)
        self.canvas.remove(self.bezierline_conn)
        self.canvas.remove(self.label_bezie.canvas)

    def __del__(self) -> None:
        self.remove()
