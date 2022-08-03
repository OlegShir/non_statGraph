'''Класс отвечает за перемещение и удаление объектов'''
class Inspector():
    def __init__(self, conditions:list, bezier_line_array: list) -> None:
        self.conditions = conditions
        self.bezier_line_array = bezier_line_array

    def move_bezie(self, inner_list_of_bezie, outer_list_of_bezie, touch):
        for _ in inner_list_of_bezie:
            index = self.bezier_line_array.index(_)
            self.bezier_line_array[index].drawing_bezier_line(touch, 'change start point')
        for _ in outer_list_of_bezie:
            index = self.bezier_line_array.index(_)
            self.bezier_line_array[index].drawing_bezier_line(touch, 'change finish point')
    
    def killer_conditions(self, inner_list_of_bezie, outer_list_of_bezie, count):
        union_array = inner_list_of_bezie + outer_list_of_bezie
        for _ in union_array:
            try:
                index = self.bezier_line_array.index(_)
                self.bezier_line_array.pop(index)
            except: pass
            for condition in self.conditions:
                condition.remove_bezie_line(_)
        # очистка в состояниях подключенных линий Безье
        self.conditions.pop(count)
        self.change_lable()

    def killer_bezier_line(self, array: list, link):
        for i in array:
            self.conditions[i].remove_bezie_line(link)


    def change_lable(self):
        count = 0
        if self.conditions:
            for condition in self.conditions:
                condition.change_lable_count(count)
                count += 1


    
