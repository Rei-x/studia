import math

H = 0.0007
H = 0.000701

E = 10e-3

def grad(x: list[float]):
    x1, x2 = x[0], x[1]
    return [10*(x1**3)-2*x1*(5*x2-1)-2, 5*x2-5*(x1**2)]

def norm(grad):
    normalized = 0
    for var in grad:
        try:
            normalized += var**2
        except:
            print(normalized, grad, sep='\n')
            raise ValueError
    return math.sqrt(normalized)

def h_(i):
    #return 0.03*math.sqrt(i)
    #return 0.0003*i
    return 0.0007 * i
    #return H*i

def d_(grad):
    return [-var for var in grad]

def is_good_solution(x):
    return norm(grad(x)) < E

# def is_good_solution(x, x_old):
#     return norm([x[i]-x_old[i] for i in range(len(x))]) < E


def metoda_zmiennokrokowa(x_i):
    x_old = x_i
    i = 0
    start = True
    while not is_good_solution(x_i) or start:
        start = False
        i += 1
        gradient = grad(x_i)
        d = d_(gradient)
        h = h_(i)
        x_old = x_i
        x_i = [x_i[i] + d_i*h for i, d_i in enumerate(d)]
    return i, x_i

def func(x):
    x1, x2 = x[0], x[1]
    return 2.5*(x1**2 - x2)**2 + (1-x1)**2

def main():
    x_0 = [-0.5, 1]
    i, x_solution = metoda_zmiennokrokowa(x_0)
    print(f'Solution: {x_solution}\nComputed in {i} steps')

    print(f'Initial function result for {x_0}:\t{func(x_0)}')
    print(f'Final function result for {x_solution}:\t{func(x_solution)}')

    x_test = [x_solution[0]-1, x_solution[1]+1]
    print(f'Test function result for {x_test}:\t{func(x_test)}')

    x_test = [x_solution[0]+0.4, x_solution[1]-0.7]
    print(f'Test function result for {x_test}:\t{func(x_test)}')


if __name__ == "__main__":
    main()
