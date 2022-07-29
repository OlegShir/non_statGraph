
COLOR_DEFAULD = [1,1,1]
COLOR_SELECTED = [1,1,0]
COLOR_TEXT_CONDITION = [0,0,0]
COLOR_TEXT = [1,1,1]
COLOR_CONNECTOR = [1,0,0]


SIMPLE_CONNECT = True

WIDTH_LIGHTER = 3
FONT_SIZE_LABEL_CONDITION = 60
FONT_SIZE_LAW_PARAM = 18
FONT_SIZE_LABEL_BEZIE = 18

SIZE_ARROW = 10
SIZE_BTN = (150 ,60)
PADDING_VERTICAL = 30
PADDING_HORIZONTAL = 10

RADIUS_CONDITION = 50
RADIUS_CONNECTOR = 5
RADIUS_BEZIER_POINT = 5

LAW_SYMBOLS: dict = {'exp': 'Exp(\u03BB)',
                     'gamma': '\u0393(\u03BA, \u03B8)',
                     'norm': 'N(\u03BC, \u03C3)',
                     'unex': 'U(a)',
                     'rayl': 'Rayl(\u03C3)'}

LAW_FULL_NAME: dict = {'exp': 'Экспоненциальное\nраспределение',
                       'gamma': 'Гамма\nраспределение',
                       'norm': 'Нормальное\nраспределение',
                       'unex': 'Равномерное\nраспределение',
                       'rayl': 'Распределение\nРэлея'}

LAW_PARAM: dict = {'exp': ['\u03BB :'],
                   'gamma': ['\u03BA :', '\u03BB :'],
                   'norm': ['\u03BC :', '\u03C3 :'],
                   'unex': ['a :'],
                   'rayl': ['\u03C3 :']}
