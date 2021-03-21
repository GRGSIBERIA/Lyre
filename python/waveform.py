import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plot

def func(state, t, m, k, c):
    """ソルバ

    Args:
        state (odeint.state): 常微分方程式のfunction側
        t (float): 時刻 [s]
        m (float): 質点の重さ [kg]
        k (float): 質点の弾性 [N/m]
        c (float): 減衰係数 [N･s/m]
    """
    x1, x2 = state
    dxdt = -(c/m) * x2 - (k/m) * x1
    return [x2, dxdt]

if __name__ == "__main__":
    """周波数、重量、減衰比を与えれば機械の周波数応答を自動計算する
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
    """

    m = 0.5
    k = 1000.
    c = 5.
    cc = 2. * np.sqrt(m * k)    # 臨界減衰比
    zeta = c / cc
    omega = np.sqrt(k/m)
    omeda_d = omega * np.sqrt(1 - np.power(zeta, 2.))
    sigma = omega_d * zeta

    f = 7. 
    state0 = [0.1, 0.]   # 初期値 [初期変位, 初速]

    n_order_v = state0[1] / (state0[0] * omega)
 
    # 減衰振動の場合
    if zeta < 1:
        """減衰振動
        """
        X = np.sqrt(np.power(state0[0], 2) + np.power((state0[1] + sigma * state0[0])/omega_d, 2))
        phi = np.arctan((state0[1] + (sigma * state0[0]))/(state0[0] * omega_d))
        theory = np.exp(- sigma * t) * X * np.cos(omega_d * t - phi)
    elif zeta == 1:
        """臨界減衰
        """
        theory = state0[0] * np.exp(- omega * t) * ((n_order_v + 1) * omega * t + 1)
    else:
        """過減衰
        """
        theory = state0[0] * np.exp(- zeta * omega * t) * (\
            np.cosh(omega * t * np.sqrt(zeta ** 2 - 1))\
            + (n_order_v + zeta) / (np.sqrt(zeta ** 2 + 1))\
            * np.sinh(omega * t * np.sqrt(zeta ** 2 - 1)))

    t0 = 0.         # 初期時刻 [s]
    tf = 10.        # 終了時刻 [s]
    dt = 1./48000.  # 時刻の刻み幅 [s]
    t = np.arange(0, tf, dt)

    sol = odeint(func, state0, t, args(m, k, c))
    plot.plot(t, sol[:,0])
    plot.tight_layout()
    plot.show()

    """参考文献
    https://watlab-blog.com/2019/06/10/python-1dof-mck/
    """