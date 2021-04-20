import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

if __name__ == "__main__":
    print("visualize frequency (Hz) > ", end="")
    visfreq = float(input())
    print("generate frequency (MIDI note number, C4 = 69) > ", end="")
    f0 = 440. * 2.**((float(input()) - 69.) / 12.)
    print("f0 = {}".format(f0))

    t = np.arange(0, 1. / f0 * visfreq, 1./44100.)
    square = signal.square(2. * np.pi * f0 * t)
    sine = np.sin(8. * np.pi * f0 * t)

    print(t)

    plt.figure()
    plt.plot(t, square)
    plt.plot(t, sine)
    plt.tight_layout()
    plt.show()