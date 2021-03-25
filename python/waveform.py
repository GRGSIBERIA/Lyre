import wave
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

    def __init__(self, spfq: int, f0: float, L0: float, Q: float, radius: float, tf: float):
        """波形クラス

        Args:
            spfq (int): サンプリング周波数
            f0 (float): 基本周波数 [Hz]
            L0 (float): 弦の長さ [m]
            Q (float): Q値
            radius (float): 弦の半径 [m]
            
            tf (float): 終了時刻 [s]
        """
        dt = 1. / float(spfq)
        t = np.arange(0, tf, dt)            # 時間の配列 [s]
        A = radius * radius * np.pi         # 断面 [m^2]
        m = A * L0 * Waveform.dens          # 質量 [kg]
        rho = A * Waveform.dens             # 線密度 [kg/m]
        sigma = (2. * L0 * f0)**2. * rho    # 応力 [Pa]
        delta = (L0 * sigma) / Waveform.E   # 引張後のひずみ
        I = (radius * 2.)**4. * np.pi / 4   # 断面二次モーメント [m^4]
        T = (2. * L0 * f0)**2. * rho        # 張力 [N]
        B = (np.pi / (L0 + delta))**2. * ((Waveform.E * I) / T)

        self.__numof_harmonic = int((spfq / 2.) / f0) # 倍音の数
        self.__ns = [n + 2 for n in range(self.__numof_harmonic - 2)]

        self.__spfq = spfq
        self.__f0 = f0
        self.__L0 = L0
        self.__Q = Q
        self.__dt = dt
        self.__t = t
        self.__A = A
        self.__m = m
        self.__rho = rho
        self.__sigma = sigma
        self.__delta = delta
        self.__I = I
        self.__T = T
        self.__B = B

    
    def get_t(self):
        """時刻の配列を取得する

        Returns:
            np.ndarray: 時刻の配列
        """
        return self.__t

    
    def generate(self, v0: float, ratio: float):
        """波形を清々する

        Args:
            v0 (float): 初期速度
            ratio (float): 弦を弾いた位置 [0,1]

        Returns:
            [type]: [description]
        """
        state0 = [0., v0]

        k0 = self.__f0**2. * self.__m       # 剛性 [N/m]
        cc = 2. * np.sqrt(self.__m * k0)    # 臨界減衰係数
        c0 = cc / self.__Q                  # 減衰係数 [N･s/m]

        wave = odeint(func, state0, self.__t, args=(self.__m, k0, c0))[:,0]

        harmonics = []
        mode_num = 1. / ratio
        mode = 0

        for n in self.__ns:
            mode += 1
            acount = 1.
            if mode > mode_num:
                mode = 0
                acount = mode / mode_num

            fn = float(n) * f0 * np.sqrt(1. + self.__B * float(n)**2.) # 部分音周波数
            kn = fn**2. * self.__m      # 剛性 [N/m]
            cc = 2. * np.sqrt(self.__m * kn)
            cn = cc / self.__Q
            hw = odeint(func, state0, self.__t, args=(self.__m, kn, cn))[:,0]

            #wave += hw * acount
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

    selected_keynum = 40
    midi_freqs = [440. * 2.**((float(n)-69.)/12.) for n in range(128)]

    L0 = 0.5            # 弦の長さ [m]
    Q = 2000.           # Q値

    # 弦の半径 [m], ex. E2=0.58mm
    radius = 0.0005842

    ratio = 0.3         # 全体の長さから見た押さえた位置 [0,1]
    tf = 10.            # 終了時刻 [s]
    spfq = 8000.        # サンプリング周波数 [Hz]

    # 固有振動数 [Hz]
    f0 = midi_freqs[selected_keynum]

    sound = Waveform(spfq, f0, L0, Q, radius, tf)
    waveform = sound.generate(10, ratio)

    plot.plot(sound.get_t(), waveform)

    plot.tight_layout()
    plot.show()

    maxv = 32767. / max(waveform)
    w16 = [int(x * maxv) for x in waveform]
    bi_wave = struct.pack("h" * len(w16), *w16)

    wf = wave.Wave_write("test.wav")
    param = (1, 2, int(spfq), 'NONE', 'not compressed')
    wf.setparams(param)
    wf.writeframes(bi_wave)
    wf.close()

    """参考文献
    https://watlab-blog.com/2019/06/10/python-1dof-mck/
    """