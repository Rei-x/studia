from .gradient_descend import *
import random


# funkcja celu
def f(x):
    return 7 * x**2 - 17 * x + 20


# parametry
initial_point = 10
tolerance = 10 ** (-2)
fixed_learning_rate = 0.1
adaptive_learning_rate = 1

points = []
for i in range(10):
    random_x = random.uniform(-10, 10)
    points.append(random_x)


print("------------------------------------------------------------------------")

print("\nFIXED STEP:")
minimum_point = gradient_descent_fixed_step(
    f, initial_point, tolerance, fixed_learning_rate
)
print(f"Minimum znalezione w punkcie: {minimum_point}")
print(f"Wartość funkcji w minimum: {f(minimum_point)}")

print("\nADAPTIVE STEP:")
minimum_point = gradient_descent_adaptive_step(
    f, initial_point, tolerance, adaptive_learning_rate
)
print(f"Minimum znalezione w punkcie: {minimum_point}")
print(f"Wartość funkcji w minimum: {f(minimum_point)}")

print("\nADAPTIVE STEP 2:")
minimum_point = gradient_descent_adaptive_step_2(f, initial_point, tolerance)
print(f"Minimum znalezione w punkcie: {minimum_point}")
print(f"Wartość funkcji w minimum: {f(minimum_point)}")

print("\nADAPTIVE STEP WIECEJ PUNKTOW:")
min_point = points[0]
min_start_point = points[0]
for start_point in points:
    minimum_point = gradient_descent_adaptive_step(
        f, start_point, tolerance, adaptive_learning_rate
    )
    if f(minimum_point) < f(min_point):
        min_point = minimum_point
        min_start_point = start_point
print(f"Wystartowano z punktu: {min_start_point}")
print(f"Minimum znalezione w punkcie: {min_point}")
print(f"Wartość funkcji w minimum: {f(min_point)}")
