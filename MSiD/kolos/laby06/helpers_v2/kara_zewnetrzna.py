from gradient_descend import *
import random


# funkcja celu
def f(x, y):
    return 0.5 * (x + 2 * y) + 0.5 * (2 * x + y)


# funkcja kary, suma kwadratow ograniczen
def S(x, y):
    g1 = 6 - x - y
    g2 = 8 - 2 * x - y
    g3 = 5 - 0.75 * x - y
    g4 = -1 * x
    g5 = -1 * y
    return (
        max(0, g1) ** 2
        + max(0, g2) ** 2
        + max(0, g3) ** 2
        + max(0, g4) ** 2
        + max(0, g5) ** 2
    )


# parametry
initial_point = [10, 10]
tolerance = 10 ** (-3)
adaptive_learning_rate = 1
initial_c = 1


points = []
for i in range(10):
    random_x = random.uniform(-10, 10)
    random_y = random.uniform(-10, 10)
    points.append([random_x, random_y])


def kara_zewnetrzna(start_point):
    max_iterations = 1000
    point = start_point
    c = initial_c
    for i in range(max_iterations):

        def F(x, y):
            return f(x, y) + c * S(x, y)

        new_point = gradient_descent_adaptive_step(  # noqa: F405
            F, point, tolerance, adaptive_learning_rate
        )

        print(
            f"Iteration {i+1}: Point = {point}, New Point = {new_point}, Function value = {f(point[0], point[1])}, c = {c}"
        )

        if np.linalg.norm(new_point - point) < tolerance:
            point = new_point
            break

        point = new_point
        c *= 2

    return point


print("\nKARA ZEWNETRZNA:")
minimum_point = kara_zewnetrzna(initial_point)
print(f"Minimum znalezione w punkcie: {minimum_point}")
print(f"Wartość funkcji w minimum: {f(minimum_point[0], minimum_point[1])}")


print("\nKARA ZEWNETRZNA WIECEJ PUNKTOW:")
min_point = points[0]
min_start_point = points[0]
for start_point in points:
    minimum_point = kara_zewnetrzna(start_point)
    if f(minimum_point[0], minimum_point[1]) < f(min_point[0], min_point[1]):
        min_point = minimum_point
        min_start_point = start_point
print(f"Wystartowano z punktu: {min_start_point}")
print(f"Minimum znalezione w punkcie: {min_point}")
print(f"Wartość funkcji w minimum: {f(min_point[0], min_point[1])}")
