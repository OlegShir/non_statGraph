from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Ellipse, Color, Bezier, Line, Triangle
from numpy import array
from math_func import Geometric, Matrix
from connector import Connectors
from  bezie_line import Bezier_line
geo = Geometric()


class Condition(Widget):
      
    def __init__(self, **kwargs):
        super(Condition, self).__init__(**kwargs)
        
        self.count = 0
        self.radius = 50
        self.labels =[]

        self.elps = []     
        self.active_elp = None

        self.show_connectors = False
        self.active_connector = False
        self.connectors_array = []

        self.bizie_line = None
        self.bezier_line_array =[]
        self.start_draw_bezie = False
        self.active_bezier_line = False
        

        self.check_elps = None
        self.check_elps_line = None

        # отслеживание курсора мышки
        Window.bind(mouse_pos=self.on_motion)

    def on_motion(self, window, touch):
        """Метод отслеживания перемещения мышки по рабочей области."""
        # если курсор находится в элепсе состояния
        if self.active_elp:
            # если курсор выходит за радиус элепса состояния + 10 рх
            if not geo.cross_cursor(self.active_elp.pos, touch, self.radius, dopusk=10):
                # скрытие коннекторов
                for connector in self.connectors_array: connector.hide_connectors()
                # очистка переменных
                self.active_elp = None
                self.show_connectors = None
            else:
                # если курсор находится на коннекторе
                if self.show_connectors.find_select_connector(touch):
                    Window.set_system_cursor("hand")
                else:
                    Window.set_system_cursor("arrow")
                self.active_connector = self.show_connectors.active_connector
                print(self.active_connector)
        else:
            for i, elp in enumerate(self.elps):
                # ищем пересечение курсора и элепса состояния               
                if geo.cross_cursor(elp.pos, touch, self.radius):
                    # если не существуют коннекторов для элепса состояния
                    try:
                        _ = self.connectors_array[i]
                    except:
                        connectors = Connectors(elp.pos, self.canvas)
                        self.connectors_array.append(connectors)
                    # показываемые коннекторы
                    self.show_connectors = self.connectors_array[i]
                    self.show_connectors.show_connectors()
                    # запоминаем выбранный элипс состояния         
                    self.active_elp = elp
                    break
            #   
            if not self.active_elp and self.bezier_line_array != []:
                for self.bezier_line in self.bezier_line_array:
                    if geo.cross_cursor(self.bezier_line.control_point, touch, 10, dopusk=5):
                        Window.set_system_cursor("hand")
                        self.active_bezier_line = True
                        print('yes')
                    else:
                        Window.set_system_cursor("arrow")
                        self.active_bezier_line = False
                        print('no')


    def on_touch_down(self, touch):
        #блокировка при соединении элипсов состояния
        if self.active_connector:
            self.start_draw_bezie = True            
            self.bizie_line = Bezier_line(self.canvas)
            self.bizie_line.start_create_bezier_line()
            # сохранения номер элипса состояния и коннектор
            touch.ud['start_elp_sondition_index'] = self.elps.index(self.active_elp)
            touch.ud['start_connector_index'] = self.active_connector
        # выделение состояния
        if self.active_elp and self.active_elp != self.check_elps:
            if self.check_elps: self.canvas.remove(self.check_elps_line)
            with self.canvas:
                Color(1,1,0)
                self.check_elps_line = Line(circle=(self.active_elp.pos[0]+self.radius, self.active_elp.pos[1]+self.radius, self.radius),width=3)
                self.check_elps = self.active_elp
        elif not self.active_elp:
            if self.check_elps: 
                self.canvas.remove(self.check_elps_line)
                self.check_elps = None
                '''
            if self.active_bezierline_conn:
                print('Conn active')
                '''
        
      
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        # при условии рисования линии Безье
        if self.start_draw_bezie:
            self.start_draw_bezie = False
            # если конец линии Безье соединен с коннектором
            if self.active_connector:
                print('ok')
                # сохранение номера элипса с которым производится соединение
                touch.ud['finish_elp_sondition_index'] = self.elps.index(self.active_elp)
                # остановка рисования лини Безье
                x,y = self.connectors_array[touch.ud['finish_elp_sondition_index']].get_position_connector(self.active_connector)
                self.bizie_line.stop_create_bzezier_line(x,y)
                #добавляем все элементы в список
                self.bezier_line_array.append(self.bizie_line)
                # список номеров элепсов, которые соединяет линия Безье
                conection =  [touch.ud['start_elp_sondition_index'],touch.ud['finish_elp_sondition_index']]
            # удаление, если конец линии Безье не соединен с коннектором
            else:
                print('no')
                self.bizie_line.remove()
                
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        # в случае если рисуется линия Безье
        if self.start_draw_bezie:
            # получение координат началалинии Безье  
            x, y = self.connectors_array[touch.ud['start_elp_sondition_index']].get_position_connector(touch.ud['start_connector_index'])
            # перерисовка линии Безье          
            self.bizie_line.drawing_bezier_line([x+5 ,y+5, touch.x, touch.y])
            '''
        elif self.bezierline_conn_move:
            # позиция выбранной точки линии бизье в списке
            index = self.bezierline_conn_array.index(self.active_bezierline_conn)
            x0, y0 ,x1, y1 = *self.active_bezierline_conn.pos, touch.x, touch.y
            # разница между курсором и точки линии безье 
            ox = x1-x0-5
            oy = y1-y0-5
            #получение линии безье, которая будет менятся
            bezierline = self.bezierline_array[index]
            # новое положение середины линии безье
            points = [bezierline.points[0],bezierline.points[1],bezierline.points[2]+2*ox,bezierline.points[3]+2*oy,bezierline.points[4],bezierline.points[5]]
            self.bezierline_array[index].points = points
            # новое положение точки линии безье
            new_point_bezierline_conn = [x1-5, y1-5]
            self.bezierline_conn_array[index].pos = new_point_bezierline_conn
            #изменение положения стрелки
            point_triangle = geo.get_triangle_bezie_line(points[2],points[3],points[4],points[5])
            self.triangle_array[index].points = point_triangle
            '''                    
        # перемещение элипса
        else:
            if self.active_elp:
                # позиция выбранного элипса состояния в списке
                index = self.elps.index(self.active_elp)
                # получаем координаты для пересчета движения       
                x0, y0 ,x1, y1 = *self.active_elp.pos, touch.x, touch.y
                # разница между курсором и центром элипса
                ox = x1-x0-self.radius
                oy = y1-y0-self.radius
                # новое положение состояния
                self.active_elp.pos = [touch.x-self.radius, touch.y-self.radius]
                # новое положение обводки
                points = self.check_elps_line.points[:]
                for i in range(len(points)):
                    if not i % 2:
                        points[i] += ox
                        points[i + 1] += oy
                self.check_elps_line.points = points
                # перерисовка и изменение позиции коннекторов
                self.connectors_array[index].change_connectors_position(ox, oy)
                # перемещение подписи
                self.labels[index].pos = (self.labels[index].pos[0]+ox, self.labels[index].pos[1]+oy)

        return super().on_touch_down(touch)

class LaplaceApp(App):
    def build(self):
        parent = Widget()
        self.painter = Condition()
        parent.add_widget(self.painter)
        parent.add_widget(Button(text = 'Добавить\n состояние', halign='center', on_press=self.add_condition, size =(100,50)))
        parent.add_widget(Button(text = 'Удалить\n состояние', halign='center', on_press=self.del_condition, pos  = (105,0), size =(100,50)))

        #self.matrix = Matrix()
        
        return parent

    def add_condition(self, instance):
        with self.painter.canvas:
            Color(1,1,1)
            self.painter.elps.append(Ellipse(pos=(200,200), size=(2*self.painter.radius,2*self.painter.radius),))
            self.painter.labels.append(Label(text=str(self.painter.count), font_size = 60, halign='left', pos=(200,200), color=(0,0,0)))
        #self.matrix.extension()
        #self.painter.connector_array.append(geo.connector_pos([200,200]))
        #self.painter.connected_conn.append([False, False, False, False])
        self.painter.count += 1

    def del_condition(self, instance):
        if self.painter.elps and self.painter.check_elps:
            #получаем инднкс выбранного состояния
            index_elp = self.painter.elps.index(self.painter.check_elps)
            #удаляем из спсиска
            self.painter.elps.pop(index_elp)
            self.painter.labels.pop(index_elp)
            #удаляем из канваса состаяние и выделитель
            self.painter.canvas.remove(self.painter.check_elps)
            self.painter.check_elps = None
            self.painter.canvas.remove(self.painter.check_elps_line)
            self.painter.count -= 1
            self.change_lable_index()
            #self.matrix.compression()
    
    def change_lable_index(self):
        index = 0
        for label in self.painter.labels:
            label.text = str(index)
            index += 1

if __name__ == '__main__':
    LaplaceApp().run()