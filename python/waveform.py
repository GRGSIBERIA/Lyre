import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plot

def func(state, t, m, k, c):
    """ソルバ

    Args:
        state (odeint.state): 常微分方程式の変位x1と速度x2
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
    Args以下のコメントはプログラムの入力に使われる変数
    
    Args:
        f0 (float): 固有振動数 [Hz]
        L0 (float): 弦の長さ [m]
        Q (float): Quarity Factor, Q値
        tf (float): 終了時刻 [s]
        radius (float): 弦の半径 [m]
        ratio (float): 全体の長さから見た押さえた位置 [0,1]
    """

    f0 = 7.             # 固有振動数 [Hz]
    L0 = 0.5            # 弦の長さ [m]
    Q = 20.             # Q値
    radius = 0.001      # 弦の半径 [m]
    ratio = 0.3         # 全体の長さから見た押さえた位置 [0,1]

    # 以下は定数とする
    rho = 1145.         # 弦の密度 [kg/m^3], 1145 kg/m^3 はナイロン弦
    E = 5.4e9           # ヤング率 [GPa]

    """
    2Lf = sqrt(T/rhoA)
    (2Lf)^2 = T/rhoA
    T = (2Lf)^2 rho A
    """

    A = radius * radius * np.pi         # 断面 [m^2]
    m = A * L0 * dens                   # 質量 [kg]
    k = f0**2. * m                      # 剛性 [N/m]
    cc = 2. * np.sqrt(m * k)            # 臨界減衰係数
    c = cc / Q                          # 減衰係数 [N･s/m]
    sigma = (2. * L0 * f0)**2. * rho    # 応力
    delta = (L0 * sigma) / E            # 引張後のひずみ

    state0 = [0., 10.]   # 初期値 [初期変位, 初速]

    t0 = 0.         # 初期時刻 [s]
    tf = 10.        # 終了時刻 [s]
    spfq = 48000.   # サンプリング周波数 [Hz]
    dt = 1./spfq    # 時刻の刻み幅 [s]
    t = np.arange(t0, tf, dt)
    
    numof_harmonic = int(spfq / f0) # 倍音の数

    sol = odeint(func, state0, t, args=(m, k, c))
    plot.plot(t, sol[:,0])
    plot.tight_layout()
    plot.show()

    """参考文献
    https://watlab-blog.com/2019/06/10/python-1dof-mck/
    """