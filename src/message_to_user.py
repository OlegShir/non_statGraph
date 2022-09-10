from kivy.uix.label import Label
from settings import *


class MessageToUser():
    def __init__(self, canvas, width_windows, height_windows) -> None:
        self.canvas = canvas
        self.height_windows: int = height_windows
        self.width_windows: int = width_windows
        self.empty_text_message: str = ''
        self.label: Label = self.create_message()

    def create_message(self) -> Label:
        '''Создание сообщеня'''
        with self.canvas:
            label = Label(text=self.empty_text_message,
                          size_hint=(None, None),
                          font_size=FONT_SIZE_MESSAGE_TO_USER,
                          halign='left',
                          pos=self.get_pos_label(self.width_windows, self.height_windows),
                          color=COLOR_TEXT
                          )
        return label

    def show_message(self, text: str) -> None:
        '''Показ сообщения'''
        self.label.text = text
        self.label.size = self.label.texture_size

    def hide_message(self) -> None:
        '''Удаление сообщения'''
        if self.label.text != self.empty_text_message:
            self.label.text = self.empty_text_message

    def get_pos_label(self, width:int, height: int) -> list:
        '''Расчет положения сообщения'''
        position: list = [width/2, height - 50]
        return position

    def change_pos_label(self, new_width_windows: int, new_height_windows: int) -> None:
        '''Изменение положеия'''
        self.label.pos = self.get_pos_label(new_width_windows, new_height_windows)
