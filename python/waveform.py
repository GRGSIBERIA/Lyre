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
        m (float): 質量 [kg]
        Q (float): Quarity Factor, Q値
        tf (float): 終了時刻 [s]
        radius (float): 弦の半径 [m]
    """

    f0 = 7.             # 固有振動数 [Hz]
    m = 0.5             # 質量 [kg]
    Q = 20.             # Q値
    radius = 0.001      # 弦の半径 [m]

    k = f0 ** 2 * m             # 剛性 [N/m]
    cc = 2. * np.sqrt(m * k)    # 臨界減衰係数
    c = cc / Q                  # 減衰係数 [N･s/m]
    
    state0 = [0., 10.]   # 初期値 [初期変位, 初速]

    t0 = 0.         # 初期時刻 [s]
    tf = 10.        # 終了時刻 [s]
    spfq = 48000.   # サンプリング周波数 [Hz]
    dt = 1./spfq    # 時刻の刻み幅 [s]
    numof_harmonic = int(spfq / f0) # 倍音の数
    t = np.arange(t0, tf, dt)

    sol = odeint(func, state0, t, args=(m, k, c))
    plot.plot(t, sol[:,0])
    plot.tight_layout()
    plot.show()

    """参考文献
    https://watlab-blog.com/2019/06/10/python-1dof-mck/
    """