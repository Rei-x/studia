import numpy as np
from visualise import visualise_method

class SimpleGradientMethod:

    def __init__(self, f, grad, N_max, x_0, E, h_) -> None:
        self.f = f
        self.grad = grad
        self.N_max = N_max
        self.x_0 = x_0
        self.E = E
        self.h_ = h_

        self.x_min = x_0
        self.iterations = 0
        self.algorithm_steps = [x_0]

    def normalize(self, vector: np.ndarray):
        return np.linalg.norm(vector)

    def start_algorithm(self):
        i = 1 # zaczynam od i=1 (zeby nie spowodowac: h(i)=0)
        x_i = self.x_0

        def stop_condition_1():             # dla podanego E i x_0, ten warunek stopu gubi minimum i go nie znajduje (znajduje dla E = 1e-2)
            return self.normalize(gradient) < self.E
    
        def stop_condition_2():
            #return normalize(x_i - x_old) < E and i != 1
            return self.normalize(h * d) < self.E and i != 1
        
        while i < self.N_max:
            gradient = self.grad(x_i)
            d = -gradient
            h = h_(i)
            #x_old = x_i
            x_i = x_i + h * d
            self.algorithm_steps.append(x_i)
            i = i + 1
            if stop_condition_2():
                self.x_min = x_i
                self.iterations = i 
                return True
        return False


def h_(i: int):
    return 0.0007 * i              # 166 iterations
    #return 0.000701 * i            # 166 iterations
    #return 0.021 * (i ** (1/2))     # dziala dla E = 1e-2
    #return 0.03 * (i ** (1/2))     # zaden warunek stopu nie chce dawac dla tej metody rezultatow - algorytm gubi minimum
    #return 0.03 * (i ** (1/4))     # 117 iterations
    #return 0.03                    # jako porownanie dla 0.03 * i^(1/4) - gorsza jakosc i wiecej iteracji

def grad(x: np.ndarray) -> np.ndarray:
        x1, x2 = x[0], x[1]
        return np.array([10*(x1**3)-2*x1*(5*x2-1)-2, 5*x2-5*(x1**2)])

def func(x):
    x1, x2 = x[0], x[1]
    return 2.5*(x1**2 - x2)**2 + (1-x1)**2


def main():
    x_0 = np.array([-0.5, 1])
    #E = 1e-2
    E = 1e-3
    N_max = 100000
    algorithm = SimpleGradientMethod(func, grad, N_max, x_0, E, h_)

    if not algorithm.start_algorithm():
        print('Unable to optimize with given parameters')
    else:
        i, x_min = algorithm.iterations, algorithm.x_min
        print(f'Solution found after {i} iterations:\nminimal x: {x_min}\nfunction value: {func(x_min)}')

    print(f'Step before the last one: {algorithm.algorithm_steps[-2]}')

    print("\nVisualisation:")
    # parametry wykresu ustawione na stale
    x1 = np.linspace(-2, 2, 100)
    x2 = np.linspace(-1, 2, 100)
    x1, x2 = np.meshgrid(x1, x2)
    z = func([x1, x2])

    visualise_method(z, x1, x2, np.array(algorithm.algorithm_steps))

if __name__ == "__main__":
    main()
