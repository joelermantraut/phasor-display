import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import random as rand

class Socket():
    def __init__(self):
        pass

class UpdateDist(object):
    def __init__(self, ax):
        ax.plot([], [], color="red")
        ax.plot([], [], color="blue")
        ax.plot([], [], color="green")

        self.x = np.linspace(0, 1, 360)
        self.ax = ax

        # Set up plot parameters
        self.ax.set_xlim(0, 2 * np.pi)
        self.ax.set_ylim(0, 120)
        self.ax.grid(True)

        # self.ax.axvline(1, linestyle='--', color='black')
        # Por si quiero dibujar alguna linea adicional

    def init(self):
        for line_k in self.ax.lines:
            line_k.set_data([], [])

    def create_line(self, radio, theta):
        items = radio

        radio_data = np.linspace(0, radio, items)
        theta_data = np.empty(items)
        theta_data.fill(theta)
        return radio_data, theta_data

    def __call__(self, _):
        for line_k in self.ax.lines:
            radio = rand.randint(0, 100)
            theta = rand.randint(0, 360)

            radio_data, theta_data = self.create_line(radio, theta)

            line_k.set_data(theta_data, radio_data)

class Display():
    def __init__(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="polar")
        ud = UpdateDist(ax)
        self.anim = FuncAnimation(fig, ud, frames=np.arange(10), init_func=ud.init,
                            interval=10, blit=False, repeat=True)
        # Declaro anim como propia de la clase para que no se borre al salir del bloque

    def show(self):
        plt.show()

def main():
    display = Display()
    display.show()

if __name__ == "__main__":
    main()