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


class Waveform:
    dens = 1145.         # 弦の密度 [kg/m^3], 1145 kg/m^3 はナイロン弦
    E = 5.4e9            # ヤング率 [GPa]

    def __init__(self, spfq: int, f0: float, L0: float, Q: float, radius: float, ratio: float, tf: float):
        """波形クラス

        Args:
            spfq (int): サンプリング周波数
            f0 (float): 基本周波数 [Hz]
            L0 (float): 弦の長さ [m]
            Q (float): Q値
            radius (float): 弦の半径 [m]
            ratio (float): 弦を押さえた位置 [0,1]
            tf (float): 終了時刻 [s]
        """
        dt = 1. / float(spfq)
        t = np.arange(0, tf, dt)            # 時間の配列 [s]
        A = radius * radius * np.pi         # 断面 [m^2]
        m = A * L0 * Waveform.dens          # 質量 [kg]
        rho = A * Waveform.dens             # 線密度 [kg/m]
        sigma = (2. * L0 * f0)**2. * rho    # 応力 [Pa]
        delta = (L0 * sigma) / E            # 引張後のひずみ
        I = (radius * 2.)**4. * np.pi / 4   # 断面二次モーメント [m^4]
        T = (2. * L0 * f0)**2. * rho        # 張力 [N]
        B = (np.pi / (L0 + delta))**2. * ((E * I) / T)

        self.__numof_harmonic = int((spfq / 2.) / f0) # 倍音の数
        self.__ns = [n + 2 for n in range(numof_harmonic - 2)]

        self.__spfq = spfq
        self.__f0 = f0
        self.__L0 = L0
        self.__Q = Q
        self.__dt = dt
        self.__t = T
        self.__A = A
        self.__m = m
        self.__rho = rho
        self.__sigma = sigma
        self.__delta = delta
        self.__I = I
        self.__T = T
        self.__B = B

    
    def generate(self, v0: float):
        state0 = [0., v0]

        k0 = self.__f0**2. * self.__m       # 剛性 [N/m]
        cc = 2. * np.sqrt(self.__m * k0)    # 臨界減衰係数
        c0 = cc / self.__Q                  # 減衰係数 [N･s/m]
        wave = np.array(odeint(func, state0, self.__t, args=(self.__m, k0, c0))[:,0])
        harmonics = []

        for n in ns:
            fn = float(n) * f0 * np.sqrt(1. + self.__B * float(n)**2.) # 部分音周波数
            kn = fn**2. * self.__m      # 剛性 [N/m]
            cc = 2. * np.sqrt(m * kn)
            cn = cc / self.__Q
            hw = odeint(func, state0, self.__t, args(self.__m, kn, cn))[:,0]
            wave += hw

        return wave

if __name__ == "__main__":
    """周波数、重量、減衰比を与えれば機械の周波数応答を自動計算する
    Args以下のコメントはプログラムの入力に使われる変数
    
    Args:
        selected_keynum (int): 基本周波数として入力したいMIDIノート番号
        L0 (float): 弦の長さ [m]
        Q (float): Quarity Factor, Q値
        tf (float): 終了時刻 [s]
        radius (float): 弦の半径 [m]
        ratio (float): 全体の長さから見た押さえた位置 [0,1]
    """

    selected_keynum = 69
    midi_freqs = [440. * 2.**((float(n)-69.)/12.) for n in range(128)]

    L0 = 0.5            # 弦の長さ [m]
    Q = 2000.           # Q値
    radius = 0.001      # 弦の半径 [m]
    ratio = 0.3         # 全体の長さから見た押さえた位置 [0,1]

    # 以下は定数とする
    dens = 1145.         # 弦の密度 [kg/m^3], 1145 kg/m^3 はナイロン弦
    E = 5.4e9            # ヤング率 [GPa]

    # 固有振動数 [Hz]
    f0 = midi_freqs[selected_keynum]

    """
    f0 = 1/2L sqrt(T/rho)
    2Lf0 = sqrt(T/rho)
    (2Lf0)^2 = T/rho
    (2Lf0)rho = T
    """

    A = radius * radius * np.pi         # 断面 [m^2]
    m = A * L0 * dens                   # 質量 [kg]
    rho = A * dens                      # 線密度 [kg/m]
    k = f0**2. * m                      # 剛性 [N/m]
    cc = 2. * np.sqrt(m * k)            # 臨界減衰係数
    c = cc / Q                          # 減衰係数 [N･s/m]
    sigma = (2. * L0 * f0)**2. * rho    # 応力 [Pa]
    delta = (L0 * sigma) / E            # 引張後のひずみ
    I = (radius * 2.)**4. * np.pi / 4   # 断面二次モーメント [m^4]
    T = (2. * L0 * f0)**2. * rho        # 張力 [N]

    state0 = [0., 10.]   # 初期値 [初期変位, 初速]

    t0 = 0.         # 初期時刻 [s]
    tf = 60.        # 終了時刻 [s]
    spfq = 48000.   # サンプリング周波数 [Hz]
    dt = 1./spfq    # 時刻の刻み幅 [s]
    t = np.arange(t0, tf, dt)
    
    numof_harmonic = int(spfq / f0) # 倍音の数

    B = (np.pi / (L0 + delta))**2. * E * I / T
    ns = [n + 2 for n in range(numof_harmonic - 2)]

    for n in ns:
        elastic_fn = n * f0 * np.sqrt(1. + B * n**2.)
        print(n, elastic_fn, elastic_fn**2. * m)
        

    sol = odeint(func, state0, t, args=(m, k, c))
    plot.plot(t, sol[:,0])
    plot.tight_layout()
    plot.show()

    print(state0)

    """参考文献
    https://watlab-blog.com/2019/06/10/python-1dof-mck/
    """