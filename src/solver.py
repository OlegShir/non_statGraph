from sympy import symbols, integrate, oo, DiracDelta, laplace_transform, solve, pprint
from sympy.stats import Normal, cdf, density
from settings import DEBUG
import math


def _logger(func):
    '''Логгер отслеживания'''
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if DEBUG:
            zip = '-'
            print(result, '\n', f'{zip*25}')
        return result
    return wrapper


class Solver():
    def __init__(self, storage: list) -> None:
        self.storage: list = storage


    def get_solution(self):
        system_equations = self.get_system_equations()
        solution:str = self.solve_system_equations(system_equations)
        return solution


    @_logger
    def get_system_equations(self) -> list:
        '''Медот формирует систему уравнений баланса.
           Результат сохраняется списком

           Пример:
           -----------------------------------------
                        b1
                    PO---------->P1
                    \__b2    | b3
                        \_    |
                            _\| \|/
                            P2 _
                            / |\         
                            /_b4_\ 
           -----------------------------------------
            Входной список:[                        [
                           [False, b1, b2],         [False, ['exp', ['1']], ['exp', ['2']]],
                           [False, False, b3],      [False, False, ['exp', ['3']]],
                           [False, False, b4]       [False, False, ['exp', ['4']]]
                           ]                        ]
                                       __   
           Система уравнений баланса: |  P0*b1 + P0*b2 = 0              
                                     _|  P1*b3 = P0*b1 
                                      |  P2*b4 = P1*b3 + P0*b2
                                      |__P0 + P1 + P2 = 1

           Для дальнейшего расчета необходимо, что бы правая часть равнялась нулю

           Выходной список: [P0*b1 + P0*b2, P1*b3 - P0*b1 , P2*b4 - P0*b2 - P1*b3 , P0 + P1 + P2 - 1]

                                        '''
        iterator_count = len(self.storage)
        P = symbols(f'P:{iterator_count}')
        self.P = P
        equations = []
        # производится запись входящих и выходящих в состояние значений
        for i in range(iterator_count):
            # запись входящих значений
            left_part = 0
            for j in range(iterator_count):
                if self.storage[i][j]:
                    left_part += P[i]*self.filt_laplace(self.storage[i][j])
            # запись исходящих значений
            right_part = 0
            for k in range(iterator_count):
                if i == k:
                    continue
                if self.storage[k][i]:
                    right_part += P[k]*self.filt_laplace(self.storage[k][i])
            equations.append(left_part-right_part)
        # запись значеня полной вероятности
        sum_property = -1
        for i in range(iterator_count):
            sum_property += P[i]
        equations.append(sum_property)
        return equations

    def solve_system_equations(self, equation: list):
        P = symbols(f'P:{len(self.storage)}')
        t = symbols('t')
        solution: dict = solve(equation, P)
        text = ''
        for key, value in solution.items():
            text += f'{key}={value}\n' 
        return text

    def filt_laplace(self, law_param: list):
        '''Метод возвращает гипердельтную аппроксимацию выбранной плотности распределения.
           Значеия  могут быть:
           - ['exp', [lambda]];
           - ['gamma',[k, lambda]];
           - ['norm', [mu, sigma]];
           - ['unex', [a]];
           - ['rayl', [sigma]].
        '''
        distribution_type, param = law_param
        arg = list(map(int, param))

        if distribution_type == 'exp':
            # C1  = 0.854; C2 = 0.146; T1 = 0.293/lambda; T2 = 1.707/lambda
            C1 = 0.854
            C2 = 0.146
            T1 = 0.293/arg[0]
            T2 = 1.707/arg[1]

        if distribution_type == 'gamma':
            # C1  = (1 + sqrt(k + 1))/2*sqrt(k + 1); C2 = (1 - sqrt(k + 1))/2*sqrt(k + 1);
            # T1 = (k + 1 - sqrt(k + 1))/lambda; T2 = (k + 1 + sqrt(k + 1))/lambda
            C1 = (1 + math.sqrt(arg[0] + 1))/2*math.sqrt(arg[0] + 1)
            C2 = (1 - math.sqrt(arg[0] + 1))/2*math.sqrt(arg[0] + 1)
            T1 = (arg[0] + 1 - math.sqrt(arg[0] + 1))/arg[1]
            T2 = (arg[0] + 1 + math.sqrt(arg[0] + 1))/arg[1]

        if distribution_type == 'norm':
            # C1  = 0.5; C2 = 0.5; T1 = mu - sigma; T2 = mu + sigma
            C1 = 0.5
            C2 = 0.5
            T1 = arg[0] - arg[1]
            T2 = arg[0] + arg[1]

        if distribution_type == 'unex':
            # C1  = 0.5; C2 = 0.5;
            # T1 = 0.211*a; T2 = 0.789*a
            C1 = 0.5
            C2 = 0.5
            T1 = 0.211*arg[0]
            T2 = 0.789*arg[0]

        if distribution_type == 'rayl':
            # C1  = 0.35; C2 = 0.65; T1 = 0.773*sigma; T2 = 2.147*sigma
            C1 = 0.35
            C2 = 0.65
            T1 = 0.773*arg[0]
            T2 = 2.147*arg[0]

        t, s = symbols('t s')
        # построение апроксимационной функции a(t) = C1*dir(t-T1)+C2*dir(t-T2)
        f = C1 * DiracDelta(t - T1) + C2 * DiracDelta(t - T2)
        # получение изображения Лапласа
        f_laplace_s = laplace_transform(f, t, s, noconds=True)
        # получение фильтра Лапласа
        f_laplace_t = f_laplace_s.replace(s, 1/t)
        #value = f(1/t)
        return f_laplace_t


def get_conditional_prob(first_law: list, second_law: list):
    '''Возвращает условные вероятности переходов.
    Условные вероятности переходов alfa и beta определяют выбор дальнейшего
    движения случайного процесса из состояний графа
    '''
    x = symbols('x')
    # получение функции плотности вероятности для первого закона распределения
    if first_law[0] == 'Normal':
        first_law_function = Normal(x, first_law[1], first_law[2])

    pdf_first_law = density(first_law_function)(x)

    # получение функции плотности вероятности для второго закона распределения
    if second_law[0] == 'Normal':
        second_law_function = Normal(x, second_law[1], second_law[2])

    cdf_second_law = cdf(second_law_function)(x)

    # получение
    formuleCondProb = (1 - pdf_first_law)*cdf_second_law
    print(formuleCondProb)

    # получение значений условных вероятностей переходов alfa и beta
    alfa = integrate(formuleCondProb, (x, -oo, oo))
    beta = 1 - alfa

    return alfa, beta


if __name__ == '__main__':
    pass