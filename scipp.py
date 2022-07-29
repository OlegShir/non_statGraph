
import math

def angle_coefficient(x0, y0, x1, y1):
    '''Определения углового коэффициента отрезка.'''
    c = 0
    # если отрезок уходит во 2 или 3 четверть
    if x1 < x0:
        c = math.pi
    if x0 == x1:
        return 0
    return math.atan((y1-y0)/(x1-x0))+c



relative_center_x = 0
relative_center_y = 0

RADIUS_CONDITION = 50


touch_x  =150
touch_y = 150
# центр состояния
xc = relative_center_x + RADIUS_CONDITION
yc = relative_center_y + RADIUS_CONDITION
angel = angle_coefficient(xc, yc, touch_x, touch_y)

x1= (xc + RADIUS_CONDITION)*math.cos(angel)
y1= (yc + RADIUS_CONDITION)*math.sin(angel)


print(angel)