import math
from typing import Tuple

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
        conn_1 = (pos_x-5, pos_y+45)
        conn_2 = (pos_x+45, pos_y-5)
        conn_3 = (pos_x+95, pos_y+45)
        conn_4 = (pos_x+45, pos_y+95)

        return [conn_1, conn_2, conn_3, conn_4]

if __name__ == "__main__":
    g = Geometric()
    a=(333,455)
    b=(434,434)
    print(g.cross_cursor_ellipse(a,b,55))
    
