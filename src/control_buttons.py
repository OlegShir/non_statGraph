from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from src.condition import Condition
from src.painter import Painter
from src.solver import Solver
from kivy.core.window import Window
from settings import *
import re


class SuperButton(Button):
    '''Новый класс необходим для добавления нового свойства'''

    def __init__(self, key_law, **kwarg):
        super(SuperButton, self).__init__(**kwarg)
        self.key_law = key_law


class ControlButtons(Widget):
    def __init__(self, **kwargs):
        super(ControlButtons, self).__init__(**kwargs)
        # создание выпадающего списка
        self.dropdown: DropDown = DropDown()
        self.dropdown.bind(on_select=self.on_select_dropdown)
        # создание свойств кнопки выбора закона
        self.disabled_law_btn: bool = True
        self.key_law_btn: str = ''
        self.text_law_btn: str = BTN_TEXT.get('dropdown_btn')
        self.label_image_law_btn: list = []
        self.input_image_law_btn: list = []
        # отрисовка всех кнопок
        self.build()
        # отрисовка пейнтора с передачей ему связи с текущим класом для изменения свойств кнопок
        self.painter = Painter(self, size=Window.size, pos=[0, SIZE_BTN[1]])
        self.add_widget(self.painter)

    def build(self) -> None:
        '''Метод отрисовки всех кнопок'''
        self.add_condition_btn = Button(text=BTN_TEXT.get('add_btn'),
                                        halign='center',
                                        on_press=self.add_condition,
                                        size=SIZE_BTN
                                        )
        self.del_element_btn = Button(text=BTN_TEXT.get('del_btn'),
                                      halign='center',
                                      on_press=self.del_element,
                                      pos=(155, 0),
                                      size=SIZE_BTN,
                                      disabled=True
                                      )
        self.calculate_btn = Button(text=BTN_TEXT.get('calculate_btn'),
                                    halign='center',
                                    on_press=self.calculate,
                                    pos=(650, 0),
                                    size=SIZE_BTN
                                    )

        self.export_png_btn = Button(text=BTN_TEXT.get('export_btn'),
                                     halign='center',
                                     on_press=self.export,
                                     pos=(650, 70),
                                     size=SIZE_BTN
                                     )
        # создание списка кнопок для выпадающего списка
        for key, value in LAW_FULL_NAME.items():
            _btn = SuperButton(text=value, halign='center',
                               size_hint_y=None, height=44, key_law=key)
            _btn.bind(on_release=lambda btn: self.dropdown.select(
                [btn.text, btn.key_law]))
            self.dropdown.add_widget(_btn)
        # создание основной кнопи для выпадающего списка
        self.law_btn = Button(text=self.text_law_btn,
                              halign='center',
                              pos=(310, 0),
                              size=SIZE_BTN,
                              disabled=True)
        self.law_btn.bind(on_release=self.dropdown.open)
        # отрисовка
        self.add_widget(self.law_btn)
        self.add_widget(self.add_condition_btn)
        self.add_widget(self.del_element_btn)
        self.add_widget(self.calculate_btn)
        self.add_widget(self.export_png_btn)

    def add_condition(self, instance) -> None:
        '''Добавление состояний на пайнтер'''
        self.painter.conditions.append(
            Condition(self.painter.canvas, [200, 200], self.painter.count))
        self.painter.watcher.expand_storage()
        self.painter.count += 1

    def del_element(self, instance) -> None:
        if self.painter.check_condition:
            index = self.painter.check_condition.count
            # получение линий Безье соединенных с состояним из хранилища
            inner, outer = self.painter.watcher.reduce_storage(index)
            self.painter.inspector.killer_conditions(inner, outer, index)
            self.painter.check_condition = False
            self.painter.count -= 1
        if self.painter.selected_bezier_line:
            connected_conditions = self.painter.watcher.get_conditions_index(
                self.painter.selected_bezier_line)
            self.painter.inspector.killer_bezier_line(
                connected_conditions, self.painter.selected_bezier_line)
            # удаляем связь из хранилища
            self.painter.watcher.del_link_in_storage(
                self.painter.selected_bezier_line)
            # получаем индекс выбранной линии Безье в общем списке
            index = self.painter.bezier_line_array.index(
                self.painter.selected_bezier_line)
            # удаляем линию из списка, при этом эта последняя ссылка на линию и вызывается м. метод __del__
            self.painter.bezier_line_array.pop(index)
            self.painter.change_element()

    def calculate(self, instance) -> None:
        # проверка, что для всех линий Безье введены законы
        result = True
        for line in self.painter.bezier_line_array:
            result = result and line.is_full_law_param
        if not result:
            self.painter.message.show_message('Введены не все параметры законов распределения')
            return
        export_storage = self.painter.watcher.export_storage()
        solver = Solver(export_storage)
        solver.get_solution()
        #self.painter.message.show_message(solution)

    def export(self, instance) -> None:
        self.painter.export_to_png('graph.png')

    def on_select_dropdown(self, instance, x) -> None:
        '''Метод изменения названия кнопки при выборе'''
        setattr(self.law_btn, 'text', x[0])
        # сохранение для дальнейшей передачи
        self.key_law_btn = x[1]
        self.paint_law_param(self.key_law_btn)

    def paint_law_param(self, key: str, values: list = []) -> None:
        '''Метод отрисовки параметров закона распределения при его изменении'''
        # очистка из канваса изображения Лайбла и Импута закона распределения
        self.remove_law_btn()
        # для каждого закона отрисовывается ярлык и Импут в соответствии с его параметром
        # текстовое знчение для ярлыка берется из словаря
        param = LAW_PARAM.get(key)
        # парамерты в случе если для лиии Безье выбирался закон
        for count, text_param in enumerate(param):
            with self.painter.canvas:
                self.label_image_law_btn.append(Label(text=text_param,
                                                      text_size=(90, None),
                                                      font_size=FONT_SIZE_LAW_PARAM,
                                                      halign='left',
                                                      pos=(465,
                                                           -count*PADDING_VERTICAL),
                                                      color=COLOR_TEXT
                                                      )
                                                )
            edit_text = '' if not values else values[count]
            textinput: TextInput = FloatInput([500, 35-count*PADDING_VERTICAL],
                                              text=edit_text)
            self.input_image_law_btn.append(textinput)
            self.painter.add_widget(textinput)

    def get_law_param(self) -> list or bool:
        '''Метод передает данные о выбранном законе распределения.
           При этом если параметры закона не введены передает пустую строку'''
        # проверка, что закон выбран
        if self.key_law_btn:
            # получаем ключ закона
            key = self.key_law_btn
            param: list = []
            for _ in self.input_image_law_btn:
                param.append(_.text)
            array = [key, param]
        else:
            array = False
        return array

    def show_law_btn(self, array: list) -> None:
        '''Метод разблокировки кнопки выбора закона.'''
        self.law_btn.disabled = False
        # если для линии Безье уже вводились параметры
        if array:
            key, param = array
            self.law_btn.text = LAW_FULL_NAME.get(key)
            self.paint_law_param(key, values=param)

    def hide_law_btn(self) -> None:
        '''Метод возвращает свойства кнопки выбора закона распределения в исходное состояние.'''
        self.remove_law_btn()
        self.law_btn.text = self.text_law_btn
        self.law_btn.disabled = True

    def remove_law_btn(self) -> None:
        '''Метод очистки из канваса изображения Лайбла и Импута закона распределения.'''
        if self.label_image_law_btn:
            for _number_input, _label in enumerate(self.label_image_law_btn):
                self.painter.canvas.remove(_label.canvas)
                self.painter.remove_widget(
                    self.input_image_law_btn[_number_input])
            self.label_image_law_btn = []
            self.input_image_law_btn = []


class FloatInput(TextInput):
    def __init__(self, position: list, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.2, None)
        self.multiline = False
        self.x = position[0]
        self.y = position[1]
        self.height = FONT_SIZE_LAW_PARAM/0.7
        self.pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo: bool = False):
        '''Метод фильтрации вводимых значений'''
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join(
                re.sub(pat, '', s)
                for s in substring.split('.', 1)
            )
        return super().insert_text(s, from_undo=from_undo)
