import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """
    pi_estimate = 0
    a = 1
    b = 1/(math.sqrt(2))
    t = (1/4)
    p = 1

    while abs(pi_estimate - math.pi) > target_error:

        ai = (a + b) / 2
        b = math.sqrt(a * b)
        t = (t - (p * ((ai - a)**2)))
        p = 2 * p
        a = ai

        pi_estimate = (((a + b)**2)/(4 * t))

    return pi_estimate


desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
