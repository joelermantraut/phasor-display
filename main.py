import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from matplotlib.animation import FuncAnimation

import socket

class SocketClient():
    def __init__(self, host, port):
        """
        Socket class to communicate.
        """
        self.HOST = host
        self.PORT = port
        self.BUFFER_SIZE = 1024
        self.init()

    def init(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.HOST, self.PORT))

    def read_data(self):
        data = None
        if self.is_available():
            data = self.server.recv(self.BUFFER_SIZE).decode("utf-8").split(",")
            data = [int(item) for item in data]
        # Receives comma separated values
        
        return data

    def is_available(self):
        if self.server.recv(self.BUFFER_SIZE, socket.MSG_PEEK):
            return True
    
        return False

class UpdateDist(object):
    """
    Class to overwrite update event.
    """
    def __init__(self, ax, socketObject):
        self.ax = ax
        self.socketObject = socketObject

        self.x = np.linspace(0, 1, 360)

        # Set up plot parameters
        self.ax.set_xlim(0, 2 * np.pi)
        self.ax.set_ylim(0, 120)
        self.ax.grid(True)

        self.running = True

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
        if not self.running:
            return
        
        if self.socketObject.is_available():
            data = self.socketObject.read_data()
            if len(data) != 2 * len(self.ax.lines):
                return
            # Expects two values per line, radio and theta, interleaved
            
            radio = [data[index] for index in range(0, len(data), 2)] # Even elements
            theta = [data[index + 1] for index in range(0, len(data), 2)] # Odd elements

            for index, line_k in enumerate(self.ax.lines):
                radio_data, theta_data = self.create_line(radio[index], theta[index])

                line_k.set_data(theta_data, radio_data)

    def stop_and_run(self):
        self.running = not self.running

class Display():
    """
    Class to display polar plot. Parameters received are the 
    lines names, and socketObject to read received values.
    """
    def __init__(self, TITLE, X_NAME, Y_NAME, LINES_NAMES, socketObject):
        self.COLORS = [
            "red",
            "blue",
            "green",
            ""
        ]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="polar")

        plt.title(TITLE)
        plt.xlabel(X_NAME)
        plt.ylabel(Y_NAME, labelpad=30)
        # Add space to not overwrite angle label

        colors = list(mcolors.BASE_COLORS.values())

        for i in range(len(LINES_NAMES)):
            ax.plot([], [], color=colors[i  % len(colors)])

        ax.legend(ax.lines, LINES_NAMES, loc="upper left", draggable=True, framealpha=1, borderaxespad=-3)

        self.ud = UpdateDist(ax, socketObject)
        self.anim = FuncAnimation(
            fig,
            self.ud,
            frames=np.arange(10), # 10 frames
            init_func=self.ud.init,
            interval=10, # Updating interval
            blit=False,
            repeat=True
        )
        # Declare "anim" as property to not delete it after instance

        fig.canvas.mpl_connect('button_press_event', self.onclick)
        # Stop updating after left click on plot.

    def onclick(self, _):
        self.ud.stop_and_run()

    def show(self):
        plt.show()

def main():
    socketObject = SocketClient("localhost", 65432)

    display = Display("Phasor Display", "X axis", "Y axis", ["blue", "green", "red"], socketObject)
    display.show()

if __name__ == "__main__":
    main()