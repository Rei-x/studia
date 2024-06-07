from gradient_descend import *
import random


# funkcja celu
def f(x):
    return (x + 3) * x * (x - 3)


# funkcja kary, suma kwadratow ograniczen
def S(x):
    g1 = (-1) * x - 2
    g2 = x - 2
    return max(0, g1) ** 2 + max(0, g2) ** 2


# parametry
initial_point = 0
tolerance = 10 ** (-3)
adaptive_learning_rate = 1
initial_c = 1

points = []
for i in range(10):
    random_x = random.uniform(-10, 10)
    points.append(random_x)


def kara_zewnetrzna(start_point):
    max_iterations = 1000
    point = start_point
    c = initial_c
    for i in range(max_iterations):
        F = lambda x: f(x) + c * S(x)
        new_point = gradient_descent_adaptive_step(
            F, point, tolerance, adaptive_learning_rate
        )

        print(
            f"Iteration {i+1}: Point = {point}, New Point = {new_point}, Function value = {f(point)}, c = {c}"
        )

        if abs(new_point - point) < tolerance:
            point = new_point
            break

        point = new_point
        c *= 2

    return point


print("\nKARA ZEWNETRZNA:")
minimum_point = kara_zewnetrzna(initial_point)
print(f"Minimum znalezione w punkcie: {minimum_point}")
print(f"Wartość funkcji w minimum: {f(minimum_point)}")


print("\nKARA ZEWNETRZNA WIECEJ PUNKTOW:")
min_point = points[0]
min_start_point = points[0]
for start_point in points:
    minimum_point = kara_zewnetrzna(start_point)
    if f(minimum_point) < f(min_point):
        min_point = minimum_point
        min_start_point = start_point
print(f"Wystartowano z punktu: {min_start_point}")
print(f"Minimum znalezione w punkcie: {min_point}")
print(f"Wartość funkcji w minimum: {f(min_point)}")
