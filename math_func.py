import math
from typing import Tuple

class Geometric:
    def __init__(self) -> None:
        pass

    def cross_cursor(self, witget, touch_position, radius,)-> bool:
        ''' first argument is widget, second cursor'''
        x0, y0 = witget
        x1, y1 = touch_position
        if math.sqrt((x1-x0-radius)**2+(y1-y0-radius)**2) <= radius:
            return True
        else:
            return False



        

    def connector_pos(self, ellips_pos):
        '''
        Формрование центров координат коннекторов
        '''
        print(ellips_pos)
        pos_x, pos_y = ellips_pos
        conn_1 = (pos_x, pos_y+50)
        conn_2 = (pos_x+50, pos_y)
        conn_3 = (pos_x+100, pos_y+50)
        conn_4 = (pos_x+50, pos_y+100)

        return [conn_1, conn_2, conn_3, conn_4]

if __name__ == "__main__":
    g = Geometric()
    a=(333,455)
    b=(434,434)
    print(g.cross_cursor_ellipse(a,b,55))
    
