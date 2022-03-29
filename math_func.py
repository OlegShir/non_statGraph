import math
import numpy as np

class Geometric:
    def __init__(self) -> None:
        pass

    def cross_cursor(self, witget_position:tuple, touch_position:tuple, radius:int, dopusk:int = 0)-> bool:
        '''Определяет пересечение курсорва мыши с виджетом (элипсом).
        
        Перевый аргумент позиция виджета, второй позиция курсора, третий - радиус элипса,
        четвертый является возможным допуском между курсором и элипсом  '''
        x0, y0 = witget_position
        x1, y1 = touch_position
        if math.sqrt((x1-x0-radius)**2+(y1-y0-radius)**2) <= radius + dopusk:
            return True
        else:
            return False
      

    def connector_pos(self, ellips_pos):
        '''
        Формрование центров координат коннекторов
        '''
        pos_x, pos_y = ellips_pos
        conn_1 = (pos_x-5, pos_y+45)
        conn_2 = (pos_x+45, pos_y-5)
        conn_3 = (pos_x+95, pos_y+45)
        conn_4 = (pos_x+45, pos_y+95)

        return [conn_1, conn_2, conn_3, conn_4]

class Matrix:

    def __init__(self) -> None:
        self.matrix = np.array([0])

    def extension(self, axis = None):
        if not axis:
            shape = self.matrix.shape
            
            try:
                shape_row = shape[1]
            except:
                shape_row = 1
            shape_column = shape[0]

            new_row = np.array(np.zeros(shape_row, dtype=int))
            new_column = np.array(np.zeros((shape_column+1, 1), dtype=int))

            # добавление строки
            self.matrix = np.vstack([self.matrix, new_row])
            # добавление столбца
            self.matrix = np.hstack((self.matrix, new_column))
            
            print(self.matrix)
    
    def compression(self, row_column):
        self.matrix = np.delete(self.matrix, row_column, 0)
        self.matrix = np.delete(self.matrix, row_column, 1)

        print(self.matrix)



if __name__ == "__main__":
    g = Matrix()
    g.extension()
    g.extension()
    g.extension()

    g.compression(2)

    g.matrix[1,1]='None'
    print(g.matrix)
