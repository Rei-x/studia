import numpy as np



def gradient(f, x, y, h=1e-5):
    df_dx = (f(x + h, y) - f(x - h, y)) / (2 * h)
    df_dy = (f(x, y + h) - f(x, y - h)) / (2 * h)
    return np.array([df_dx, df_dy])



def gradient_descent_fixed_step(f, initial_point, tolerance, learning_rate=0.1):
    max_iterations=1000
    point = np.array(initial_point, dtype=float)

    for i in range(max_iterations):
        grad = gradient(f, point[0], point[1])
        new_point = point - learning_rate * grad

        #print(f"\tIteration {i+1}: Point = {point}, New Point = {new_point}, Function value = {f(point[0], point[1])}")

        if np.linalg.norm(new_point - point) < tolerance:
            point = new_point
            break

        point = new_point
        
    return point



def gradient_descent_adaptive_step(f, initial_point, tolerance, initial_learning_rate=1):
    max_iterations=1000
    point = np.array(initial_point, dtype=float)
    for i in range(max_iterations):
        learning_rate = initial_learning_rate
        grad = gradient(f, point[0], point[1])

        new_point = point - learning_rate * grad
        zabezpieczenie = 0
        while f(new_point[0], new_point[1]) >= f(point[0], point[1]):
            learning_rate /= 2
            new_point = point - learning_rate * grad
            zabezpieczenie += 1
            if zabezpieczenie > 1000:
                break

        #print(f"\tIteration {i+1}: Point = {point}, New Point = {new_point}, Function value = {f(point[0], point[1])}, Step = {learning_rate}")

        if np.linalg.norm(new_point - point) < tolerance:
            point = new_point
            break

        point = new_point
        
    return point



def gradient_descent_adaptive_step_2(f, initial_point, tolerance):
    max_iterations=1000
    point = np.array(initial_point, dtype=float)
    for i in range(max_iterations):
        learning_rate = 0.03 * (i+1)**0.5
        grad = gradient(f, point[0], point[1])

        new_point = point - learning_rate * grad

        #print(f"\tIteration {i+1}: Point = {point}, New Point = {new_point}, Function value = {f(point[0], point[1])}, Step = {learning_rate}")

        if np.linalg.norm(new_point - point) < tolerance:
            point = new_point
            break

        point = new_point
        
    return point