from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from modules.condition import Condition
from modules.painter import Painter
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
        self.dropdown = DropDown()
        self.dropdown.bind(on_select=self.on_select_dropdown)
        # создание свойств кнопки выбора закона
        self.position_law_btn = POSITION_SELECT_LAW_BTN
        self.disabled_law_btn = True
        self.key_law_btn: str = ''
        self.text_law_btn = 'Выберите закон\nраспределения'
        self.label_image_law_btn = []
        self.input_image_law_btn = []
        # отрисовка всех кнопок
        self.build()
        # отрисовка пейнтора с передачей ему связи с текущим класом для изменения свойств кнопок
        self.painter = Painter(self)
        self.add_widget(self.painter)

    def build(self):
        '''Метод отрисовки всех кнопок'''
        self.add_condition_btn = Button(text='Добавить\nсостояние',
                                        halign='center',
                                        on_press=self.add_condition,
                                        size=SIZE_BTN
                                        )
        self.del_element_btn = Button(text='Удалить\nэлемент',
                                      halign='center',
                                      on_press=self.del_element,
                                      pos=(155, 0),
                                      size=SIZE_BTN,
                                      disabled=True
                                      )
        self.calculate_btn = Button(text='Провести\nрасчет',
                                    halign='center',
                                    on_press=self.calculate,
                                    pos=(310, 0),
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
                              pos=self.position_law_btn,
                              size=SIZE_BTN,
                              disabled=True)
        self.law_btn.bind(on_release=self.dropdown.open)
        # отрисовка
        self.add_widget(self.law_btn)
        self.add_widget(self.add_condition_btn)
        self.add_widget(self.del_element_btn)
        self.add_widget(self.calculate_btn)

    def add_condition(self, instance):
        '''Добавление состояний на пайнтер'''
        self.painter.conditions.append(
            Condition(self.painter.canvas, [200, 200], self.painter.count))
        self.painter.watcher.expand_storage()
        self.painter.count += 1

    def del_element(self, instance):
        if self.painter.check_condition:
            index = self.painter.check_condition.count
            inner, outer = self.painter.watcher.reduce_storage(index)
            self.painter.inspector.killer(inner, outer, index)
            self.painter.check_condition = False
            self.painter.count -= 1
        if self.painter.selected_bezier_line:
            self.painter.delete_bezie_line()



    def calculate(self, instance):
        print('calculate')

    def on_select_dropdown(self, instance, x) -> None:
        "Метод изменения названия кнопки при выборе"
        setattr(self.law_btn, 'text', x[0])
        # сохранение для дальнейшей передачи
        self.key_law_btn = x[1]
        self.paint_law_param(self.key_law_btn)

    def paint_law_param(self, key: str, values: list = []) -> None:
        "Метод отрисовки параметров закона распределения при его изменении"
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
                                                      pos=(self.position_law_btn[0]+10,
                                                           self.position_law_btn[1]-2*PADDING_VERTICAL-count*PADDING_VERTICAL),
                                                      color=COLOR_TEXT
                                                      )
                                                )
            edit_text = '' if not values else values[count]
            textinput: TextInput = FloatInput([self.position_law_btn[0]+35, self.position_law_btn[1]-PADDING_VERTICAL-count*PADDING_VERTICAL],
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
        '''Метод разблокировки кнопки выбора закона'''
        self.law_btn.disabled = False
        # если для линии Безье уже вводились параметры
        if array:
            key, param = array
            self.law_btn.text = LAW_FULL_NAME.get(key)
            self.paint_law_param(key, values=param)

    def hide_law_btn(self):
        self.remove_law_btn()
        self.law_btn.text = self.text_law_btn
        self.law_btn.disabled = True

    def remove_law_btn(self):
        "Метод очистки из канваса изображения Лайбла и Импута закона распределения"
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

    def insert_text(self, substring, from_undo=False):
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
