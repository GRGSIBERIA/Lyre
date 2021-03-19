import numpy as np
import matplotlib.pyplot as plot

if __name__ == "__main__":
    """周波数、重量、減衰比を与えれば機械の周波数応答を自動計算する
    """
    print("Normal mode(f0) frequency (Hz): ", end="")
    f0 = float(input())
    print("Mass (kg): ", end="")
    mass = float(input())
    print("Damping ratio [0,1]: ", end="")
    damping_ratio = float(input())

    # 臨界減衰比は下式で求められる
    # f0 = sqrt(k/m)
    # f0^2 = k/m
    # f0^2 * m = k

    # 減衰比は下式で求められる
    # z = c / cc

    k = f0**2. * mass
    critical_damping = 2. * np.sqrt(mass * k)
    damping_coeff = critical_damping / damping_ratio

    print("--------------------------------------------------")
    print("Spring constant (N): {}".format(k))
    print("Critical damping ratio: {}".format(critical_damping))
    print("Damping Coefficient: {}".format(damping_coeff))