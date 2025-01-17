from cmath import inf
from sympy import symbols, DiracDelta, laplace_transform
from sympy.solvers import solve
from sympy.plotting import plot
from settings import DEBUG
from scipy.stats import gamma, expon, norm, uniform, rayleigh
from scipy.integrate import quad
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


t = symbols('t')


class Solver():
    def __init__(self, storage: list) -> None:
        self.storage: list = storage
        self.conditional_storage = self.get_conditional_storage()

    def get_conditional_storage(self) -> list:
        # создаем клон хранилища для работы с условным велоятносятями
        conditional_storage = [e.copy() for e in self.storage]

        for i in conditional_storage:
            # определение количество выходов из состояния (количество не пустых значений)
            find = [x for x in i if isinstance(x, list)]
            # если в строке более одного выхода из состояния
            if len(find) > 1:
                # расчет условных вероятностей для строки
                new_val: list = self.get_conditional_prob(find)
                ind: int = 0
                # замена значений в списке на расчитанные
                for z in range(len(i)):
                    if i[z]:
                        i[z] = round(new_val[ind], 3)
                        ind += 1
                    else:
                        i[z] = 1
            # ели выход один -> условной вероятности нет -> замена значения на False
            else:
                for z in range(len(i)):
                    i[z] = 1

        return conditional_storage

    def get_solution(self):
        system_equations = self.get_system_equations()
        solution: dict = self.solve_system_equations(system_equations)
        text: str = ''
        for key, value in solution.items():
            text += f'{key}={value}\n'

        self.plot_solution(solution)

    def plot_solution(self, solution: dict):

        plotting = plot(show=False, legend=True, xlabel='t', ylabel='P(t)')
        for key, value in solution.items():
            label_str = f'{str(key)}(t)'
            plotting.extend(plot(value, (t, 0.1, 100), legend=True,
                            show=False, label=label_str, ylim=(0, 1)))

        plotting.show()

    @_logger
    def solve_system_equations(self, equation: list):
        P = symbols(f'P:{len(self.storage)}')
        solution = solve(equation, P)

        if type(solution) == dict:
            return solution

        print('Ошибка при решении системы уравнений')

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
        equations: list = []
        print(self.conditional_storage)
        # производится запись входящих и выходящих в состояние значений
        for i in range(iterator_count):
            # запись входящих значений
            left_part = 0
            for j in range(iterator_count):
                if self.storage[i][j]:
                    left_part += self.conditional_storage[i][j] * \
                        P[i]*self.filt_laplace(self.storage[i][j])
            # запись исходящих значений
            right_part = 0
            for k in range(iterator_count):
                if i == k:
                    continue
                if self.storage[k][i]:
                    right_part += self.conditional_storage[k][i] * \
                        P[k]*self.filt_laplace(self.storage[k][i])
            equations.append(left_part-right_part)
        # запись значеня полной вероятности
        sum_property = -1
        for i in range(iterator_count):
            sum_property += P[i]
        equations.append(sum_property)
        return equations

    @_logger
    def filt_laplace(self, law_param: list):
        '''Метод возвращает гипердельтную аппроксимацию выбранной плотности распределения.
           Значеия  могут быть:
           - ['expon', [lambda]];
           - ['gamma',[k, lambda]];
           - ['norm', [mu, sigma]];
           - ['uniform', [a]];
           - ['rayleigh', [sigma]].
        '''
        distribution_type, param = law_param
        arg: float = list(map(float, param))

        if distribution_type == 'expon':
            # C1  = 0.854; C2 = 0.146; T1 = 0.293/lambda; T2 = 1.707/lambda
            C1 = 0.854
            C2 = 0.146
            T1 = 0.293/arg[0]
            T2 = 1.707/arg[0]

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

        if distribution_type == 'uniform':
            # C1  = 0.5; C2 = 0.5;
            # T1 = 0.211*a; T2 = 0.789*a
            C1 = 0.5
            C2 = 0.5
            T1 = 0.211*arg[0]
            T2 = 0.789*arg[0]

        if distribution_type == 'rayleigh':
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

    def get_conditional_prob(self, array_law: list):
        '''Возвращает условные вероятности переходов.
        Условные вероятности переходов alfa и beta определяют выбор дальнейшего
        движения случайного процесса из состояний графа
        '''
        # словарь методов
        law_dict: dict = {'gamma': gamma, 'expon': expon,
                          'norm': norm, 'uniform': uniform, 'rayleigh': rayleigh}
        # количество поданных законов
        count_laws: int = len(array_law)
        # список для расчитанных вероятностей перехода
        probarty_array: list = []
        #
        for _ in range(count_laws-1):

            def formule_to_integrate(x):
                result = 1
                # построение формулы
                for j in range(count_laws):
                    type_law, param_law = array_law[j]
                    # преобразование типа данных параметров зокона из строк в число
                    param_law = list(map(float, param_law))
                    # для первого в списке закона берется функция распределения
                    if j == 0:
                        result = result * \
                            law_dict.get(type_law, None).pdf(x, *param_law)
                        continue
                    result = result * \
                        (1-law_dict.get(type_law, None).cdf(x, *param_law))
                    # print(result)
                    return result
            alfa, err = quad(formule_to_integrate, -inf, inf)
            probarty_array.append(alfa)
            # сдвиг списка [0,1,2] -> [1,2,0]
            array_law = array_law[1:]+array_law[:1]

        beta = 1 - sum(probarty_array)
        probarty_array.append(beta)

        return probarty_array


if __name__ == '__main__':
    pass
