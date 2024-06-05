import numpy as np


def grad(x: np.ndarray) -> np.ndarray:
    x1, x2 = x[0], x[1]
    return np.array([10*(x1**3)-2*x1*(5*x2-1)-2, 5*x2-5*(x1**2)])

def normalize(vector: np.ndarray):
    return np.linalg.norm(vector)

def h_(i: int):
    return 0.000701 * i              # 166 iterations
    #return 0.000701 * i            # 166 iterations
    #return 0.03 * (i ** (1/2))     # zaden warunek stopu nie chce dawac dla tej metody rezultatow - algorytm gubi minimum
    #return 0.03 * (i ** (1/4))     # 117 iterations
    #return 0.05

def simple_gradient_method():
    i = 0
    N_max = 100000
    x_i = np.array([-0.5, 1])
    x_old = x_i
    E = 1e-3

    def stop_condition_1():             # dla podanego E i x_0, ten warunek stopu gubi minimum i go nie znajduje (znajduje dla E = 1e-2)
        return normalize(gradient) < E
    
    def stop_condition_2():
        #return normalize(x_i - x_old) < E and i != 1
        return normalize(h * d) < E and i != 1

    while i < N_max:
        gradient = grad(x_i)
        d = -gradient
        h = h_(i)
        x_old = x_i
        x_i = x_i + h * d
        i = i + 1
        if stop_condition_2():
            return i, x_i
    return None

def func(x):
    x1, x2 = x[0], x[1]
    return 2.5*(x1**2 - x2)**2 + (1-x1)**2


def main():
    result = simple_gradient_method()
    if result is None:
        print('Unable to optimize with given parameters')
    else:
        i, x_min = result
        print(f'Solution found after {i} iterations:\nminimal x: {x_min}\nfunction value: {func(x_min)}')


if __name__ == "__main__":
    main()
