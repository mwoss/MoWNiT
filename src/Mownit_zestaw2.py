from matplotlib import pyplot as plt

plt.plot()

def function1(x):
    return x ** 2 - 5


def function2(x):
    return x ** 2 - 2 * x + 1


def derivative_fun(func, x, h=1e-6):
    return (func(x + h) - func(x - h)) / (2 * h)


def check_sign(a, b):
    return a * b <= 0


from time import process_time


def time_decorator(fun):
    def wrapper(*args, **kwargs):
        start = process_time()
        res = fun(*args, **kwargs)
        print("Function name: {0}, CPU time: {1}"
              .format(fun.__name__, process_time() - start))
        return res

    return wrapper


def bisection(func, x_s, x_e, epsilon):
    assert check_sign(func(x_s), func(x_e))
    iterator = 0
    midpoint = x_s
    while abs(x_e - x_s) > epsilon:
        iterator += 1
        midpoint = (x_s + x_e) / 2.0
        if abs(func(midpoint)) <= epsilon:
            return midpoint, iterator
        elif not check_sign(func(x_s), func(midpoint)):
            x_s = midpoint
        else:
            x_e = midpoint
    return midpoint, iterator


def secant(func, x_s, x_e, epsilon, max_iterations=100):
    fx0 = func(x_s)
    fx1 = func(x_e)
    for iterator in range(max_iterations):
        if abs(fx1) < epsilon:
            return x_e, iterator
        try:
            denominator = (fx1 - fx0) / (x_e - x_s)
            x2 = x_e - fx1 / denominator
        except ZeroDivisionError:
            print("fx1 - fx0 error")
            raise

        x_s, x_e = x_e, x2
        fx0, fx1 = fx1, func(x_e)
    return x_e, iterator


def newton_raphson(func, x0, epsilon, max_iterations=100):
    for iterator in range(max_iterations):
        x1 = x0 - (func(x0) / derivative_fun(func, x0))
        if abs(x1 - x0) < epsilon:
            return x1, iterator
        else:
            x0 = x1
    return x1, iterator


@time_decorator
def newton_10k_iterations(func, x0, epsilon):
    for _ in range(10000):
        newton_raphson(func, x0, epsilon)


@time_decorator
def bisection_10k_iterations(func, x_s, x_e, epsilon):
    for _ in range(10000):
        bisection(func, x_s, x_e, epsilon)


@time_decorator
def secant_10k_iterations(func, x_s, x_e, epsilon):
    for _ in range(10000):
        secant(func, x_s, x_e, epsilon)


if __name__ == '__main__':
    # Bisection method test
    print("Bisection method")
    func1_value, iter1 = bisection(function1, 0, 5, 0.00003)
    # func2_value = bisection(function2, 0, 5, 0.00003)
    print(function1.__name__ + "\nRoot x = {0} and its calculated value(should be close to 0): {1}"
          .format(func1_value, function1(func1_value)))
    # print(function2.__name__ + "\nRoot x = {0} and its calculated value(should be close to 0): {1}"
    # .format(func2_value, function2(func2_value)))

    # ************************************************

    # Secant method test
    print("Secant method")
    try:
        func1_value2, iter1_2 = secant(function1, 0, 5, 0.00003)
        func2_value2, iter2_2 = secant(function2, 0, 5, 0.00003)
        print(function1.__name__ + "\nRoot x = {0} and its calculated value(should be close to 0): {1}"
              .format(func1_value2, function1(func1_value2)))
        print(function2.__name__ + "\nRoot x = {0} and its calculated value(should be close to 0): {1}"
              .format(func2_value2, function2(func2_value2)))
    except Exception as e:
        print(str(e))

    # ************************************************

    # Newton-Raphson method test
    print("Newton-Raphson method")
    func1_value3, iter1_3 = newton_raphson(function1, 5, 0.00003)
    func2_value3, iter2_3 = newton_raphson(function2, 5, 0.00003)
    print(function1.__name__ + "\nRoot x = {0} and its calculated value(should be close to 0): {1}"
          .format(func1_value3, function1(func1_value3)))
    print(function2.__name__ + "\nRoot x = {0} and its calculated value(should be close to 0): {1}"
          .format(func2_value3, function2(func2_value3)))

    # ************************************************

    # CPU time
    bisection_10k_iterations(function1, 0, 5, 0.00003)
    secant_10k_iterations(function1, 0, 5, 0.00003)
    newton_10k_iterations(function1, 5, 0.00003)
    print("")
    # bisection_10k_iterations(function1, 0, 3, 0.00003)
    secant_10k_iterations(function2, 0, 5, 0.00003)
    newton_10k_iterations(function2, 5, 0.00003)
    print('')
    print("Number of iterations for: {0} = {1}".format(function1.__name__, iter1))
    print("Number of iterations for: {0} = {1}".format(function1.__name__, iter1_2))
    print("Number of iterations for: {0} = {1}".format(function2.__name__, iter2_2))
    print("Number of iterations for: {0} = {1}".format(function1.__name__, iter1_3))
    print("Number of iterations for: {0} = {1}".format(function2.__name__, iter2_3))
