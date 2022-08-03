from turtle import left
from sympy import symbols, integrate, oo
from sympy.stats import Normal, cdf, density
import math


class Solver():
    def __init__(self, storage) -> None:
        self.storage = storage

    def get_main(self):
        P = symbols(f'P:{len(self.storage)}')
        equations = []
        for i in range(len(self.storage)):
            left_part = 0
            for j in range(len(self.storage)):
                if self.storage[i][j]:
                    left_part +=  P[i]*self.storage[i][j]
            equations.append(left_part)
        return equations
            


    def filt_laplace(self, distribution_type, *arg):

        '''Метод возвращает гипердельтную аппроксимацию выбранной плотности распределения.
           Значеия distribution_type могут быть:
           - 'Exponential', lambda;
           - 'Gamma', k, lambda;
           - 'Normal', mu, sigma;
           - 'Uniform', a;
           - 'Rayleigh', sigma.
        '''
 
        if distribution_type == 'Exponential':
            # C1  = 0.854; C2 = 0.146; T1 = 0.293/lambda; T2 = 1.707/lambda
            C1 = 0.854
            C2 = 0.146
            T1 = 0.293/arg[0]
            T2 = 1.707/arg[1]
            
        if distribution_type == 'Gamma':
            # C1  = (1 + sqrt(k + 1))/2*sqrt(k + 1); C2 = (1 - sqrt(k + 1))/2*sqrt(k + 1);
            # T1 = (k + 1 - sqrt(k + 1))/lambda; T2 = (k + 1 + sqrt(k + 1))/lambda
            C1 = (1 + math.sqrt(arg[0] + 1))/2*math.sqrt(arg[0] + 1)
            C2 = (1 - math.sqrt(arg[0] + 1))/2*math.sqrt(arg[0] + 1)
            T1 = (arg[0] + 1 - math.sqrt(arg[0] + 1))/arg[1]
            T2 = (arg[0] + 1 + math.sqrt(arg[0] + 1))/arg[1]
            
        if distribution_type == 'Normal':
            # C1  = 0.5; C2 = 0.5; T1 = mu - sigma; T2 = mu + sigma
            C1 = 0.5
            C2 = 0.5
            T1 = arg[0] - arg[1]
            T2 = arg[0] + arg[1]
            
        if distribution_type == 'Uniform':
            # C1  = 0.5; C2 = 0.5;
            # T1 = 0.211*a; T2 = 0.789*a
            C1 = 0.5
            C2 = 0.5
            T1 = 0.211*arg[0]
            T2 = 0.789*arg[0]
            
        if distribution_type == 'Rayleigh':
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

def get_conditional_prob(first_law: list, second_law:list):
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
    p = symbols('b')
    storage =[                                                  
            [False, p, p, False],     
            [False, p, False, p],     
            [False, False, False, False],       
            [p, False, False, False]       
            ] 



    solver = Solver(storage)
    value = solver.get_main()
    print(value)