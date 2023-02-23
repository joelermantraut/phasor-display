import numpy as np
import matplotlib.pyplot as plt

class Socket():
    def __init__(self):
        pass

class Display():
    def __init__(self):
        theta = np.linspace(0,2 * np.pi)
        r = 5 + 50 * theta

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="polar")
        ax.plot(theta, r)

    def show(self):
        plt.show()

def main():
    display = Display()
    display.show()

if __name__ == "__main__":
    main()