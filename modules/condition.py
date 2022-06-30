from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color, Line
import math
from settings import *


class Condition():
    def __init__(self, canvas, position:list, count) -> None:
        self.canvas = canvas
        self.condition_position = position
        #счетчик для лайблов
        self.count = count
        self.radius_condition = RADIUS_CONDITION
        self.radius_connector = RADIUS_CONNECTOR
        #----condition & label
        self.condition_image = None
        self.label_image = None
        #----connector
        self.connector_image = []
        self.connectors_position = self.set_connector_position()
        self.active_connector = False
        #----lighter
        self.lighter_image = None
        #создание состояния
        self.add_condition()

    #создание нового состояния
    def add_condition(self)->None:
        with self.canvas:
            Color(rgb=COLOR_DEFAULD)
            self.condition_image = Ellipse(pos=self.condition_position, size=(2*self.radius_condition,2*self.radius_condition))
            self.label_image = Label(text=str(self.count), 
                                     font_size = FONT_SIZE_LABEL_CONDITION, 
                                     halign='left', 
                                     pos=self.condition_position, 
                                     color=COLOR_TEXT_CONDITION
                                    )

    def move_condition(self, touch)->None:
        old_x, old_y, new_x, new_y = *self.condition_position, touch.x, touch.y
        # новое положение состояния
        self.condition_position = [new_x-self.radius_condition, new_y-self.radius_condition]
        self.condition_image.pos = self.condition_position
        # разница между курсором и центром элипса
        ox = new_x-old_x-self.radius_condition
        oy = new_y-old_y-self.radius_condition
        # новое положение обводки
        points = self.lighter_image.points[:]
        for i in range(len(points)):
            if not i % 2:
                points[i] += ox
                points[i + 1] += oy
        self.lighter_image.points = points
        # новое положение коннекторов
        for i in range(4):
            self.connectors_position[i][0] += ox 
            self.connectors_position[i][1] += oy
            self.connector_image[i].pos = (self.connectors_position[i][0], self.connectors_position[i][1])
        # новое положение лейбла   
        self.label_image.pos = (self.label_image.pos[0]+ox, self.label_image.pos[1]+oy)

    def change_lable_count(self, new_count)->None:
        self.count = new_count
        self.label_image.text = str(self.count)
        
    #######################################
    ## Управление коннекторами состояния ##
    #######################################

    def set_connector_position(self):
        '''Формрование центров координат коннекторов.'''
        pos_x, pos_y = self.condition_position
        conn_1 = [pos_x-self.radius_connector, pos_y+self.radius_condition-self.radius_connector]
        conn_2 = [pos_x+self.radius_condition-self.radius_connector, pos_y-self.radius_connector]
        conn_3 = [pos_x+2*self.radius_condition-self.radius_connector, pos_y+self.radius_condition-self.radius_connector]
        conn_4 = [pos_x+self.radius_condition-self.radius_connector, pos_y+2*self.radius_condition-self.radius_connector]

        return [conn_1, conn_2, conn_3, conn_4]

    def show_connectors(self):
        '''Отображение коннекторов.'''
        with self.canvas:
            Color(rgb=COLOR_CONNECTOR)
            for conn in self.connectors_position:
                self.connector_image.append(Ellipse(pos=[conn[0],conn[1]], size=(2*self.radius_connector, 2*self.radius_connector)))

    def hide_connectors(self):
        '''Скрытие коннекторов.'''
        for conn in self.connector_image: self.canvas.remove(conn)
        self.connector_image = []

    def find_select_connector(self, touch_position):
        '''Определяет пересечение курсорва мыши с коннектором.'''
        for i, connector_position in enumerate(self.connectors_position):
            x0, y0 = connector_position
            x1, y1 = touch_position
            if math.sqrt((x1-x0-self.radius_connector)**2+(y1-y0-self.radius_connector)**2) <= self.radius_connector:
                self.active_connector = i
                return True
        self.active_connector = False
        return False
        
    def get_position_connector(self, connector):
            x, y =  self.connectors_position[connector]
            
            return x, y
       
    #######################################
    ### Управление выделением состояния ###
    #######################################

    def show_lighter(self)->None:
        '''Отображение выделителя.'''
        if not self.lighter_image:
            with self.canvas:
                Color(rgb=COLOR_SELECTED)
                self.lighter_image = Line(circle=(self.condition_position[0]+self.radius_condition,
                                                self.condition_position[1]+self.radius_condition,
                                                self.radius_condition
                                                ),
                                                width=WIDTH_LIGHTER
                                      )
    def hide_lighter(self)->None:
        '''Скрытие выделителя.'''
        if self.label_image:
            self.canvas.remove(self.lighter_image)
            self.lighter_image = None

    #----------------------------

    def __del__(self):
        self.hide_connectors()
        self.hide_lighter()
        self.canvas.remove(self.condition_image)
        self.canvas.remove(self.label_image.canvas)