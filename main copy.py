from telnetlib import SE
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


from modules.math_func import Geometric

from modules.condition import Condition
from modules.bezie_line import Bezier_line
from modules.watcher_link import Watcher_link
from modules.inspector import Inspector
from modules.select_law import SelectLaw
from settings import *


geo = Geometric()

class Painter(Widget):
      
    def __init__(self, **kwargs):
        super(Painter, self).__init__(**kwargs)
        
        self.count = 0

        self.conditions = []  
        self.mouse_on_condition = False
        self.check_condition = False

        self.active_connector = False
        self.mouse_on_connector = False

        self.bizie_line = False
        self.bezier_line_array =[]
        self.start_draw_bezie = False
        self.mouse_on_bezier_line = False
        self.active_bezier_line = False
        self.selected_bezier_line = False

        self.inspector = Inspector(self.conditions, self.bezier_line_array)
        # добавленние кнопки выборазакона распределения
        self.select_law = SelectLaw(self)
        # добавление наблюдателя
        self.watcher = Watcher_link()
        # отслеживание курсора мышки
        Window.bind(mouse_pos=self.on_motion)

    def on_motion(self, window, touch):
        """Метод отслеживания перемещения мышки по рабочей области."""
        # если курсор находится в элепсе состояния
        if self.mouse_on_condition:
            # если курсор выходит за радиус элепса состояния + 10 рх
            if not geo.cross_cursor(self.mouse_on_condition.condition_position, touch, RADIUS_CONDITION, dopusk=15):
                # скрытие коннекторов
                self.mouse_on_condition.hide_connectors()
                # очистка переменных
                self.mouse_on_condition = False
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
                        self.mouse_on_bezier_line = True
                        self.active_bezier_line = i
                        break
                    Window.set_system_cursor("arrow")
                    self.mouse_on_bezier_line = False
                    self.active_bezier_line = False
                
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
            self.change_element()
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
                self.check_condition = False
            # если курсор находится над линией Безье
            if self.mouse_on_bezier_line:
                # меняем цвет всех линий на дефолтный - потом можно оптимизировать
                for line in self.bezier_line_array: line.change_color(COLOR_DEFAULD)
                # определение выбранной линни Безье
                self.selected_bezier_line = self.bezier_line_array[self.active_bezier_line]
                # установка цвета выбранной линии
                self.selected_bezier_line.change_color(COLOR_SELECTED)
                # включение кнопки выбора закона с передачей значения параметров линии
                self.select_law.show(self.selected_bezier_line.law_param)
            if self.selected_bezier_line and not geo.cross_zone(touch) and not self.mouse_on_bezier_line:
                self.selected_bezier_line.set_value_label(self.select_law.get_law_param())
                self.change_element()


        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        # при условии рисования линии Безье
        if self.start_draw_bezie:
            self.start_draw_bezie = False
            # если конец линии Безье соединен с коннектором
            if self.mouse_on_connector:
                # сохранение номера элипса с которым производится соединение
                touch.ud['finish_condition_connecning'] = self.mouse_on_condition.count
                # остановка рисования лини Безье
                if self.watcher.add_link_in_storage(touch.ud['start_condition_connecning'],touch.ud['finish_condition_connecning'], self.bizie_line):
                    x,y = self.mouse_on_condition.get_position_connector(self.active_connector)
                    self.bizie_line.drawing_bezier_line([x+RADIUS_CONNECTOR,y+RADIUS_CONNECTOR], 'draw straight line')
                    self.bezier_line_array.append(self.bizie_line)
                    self.bizie_line = False
                else:
                    del self.bizie_line
            # удаление, если конец линии Безье не соединен с коннектором
            else:
                del self.bizie_line
                
        return super().on_touch_up(touch)

    def on_touch_move(self, touch):
        # в случае если рисуется линия Безье
        if self.start_draw_bezie:
            # получение координат началалинии Безье  
            x, y = self.conditions[touch.ud['start_condition_connecning']].get_position_connector(touch.ud['start_connector'])
            # перерисовка линии Безье          
            self.bizie_line.drawing_bezier_line([x+RADIUS_BEZIER_POINT,
                                                 y+RADIUS_BEZIER_POINT, 
                                                 touch.x, touch.y], 
                                                 'draw straight line'
                                                )
        elif self.mouse_on_bezier_line:
            # изменяем позицию текущей линии bezie
            self.bezier_line_array[self.active_bezier_line].drawing_bezier_line([touch.x, touch.y], 
                                                                                  'change middle point'
                                                                                  )
        # перемещение элипса
        else:
            if self.mouse_on_condition:
                self.mouse_on_condition.move_condition(touch)
                inner, outer = self.watcher.get_list_of_bezie(self.mouse_on_condition.count)
                self.inspector.move_bezie(inner, outer, [touch.dx, touch.dy])

        return super().on_touch_down(touch)

    def change_element(self) -> None:
        # снятие выделения с линий Безье
        for line in self.bezier_line_array: line.change_color(COLOR_DEFAULD)
        # сктытие кнопки
        self.select_law.hide()
        # отмена вбранной линии Безье
        self.selected_bezier_line = False
 
class LaplaceApp(App):
    def build(self):
        parent = Widget()

        self.painter = Painter()

        parent.add_widget(self.painter)

        parent.add_widget(Button(text = 'Добавить\n состояние', halign='center', on_press=self.add_condition, size = SIZE_BTN))
        parent.add_widget(Button(text = 'Удалить\n \элемент', halign='center', on_press=self.del_condition, pos  = (155,0), size = SIZE_BTN))
        parent.add_widget(Button(text = 'Провести\n расчет', halign='center', on_press=self.del_condition, pos  = (310,0), size = SIZE_BTN))
        return parent

    def add_condition(self, instance):
        '''Добавление состояний на пайнтер'''
        self.painter.conditions.append(Condition(self.painter.canvas, [200,200], self.painter.count))
        self.painter.watcher.expand_storage()
        self.painter.count += 1

    def del_condition(self, instance):
        if self.painter.check_condition:
            index = self.painter.check_condition.count
            inner, outer = self.painter.watcher.reduce_storage(index)
            self.painter.inspector.killer(inner, outer, index)
            self.painter.check_condition = False
            self.painter.count -= 1

if __name__ == '__main__':
    LaplaceApp().run()