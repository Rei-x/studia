def gradient(f, x, h=1e-5):
    df_dx = (f(x + h) - f(x - h)) / (2 * h)
    return df_dx


def gradient_descent_fixed_step(f, initial_point, tolerance, learning_rate=0.1):
    max_iterations = 1000
    point = initial_point

    for i in range(max_iterations):
        grad = gradient(f, point)
        new_point = point - learning_rate * grad

        print(
            f"\tIteration {i+1}: Point = {point}, New Point = {new_point}, Function value = {f(point)}"
        )

        if abs(new_point - point) < tolerance:
            point = new_point
            break

        point = new_point

    return point


def gradient_descent_adaptive_step(
    f, initial_point, tolerance, initial_learning_rate=1
):
    max_iterations = 1000
    point = initial_point
    for i in range(max_iterations):
        learning_rate = initial_learning_rate
        grad = gradient(f, point)

        new_point = point - learning_rate * grad
        zabezpieczenie = 0
        while f(new_point) >= f(point):
            learning_rate /= 2
            new_point = point - learning_rate * grad
            zabezpieczenie += 1
            if zabezpieczenie > 1000:
                break

        print(
            f"\tIteration {i+1}: Point = {point}, New Point = {new_point}, Function value = {f(point)}, Step = {learning_rate}"
        )

        if abs(new_point - point) < tolerance:
            point = new_point
            break

        point = new_point

    return point


def gradient_descent_adaptive_step_2(f, initial_point, tolerance):
    max_iterations = 1000
    point = initial_point
    for i in range(max_iterations):
        learning_rate = 0.03 * (i + 1) ** 0.5
        grad = gradient(f, point)

        new_point = point - learning_rate * grad

        print(
            f"\tIteration {i+1}: Point = {point}, New Point = {new_point}, Function value = {f(point)}, Step = {learning_rate}"
        )

        if abs(new_point - point) < tolerance:
            point = new_point
            break

        point = new_point

    return point
