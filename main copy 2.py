from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Ellipse, Color, Bezier, Line, Triangle

from math_func import Geometric, Matrix

from modules.condition import Condition
from  modules.bezie_line import Bezier_line
from settings import *

geo = Geometric()


class Painter(Widget):
      
    def __init__(self, **kwargs):
        super(Painter, self).__init__(**kwargs)
        
        self.count = 0

        self.conditions = []  
        self.mouse_on_condition = None
        self.check_condition = None

        self.active_connector = False
        self.mouse_on_connector = False

        self.bizie_line = None
        self.bezier_line_array =[]
        self.start_draw_bezie = False
        self.active_bezier_line = False
        self.selected_bezier_line = None

        # отслеживание курсора мышки
        Window.bind(mouse_pos=self.on_motion)

    def on_motion(self, window, touch):
        """Метод отслеживания перемещения мышки по рабочей области."""
        # если курсор находится в элепсе состояния
        if self.mouse_on_condition:
            # если курсор выходит за радиус элепса состояния + 10 рх
            if not geo.cross_cursor(self.mouse_on_condition.condition_position, touch, RADIUS_CONDITION, dopusk=10):
                # скрытие коннекторов
                self.mouse_on_condition.hide_connectors()
                # очистка переменных
                self.mouse_on_condition = None
            else:
                # если курсор находится на коннекторе
                if self.mouse_on_condition.find_select_connector(touch):
                    Window.set_system_cursor("hand")
                    self.mouse_on_connector = True
                else:
                    Window.set_system_cursor("arrow")
                    self.mouse_on_connector = False
                self.active_connector = self.mouse_on_condition.active_connector
        else:
            for condition in self.conditions:
                # ищем пересечение курсора и элепса состояния               
                if geo.cross_cursor(condition.condition_position, touch, RADIUS_CONDITION):
                    # показываемые коннекторы
                    condition.show_connectors()
                    # запоминаем выбранный элипс состояния         
                    self.mouse_on_condition = condition
                    break
            #  если курсор находится вне элипса состояния и существую линии Безье
            if len(self.bezier_line_array) > 0:
                # производится проверка, на то что курсор находится на точке изменения линии Безье
                for i, line in enumerate(self.bezier_line_array):
                    if geo.cross_cursor(line.points_control, touch, 10, dopusk=5):
                        Window.set_system_cursor("hand")
                        self.active_bezier_line = True
                        self.selected_bezier_line = i
                        break
                    Window.set_system_cursor("arrow")
                    self.active_bezier_line = False
                    self.selected_bezier_line = None
                
    def on_touch_down(self, touch):
        # блокировка при соединении состояний
        if self.mouse_on_connector:
            self.start_draw_bezie = True            
            self.bizie_line = Bezier_line(self.canvas)
            self.bizie_line.start_create_bezier_line()
            # сохранения номер состояния и коннектор
            touch.ud['start_condition_connecning'] = self.mouse_on_condition.count
            touch.ud['start_connector'] = self.mouse_on_condition.active_connector

        # выделение состояния
        if self.mouse_on_condition and self.mouse_on_condition != self.check_condition:
            # если уже выбрано другое состаяние -> обводка с него убирается
            if self.check_condition: self.check_condition.hide_lighter()
            # создается обводка для нового состояния
            self.mouse_on_condition.show_lighter()
            # сохраняется выбранное состояние
            self.check_condition = self.mouse_on_condition
        # есл нажатие просходит вне состояния
        elif not self.mouse_on_condition:
            if self.check_condition: 
                self.check_condition.hide_lighter()
                self.check_condition = None
            if self.active_bezier_line:
                # меняем цвет всех линий на дефолтный - потом можно оптимизировать
                for line in self.bezier_line_array: line.change_color(COLOR_DEFAULD)
                self.bezier_line_array[self.selected_bezier_line].change_color(COLOR_SELECTED)

        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        # при условии рисования линии Безье
        if self.start_draw_bezie:
            self.start_draw_bezie = False
            # если конец линии Безье соединен с коннектором
            if self.mouse_on_connector:
                # сохранение номера элипса с которым производится соединение
                #touch.ud['finish_elp_sondition_index'] = self.elps.index(self.active_elp)
                # остановка рисования лини Безье
                x,y = self.mouse_on_condition.get_position_connector(self.active_connector)
                self.bizie_line.end_create_bzezier_line(x,y)
                #добавляем все элементы в список
                self.bezier_line_array.append(self.bizie_line)
            # удаление, если конец линии Безье не соединен с коннектором
            else:
                self.bizie_line.remove()
                
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        # в случае если рисуется линия Безье
        if self.start_draw_bezie:
            # получение координат началалинии Безье  
            x, y = self.conditions[touch.ud['start_condition_connecning']].get_position_connector(touch.ud['start_connector'])
            # перерисовка линии Безье          
            self.bizie_line.drawing_bezier_line([x+5 ,y+5, touch.x, touch.y])
        elif self.active_bezier_line:
            # изменяем позицию текущей линии bezie
            self.bezier_line_array[self.selected_bezier_line].change_third_point(touch.x, touch.y)
        # перемещение элипса
        else:
            if self.mouse_on_condition:
                self.mouse_on_condition.move_condition(touch)

        return super().on_touch_down(touch)

class LaplaceApp(App):
    def build(self):
        parent = Widget()
        self.painter = Painter()
        parent.add_widget(self.painter)
        parent.add_widget(Button(text = 'Добавить\n состояние', halign='center', on_press=self.add_condition, size =(100,50)))
        parent.add_widget(Button(text = 'Удалить\n состояние', halign='center', on_press=self.del_condition, pos  = (105,0), size =(100,50)))

        return parent

    def add_condition(self, instance):
        '''Добавление состояний на пайнтер'''
        self.painter.conditions.append(Condition(self.painter.canvas, [200,200], self.painter.count))
        self.painter.count += 1

    def del_condition(self, instance):
        if self.painter.check_condition:
            self.painter.conditions.pop(self.painter.check_condition.count)
            self.painter.check_condition = None
            self.change_lable()
    
    def change_lable(self):
        self.painter.count -= 1
        count = 0
        if self.painter.conditions:
            for condition in self.painter.conditions:
                condition.change_lable_count(count)
                count += 1

if __name__ == '__main__':
    LaplaceApp().run()