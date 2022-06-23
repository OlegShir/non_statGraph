import math
import numpy as np

class Geometric:
    def __init__(self) -> None:
        pass

    def cross_cursor(self, witget_position:tuple, touch_position:tuple, radius:int, dopusk:int = 0)-> bool:
        '''Определяет пересечение курсорва мыши с виджетом (элипсом).
        
        Перевый аргумент позиция виджета, второй позиция курсора, третий - радиус элипса,
        четвертый является возможным допуском между курсором и элипсом  '''
        x0, y0 = witget_position
        x1, y1 = touch_position
        if math.sqrt((x1-x0-radius)**2+(y1-y0-radius)**2) <= radius + dopusk:
            return True
        else:
            return False 

    def connector_pos(self, ellips_pos):
        '''
        Формрование центров координат коннекторов
        '''
        pos_x, pos_y = ellips_pos
        conn_1 = [pos_x-5, pos_y+45]
        conn_2 = [pos_x+45, pos_y-5]
        conn_3 = [pos_x+95, pos_y+45]
        conn_4 = [pos_x+45, pos_y+95]

        return [conn_1, conn_2, conn_3, conn_4]

    def connector_number(self, con_pos:list, touch) -> int:
        '''Определение номера коннектора'''

        pass 



    def middle_point(self, array_points:list) -> float and list:
        '''Определение середины отрезка'''
        x0, y0, x1, y1 = array_points
        x_mid = (x1+x0)/2
        y_mid = (y1+y0)/2

        len_line = math.sqrt((x1-x0)**2+(y1-y0)**2)

        return len_line, [x_mid, y_mid]
    
    def turn_point_to_angle(self, x, y, x_centr, y_center, angle_rad):
        '''Поворот точки на требуемый угол относительно выбранного угла'''
        #angle = math.pi/180*angle
        new_x = (x - x_centr) * math.cos(angle_rad) - (y - y_center) * math.sin(angle_rad) + x_centr
        new_y = (x - x_centr) * math.sin(angle_rad) + (y - y_center) * math.cos(angle_rad) + y_center

        return new_x, new_y

    def angle_coeff(self, x0, y0, x1, y1):
        '''Определения углового коэффициента отрезка'''
        c = 0
        # если отрезок уходит во 2 или 3 степень
        if x1<x0:
            c = math.pi
        if x0==x1:
            return 0
        return math.atan((y1-y0)/(x1-x0))+c

    def get_triangle_bezie_line(self, x_start_bezie, y_start_bezie, x_finish_bezie, y_finish_bezie):
        '''Построение стрелок для линий Безье'''
        b = 10
        c = -10
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

        x2 = x_finish_bezie - b
        y2 = y_finish_bezie + c

        x3 = x_finish_bezie - b
        y3 = y_finish_bezie - c
        #-----------------------
        #определение угла поворота
        angle = self.angle_coeff(x_start_bezie, y_start_bezie, x_finish_bezie, y_finish_bezie)
        #определение новых точек поворота
        x2,y2 = self.turn_point_to_angle(x2,y2,x1,y1,angle)
        x3,y3 = self.turn_point_to_angle(x3,y3,x1,y1,angle)
        
        return [x1, y1, x2, y2, x3, y3]

    def three_point_bezie(self, x0, y0, x1, y1, window_size):
        '''Формула для 3-х точечной кривой Безье'''

        min_array = [x1-x0,y1-y0]
        min_value = min(min_array)
        max_value = math.sqrt(window_size[0]**2 + window_size[1]**2)

        
        coef_hight = min_value*0.4*math.pi/180

        x=(x1-x0)*math.cos(coef_hight)-(y1-y0)*math.sin(coef_hight)+x0
        y=(x1-x0)*math.sin(coef_hight)+(y1-y0)*math.cos(coef_hight)+y0

        ''' 
        x=(x1-x0)*math.cos(math.pi/3)-(y1-y0)*math.sin(math.pi/3)+x0
        y=(x1-x0)*math.sin(math.pi/3)+(y1-y0)*math.cos(math.pi/3)+y0
        '''

        return x,y

class Matrix:

    def __init__(self) -> None:
        self.matrix = np.array([0])

    def extension(self, axis = None):
        if not axis:
            shape = self.matrix.shape
            
            try:
                shape_row = shape[1]
            except:
                shape_row = 1
            shape_column = shape[0]

            new_row = np.array(np.zeros(shape_row, dtype=int))
            new_column = np.array(np.zeros((shape_column+1, 1), dtype=int))

            # добавление строки
            self.matrix = np.vstack([self.matrix, new_row])
            # добавление столбца
            self.matrix = np.hstack((self.matrix, new_column))
            
            print(self.matrix)
    
    def compression(self, row_column):
        self.matrix = np.delete(self.matrix, row_column, 0)
        self.matrix = np.delete(self.matrix, row_column, 1)

        print(self.matrix)



if __name__ == "__main__":
    
    
    g = Geometric()

    print(g.angle_coeff(0,0,0,1))
