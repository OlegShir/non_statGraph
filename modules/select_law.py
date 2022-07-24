from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from settings import *
import re

class SuperButton(Button):
    def __init__(self, name_law, **kwarg):
        super(SuperButton, self).__init__(**kwarg)
        self.name_law = name_law

class SelectLaw(Widget):
    def __init__(self, parent, **kwargs):
        super(SelectLaw, self).__init__(**kwargs)
        self.position = POSITION_SELECT_LAW_BTN
        self.disabled = True
        self.key_law: str
        self.text_mainbutton = 'Выберите закон\nраспределения'
        self.label_image = []
        self.input_image = []
        self.dropdown = DropDown()
        self.dropdown.bind(on_select=self.on_select)
        self.parent = parent
        self.build()        

    def build(self):
        for key, value in LAW_FULL_NAME.items():
            btn = SuperButton(text=value, halign='center', size_hint_y=None, height=44, name_law=key)
            btn.bind(on_release=lambda btn: self.dropdown.select([btn.text, btn.name_law]))
            self.dropdown.add_widget(btn)
        self.mainbutton = Button(text= self.text_mainbutton, 
                                       halign='center',
                                       pos  = self.position, 
                                       size = SIZE_BTN,
                                       disabled = True)
        self.mainbutton.bind(on_release=self.dropdown.open)
        
        self.parent.add_widget(self.mainbutton)
        
    def on_select(self, instance, x) -> None:
        "Метод изменения названия кнопки при выборе"
        setattr(self.mainbutton, 'text', x[0])
        self.key_law = x[1]     
        self.paint_param(self.key_law)

    def paint_param(self, key: str, values: list=[]) -> None:
        "Метод отрисовки параметров закона распределения при его изменении"
        # очистка из канваса изображения Лайбла и Импута закона распределения
        self.remove()
        # для каждого закона отрисовывается ярлык и Импут в соответствии с его параметром
        # текстовое знчение для ярлыка берется из словаря
        param = LAW_PARAM.get(key)
        # парамерты в случе если для лиии Безье выбирался закон
        for count, text_param in enumerate(param):
            with self.parent.canvas:            
                self.label_image.append(Label(text=text_param,
                                        text_size = (90, None),
                                        font_size = FONT_SIZE_LAW_PARAM, 
                                        halign='left', 
                                        pos=(self.position[0]+10, self.position[1]-2*PADDING_VERTICAL-count*PADDING_VERTICAL), 
                                        color=COLOR_TEXT
                                        )
                )
            edit_text = '' if not values else values[count]
            print(edit_text)
            textinput: TextInput = FloatInput([self.position[0]+35, self.position[1]-PADDING_VERTICAL-count*PADDING_VERTICAL],
                                              text=edit_text)
            self.input_image.append(textinput)
            self.parent.add_widget(textinput)

    def get_law_param(self) -> list or bool:
        '''Метод передает данные о выбранном законе распределения.
           При этом если параметры закона не введены передает пустую строку'''
        # проверка, что закон выбран
        if self.key_law:
            # получаем ключ закона
            key = self.key_law
            param: list = []
            for _ in self.input_image:
                param.append(_.text)
            array = [key, param]
        else:
            array = False
        return array

    def show(self, array: list) -> None:
        '''Метод разблокировки кнопки выбора закона'''
        self.mainbutton.disabled = False
        # если для линии Безье уже вводились параметры
        if array:
            key, param = array
            self.mainbutton.text = LAW_FULL_NAME.get(key)
            self.paint_param(key, values=param)

        

    def hide(self):
        self.remove()
        self.mainbutton.text = self.text_mainbutton
        self.mainbutton.disabled = True
            
    def remove(self):
        "Метод очистки из канваса изображения Лайбла и Импута закона распределения"
        if self.label_image:
            for _number_input, _label in enumerate(self.label_image):
                self.parent.canvas.remove(_label.canvas)
                self.parent.remove_widget(self.input_image[_number_input])
            self.label_image = []
            self.input_image = []

class FloatInput(TextInput):
    def __init__(self, position: list, **kwargs):
        super().__init__(**kwargs)
        self.size_hint =  (.2, None)
        self.multiline = False
        self.x = position[0]
        self.y = position[1]
        self.height = FONT_SIZE_LAW_PARAM/0.7
        self.pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join(
                re.sub(pat, '', s)
                for s in substring.split('.', 1)
            )
        return super().insert_text(s, from_undo=from_undo)

