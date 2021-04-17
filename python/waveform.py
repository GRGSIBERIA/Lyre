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

    def __init__(self, spfq: int, notenum: int, B: float):
        """波形クラス

        Args:
            spfq (int): サンプリング周波数
            notenum (int): ノート番号
            B (float): B値
        """
        f0 = 440. * 2.**(float(notenum-69)/12.)
        radius = (-0.0019 * notenum + 0.1234) * 25.4 / 2. / 1000.

        self.__numof_harmonic = int((spfq / 2.) / f0) # 倍音の数
        self.__ns = [n + 2 for n in range(self.__numof_harmonic - 2)]

        self.__spfq = spfq
        self.__f0 = f0
        self.__dt = 1. / float(self.__spfq)
        self.__B = B

    def __sinwave(self, t: np.ndarray, freq: float, amp: float) -> np.ndarray:
        return np.sin(2. * np.pi * freq * t) * (self.__f0 / np.exp(t * amp))
    
    def generate(self, v0: float, ratio: float, start: float, end: float) -> np.ndarray:
        """波形を清々する

        Args:
            v0 (float): 初期速度 [m/s]
            start (float): 開始時間 [s]
            end (float): 終了時間 [s]
            ratio (float): 弦を弾いた位置 [0,1]

        Returns:
            np.ndarray: 波形のnumpy配列
        """
        amp = 1.

        t = np.arange(start, end, self.__dt)
        wave = self.__sinwave(t, self.__f0, amp)

        for n in self.__ns:
            f_elastic = self.__f0 * n * np.sqrt(1 + self.__B * n ** 2.)

            wave += self.__sinwave(t, f_elastic, amp)

        return wave
    
    def get_t(self, start: float, end: float) -> np.ndarray:
        return np.arange(start, end, self.__dt)

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

    ratio = 0.3         # 全体の長さから見た押さえた位置 [0,1]
    tf = 10.            # 終了時刻 [s]
    spfq = 8000.        # サンプリング周波数 [Hz]
    v0 = 0.05             # 初期速度
    start = 0.
    end = 10. 
    B = 0.000001

    sound = Waveform(spfq, notenum, B)
    waveform = sound.generate(v0, ratio, start, end)

    plot.plot(sound.get_t(start, end), waveform)

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