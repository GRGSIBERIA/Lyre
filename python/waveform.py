import wave
import struct
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

    def __init__(self, spfq: int, notenum: int, L0: float, Q: float, tf: float):
        """波形クラス

        Args:
            spfq (int): サンプリング周波数
            notenum (int): ノート番号
            L0 (float): 弦の長さ [m]
            Q (float): Q値
            
            tf (float): 終了時刻 [s]
        """
        f0 = 440. * 2.**(float(notenum-69)/12.)
        radius = (-0.0019 * notenum + 0.1234) * 25.4 / 2. / 1000.

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
        self.__tf = tf
        self.__dt = 1. / float(self.__spfq)
        self.__t = np.arange(0, self.__tf, self.__dt)
        self.__A = A
        self.__m = m
        self.__rho = rho
        self.__sigma = sigma
        self.__delta = delta
        self.__I = I
        self.__T = T
        self.__B = B
        self.__radius = radius
        print(self.__radius)
        print(self.__f0)
    
    def get_t(self):
        """時刻の配列を取得する

        Returns:
            np.ndarray: 時刻の配列
        """
        return self.__t

    def __sinwave(self, freq: float, amp: float) -> np.ndarray:
        return np.sin(2. * np.pi * freq * self.__t) * (1. / np.exp(self.__t * amp))
    
    def generate(self, v0: float, ratio: float) -> np.ndarray:
        """波形を清々する

        Args:
            v0 (float): 初期速度
            ratio (float): 弦を弾いた位置 [0,1]

        Returns:
            np.ndarray: 波形のnumpy配列
        """
        amp = 1.
        wave = self.__sinwave(self.__f0, amp)

        for ns in self.__ns:
            amp += 1.
            wave += self.__sinwave(self.__f0 * ns, amp)

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

    notenum = 50
    L0 = 0.5            # 弦の長さ [m]
    Q = 2000.           # Q値

    ratio = 0.3         # 全体の長さから見た押さえた位置 [0,1]
    tf = 10.            # 終了時刻 [s]
    spfq = 8000.        # サンプリング周波数 [Hz]
    v0 = 0.05             # 初期速度

    sound = Waveform(spfq, notenum, L0, Q, tf)
    waveform = sound.generate(v0, ratio)

    plot.plot(sound.get_t(), waveform)

    plot.tight_layout()
    plot.show()

    maxv = 16384. / max(np.abs(waveform))
    print(maxv)
    w16 = [int(x * maxv) for x in waveform]
    bi_wave = struct.pack("h" * len(w16), *w16)

    wf = wave.Wave_write("test.wav")
    param = (1, 2, int(spfq), len(bi_wave), 'NONE', 'not compressed')
    wf.setparams(param)
    wf.writeframes(bi_wave)
    wf.close()

    """参考文献
    https://watlab-blog.com/2019/06/10/python-1dof-mck/
    """