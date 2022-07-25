from kivy.core.window import Window
from kivy.uix.widget import Widget
from requests import delete
from modules.bezie_line import Bezier_line
from modules.condition import Condition
from modules.watcher_link import Watcher_link
from modules.inspector import Inspector
from settings import *
import math


class Painter(Widget):

    def __init__(self, control_btn, **kwargs):
        super(Painter, self).__init__(**kwargs)
        # счетчик количества состояний
        self.control_btn = control_btn
        self.count = 0

        self.conditions = []
        self.mouse_on_condition: bool or Condition = False
        self.check_condition: bool or Condition = False

        self.active_connector = False
        self.mouse_on_connector = False

        self.bizie_line = False
        self.bezier_line_array = []
        self.start_draw_bezie = False
        self.mouse_on_bezier_line = False
        self.active_bezier_line = False
        self.selected_bezier_line = False

        self.start_change_bezie = False

        self.inspector = Inspector(self.conditions, self.bezier_line_array)
        # добавление наблюдателя
        self.watcher = Watcher_link()
        # отслеживание курсора мышки
        Window.bind(mouse_pos=self.on_motion)

    def on_motion(self, window, touch):
        """Метод отслеживания перемещения мышки по рабочей области."""
        # если курсор находится в элепсе состояния
        if self.mouse_on_condition:
            # если курсор выходит за радиус элепса состояния + 10 рх
            if not self.cross_cursor(self.mouse_on_condition.condition_position, touch, RADIUS_CONDITION, dopusk=15):
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
                if self.cross_cursor(condition.condition_position, touch, RADIUS_CONDITION):
                    # показываемые коннекторы
                    condition.show_connectors()
                    # запоминаем выбранный элипс состояния
                    self.mouse_on_condition = condition
                    break
            #  если курсор находится вне элипса состояния и существую линии Безье
            if len(self.bezier_line_array) > 0:
                # производится проверка, на то что курсор находится на точке изменения линии Безье
                for i, line in enumerate(self.bezier_line_array):
                    if self.cross_cursor(line.points_control, touch, 10, dopusk=5):
                        Window.set_system_cursor("hand")
                        self.mouse_on_bezier_line = True
                        self.active_bezier_line = i
                        break
                    Window.set_system_cursor("arrow")
                    self.mouse_on_bezier_line = False
                    self.active_bezier_line = False

    def on_touch_down(self, touch):
        if touch.y > 60:
            # блокировка при соединении состояний
            if self.mouse_on_connector:
                # распаковка данных о коннекторе
                is_free, direction, change_line_bezie = self.mouse_on_condition.is_connector_free(
                    self.mouse_on_condition.active_connector)
                if is_free:
                    # сохранения номер состояния и коннектор
                    touch.ud['start_condition'] = self.mouse_on_condition.count
                    touch.ud['start_connector'] = self.mouse_on_condition.active_connector
                    # начало отрисовки линии Безье
                    self.start_draw_bezie = True
                    self.bizie_line = Bezier_line(self.canvas)
                    self.bizie_line.start_create_bezier_line()
                else:
                    # сохраняем данные об изменяемой линии Безье
                    self.start_change_bezie = change_line_bezie
                    touch.ud['from_condition'] = self.mouse_on_condition
                    touch.ud['from_connector'] = self.mouse_on_condition.active_connector
                    touch.ud['directon_change_line'] = direction
                    self.start_change_bezie.save_props()
                return
            # выделение состояния
            if self.mouse_on_condition and self.mouse_on_condition != self.check_condition:
                self.change_element()
                # если уже выбрано другое состаяние -> обводка с него убирается
                if self.check_condition:
                    self.check_condition.hide_lighter()
                # создается обводка для нового состояния
                self.mouse_on_condition.show_lighter()
                # показываем кнопку удаления
                self.control_btn.del_element_btn.disabled = False
                # сохраняется выбранное состояние
                self.check_condition = self.mouse_on_condition
                return
            # есл нажатие просходит вне состояния
            if not self.mouse_on_condition:
                if self.check_condition:
                    self.check_condition.hide_lighter()
                    self.check_condition = False
                    # скрываем кнопку удаления
                    self.control_btn.del_element_btn.disabled = True
                    return
                # если курсор находится над линией Безье
                if self.mouse_on_bezier_line:
                    # меняем цвет всех линий на дефолтный - потом можно оптимизировать
                    for line in self.bezier_line_array:
                        line.change_color(COLOR_DEFAULD)
                    # определение выбранной линни Безье
                    self.selected_bezier_line = self.bezier_line_array[self.active_bezier_line]
                    # установка цвета выбранной линии
                    self.selected_bezier_line.change_color(COLOR_SELECTED)
                    # показываем кнопку удаления
                    self.control_btn.del_element_btn.disabled = False
                    # включение кнопки выбора закона с передачей значения параметров линии
                    self.control_btn.show_law_btn(
                        self.selected_bezier_line.law_param)
                    return
                if self.selected_bezier_line and not self.cross_zone(touch) and not self.mouse_on_bezier_line:
                    self.selected_bezier_line.set_value_label(
                        self.control_btn.get_law_param())
                    self.change_element()
                    return

        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        # при условии рисования линии Безье
        if self.start_draw_bezie:
            self.start_draw_bezie = False
            # если конец линии Безье соединен с коннектором
            if self.mouse_on_connector:
                # сохранение номера элипса  и коннектора с которым производится соединение
                touch.ud['finish_condition'] = self.mouse_on_condition.count
                touch.ud['finish_connector'] = self.mouse_on_condition.active_connector
                # остановка рисования лини Безье
                if self.watcher.add_link_in_storage(touch.ud['start_condition'],
                                                    touch.ud['finish_condition'],
                                                    self.bizie_line):
                    x, y = self.mouse_on_condition.get_position_connector(
                        self.active_connector)
                    self.bizie_line.drawing_bezier_line(
                        [x+RADIUS_CONNECTOR, y+RADIUS_CONNECTOR], 'draw straight line')
                    self.bezier_line_array.append(self.bizie_line)
                    # запись в состояния входящих и выходящих линий безье
                    self.conditions[touch.ud['start_condition']].add_connector_link(touch.ud['start_connector'],
                                                                                    'out',
                                                                                    self.bizie_line)
                    self.conditions[touch.ud['finish_condition']].add_connector_link(touch.ud['finish_connector'],
                                                                                     'in',
                                                                                     self.bizie_line)
        # удаление, если конец линии Безье не соединен с коннектором
        self.bizie_line = False
        # изменение нарисованной линии Безье
        if self.start_change_bezie:
            if self.mouse_on_connector:
                # получение координат активного коннектора
                x, y = self.mouse_on_condition.get_position_connector(
                    self.active_connector)
                # изменение данных в коннекторах и состояниях
                from_condition = touch.ud['from_condition']
                direction = touch.ud['directon_change_line']
                # освобождаем коннектор в прошлом состоянии
                from_condition.remove_connector_link(touch.ud['from_connector'],
                                                     direction)
                # добавляем в новое состояние
                self.mouse_on_condition.add_connector_link(self.mouse_on_condition.active_connector,
                                                           direction,
                                                           self.start_change_bezie)
                # корректировка конечных точек линии относительно коннекторов
                self.start_change_bezie.drawing_bezier_line([x, y], direction)
                # уведомлие wathcher о изменении связи
                if from_condition != self.mouse_on_condition:
                    self.watcher.change_element_in_storage(
                        self.mouse_on_condition.count, self.start_change_bezie, direction)

            else:
                self.start_change_bezie.load_props()
            self.start_change_bezie = False
            # сделать очистку переменных

        return super().on_touch_up(touch)

    def on_touch_move(self, touch) -> None:
        if self.start_change_bezie:
            if touch.ud['directon_change_line'] == 'in':
                self.start_change_bezie.drawing_bezier_line(
                    [touch.dx, touch.dy], 'change finish point')
                return
            self.start_change_bezie.drawing_bezier_line(
                [touch.dx, touch.dy], 'change start point')
            return
        # в случае если рисуется линия Безье
        if self.start_draw_bezie:
            # получение координат началалинии Безье
            x, y = self.conditions[touch.ud['start_condition']].get_position_connector(
                touch.ud['start_connector'])
            # перерисовка линии Безье
            self.bizie_line.drawing_bezier_line([x+RADIUS_BEZIER_POINT,
                                                 y+RADIUS_BEZIER_POINT,
                                                 touch.x, touch.y],
                                                'draw straight line'
                                                )
            return

        if self.mouse_on_bezier_line:
            # изменяем позицию текущей линии bezie
            self.bezier_line_array[self.active_bezier_line].drawing_bezier_line([touch.x, touch.y],
                                                                                'change middle point'
                                                                                )
            return
        # перемещение элипса
        if self.mouse_on_condition:
            self.mouse_on_condition.move_condition(touch)
            inner, outer = self.watcher.get_list_of_bezie(
                self.mouse_on_condition.count)
            self.inspector.move_bezie(inner, outer, [touch.dx, touch.dy])
            return

        return super().on_touch_down(touch)

    def change_element(self) -> None:
        # снятие выделения с линий Безье
        for line in self.bezier_line_array:
            line.change_color(COLOR_DEFAULD)
        # сктытие кнопки
        self.control_btn.hide_law_btn()
        # отмена вбранной линии Безье
        self.selected_bezier_line = False

    def delete_bezie_line(self):
        # удаляем связь из хранилища
        self.watcher.del_link_in_storage(self.selected_bezier_line)
        # получаем индекс выбранной линии Безье в общем списке
        index = self.bezier_line_array.index(self.selected_bezier_line)
        # удаляем линию из списка, при этом эта последняя ссылка на линию и вызывается м. метод __del__
        self.bezier_line_array.pop(index)
        self.change_element()

    def cross_cursor(self, witget_position: tuple, touch_position: tuple, radius: int, dopusk: int = 0) -> bool:
        '''Определяет пересечение курсорва мыши с виджетом (элипсом).

        Перевый аргумент позиция виджета, второй позиция курсора, третий - радиус элипса,
        четвертый является возможным допуском между курсором и элипсом  '''
        x0, y0 = witget_position
        x1, y1 = touch_position
        if math.sqrt((x1-x0-radius)**2+(y1-y0-radius)**2) <= radius + dopusk:
            return True
        else:
            return False

    def cross_zone(self, touch_position: tuple) -> bool:
        '''Определяет пересечение курсорва мыши с зоной выбора закона.'''
        # распаковка начальных координат кнопки
        x0 = POSITION_SELECT_LAW_BTN[0]
        y1 = POSITION_SELECT_LAW_BTN[1]+SIZE_BTN[0]
        # получение начальных координат кнопки
        x1 = x0 + SIZE_BTN[0]
        y0 = y1 - SIZE_BTN[0] - 3*PADDING_VERTICAL
        # распаковка координат курсора
        x = touch_position.x
        y = touch_position.y
        # проверка условия
        if x >= x0 and x <= x1 and y >= y0 and y <= y1:
            return True
        else:
            return False
