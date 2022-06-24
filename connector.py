from kivy.graphics import Ellipse, Color
import math


class Connectors():
    def __init__(self, ellipse_condition_pos , canvas, bezier_aray) -> None:
        self.radius = 5
        self.ellipse_condition_pos = ellipse_condition_pos
        self.canvas = canvas
        self.connector_image = []
        self.connectors_position = self.connector_pos(self.ellipse_condition_pos)
        self.active_connector = False
 
    def connector_pos(self, ellips_pos):
        '''Формрование центров координат коннекторов.'''
        pos_x, pos_y = ellips_pos
        conn_1 = [pos_x-self.radius, pos_y+45]
        conn_2 = [pos_x+45, pos_y-self.radius]
        conn_3 = [pos_x+95, pos_y+45]
        conn_4 = [pos_x+45, pos_y+95]

        return [conn_1, conn_2, conn_3, conn_4]

    def show_connectors(self):
        '''Отображение коннекторов.'''
        with self.canvas:
            Color(1,0,0)
            for conn in self.connectors_position:
                self.connector_image.append(Ellipse(pos=[conn[0],conn[1]], size=(2*self.radius, 2*self.radius)))

    def hide_connectors(self):
        '''Скрытие коннекторов.'''
        for conn in self.connector_image: self.canvas.remove(conn)
        self.connector_image = []

    def find_select_connector(self, touch_position):
        '''Определяет пересечение курсорва мыши с коннектором.'''
        for i, connector_position in enumerate(self.connectors_position):
            x0, y0 = connector_position
            x1, y1 = touch_position
            if math.sqrt((x1-x0-self.radius)**2+(y1-y0-self.radius)**2) <= self.radius:
                self.active_connector = i
                return True
        self.active_connector = False
        return False

    def change_connectors_position(self, ox, oy):
   
        for i in range(4):
            self.connectors_position[i][0] += ox 
            self.connectors_position[i][1] += oy
            self.connector_image[i].pos = (self.connector_image[i].pos[0]+ox,  self.connector_image[i].pos[1]+oy)
        
    def get_position_connector(self, connector):

            x, y =  self.connectors_position[connector]
            
            return x, y
       
