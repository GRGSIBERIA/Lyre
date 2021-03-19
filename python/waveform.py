import numpy as np
import matplotlib.pyplot as plot

if __name__ == "__main__":
    print("midi note number: ", end="")
    notenum = int(input())
    print("alpha: ", end="")
    alpha = float(input())
    print("beta: ", end="")
    beta = float(input())
    print("sampling frequency (Hz): ", end="")
    sphz = float(input())
    print("how long time (s): ", end="")
    lt = float(input())
    
    freq = 440. * 2 ** ((notenum - 69) / 12.)

    times = np.arange(0., lt, 1. / sphz)  # 0～t秒まで48kHzで

    frequencies = np.arange(1., sphz, 1.)  # 周波数
    daming_ratio = alpha / (2 * frequencies) + (beta * frequencies) / 2. # レイリー減衰

    plot.figure()
    plot.plot(frequencies, daming_ratio)
    plot.plot(frequencies, alpha / (2. * frequencies))
    plot.plot(frequencies, beta * frequencies / 2.)
    plot.tight_layout()
    plot.show()