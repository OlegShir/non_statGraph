import math

class Geometric:
    def __init__(self) -> None:
        pass

    def cross_cursor_ellipse(witget_pos: tuple, touch_pos:tuple, radius:int)-> bool:
        x0, y0 = witget_pos
        x1, y1 = touch_pos
        if math.sqrt((x1-x0-radius)**2+(y1-y0-radius)**2) <= radius:
            return True
        else:
            return False



        

    def connector_pos(self, ellips_pos):
        '''
        Формрование центров координат коннекторов
        '''
        pos_x, pos_y = ellips_pos
        conn_1 = (pos_x, pos_y+25)
        conn_2 = (pos_x+25, pos_y)
        conn_3 = (pos_x+50, pos_y+25)
        conn_4 = (pos_x+25, pos_y+50)

        return [conn_1, conn_2, conn_3, conn_4]

if __name__ == "__main__":
    g = Geometric()
    print(g.connector_pos((0,0)))
    
