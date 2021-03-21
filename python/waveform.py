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

    m = 0.5     # 質量 [kg]
    k = 1000.   # 剛性 [N/m]
    c = 5.      # 減衰係数 [N･s/m]
    #cc = 2. * np.sqrt(m * k)    # 臨界減衰比
    
    """
    zeta = c / cc
    omega = np.sqrt(k/m)
    omega_d = omega * np.sqrt(1 - np.power(zeta, 2.))
    sigma = omega_d * zeta
    """

    f = 7.               # 周波数 [Hz]
    state0 = [0.1, 0.]   # 初期値 [初期変位, 初速]

    # n_order_v = state0[1] / (state0[0] * omega)
 
    t0 = 0.         # 初期時刻 [s]
    tf = 10.        # 終了時刻 [s]
    dt = 1./48000.  # 時刻の刻み幅 [s]
    t = np.arange(t0, tf, dt)

    sol = odeint(func, state0, t, args=(m, k, c))
    plot.plot(t, sol[:,0])
    plot.tight_layout()
    plot.show()

    """参考文献
    https://watlab-blog.com/2019/06/10/python-1dof-mck/
    """