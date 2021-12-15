class Geometric:
    def __init__(self) -> None:
        pass

    def cross_cursor_ellipse(self):



        

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
    
