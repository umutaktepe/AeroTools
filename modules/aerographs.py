import matplotlib.pyplot as plt
import numpy as np


class Plot:

    def __init__(self):
        super(Plot, self).__init__()

    def clvsvelocity(self, cl, minv, maxv, incr=0.1, linecolor='b', lw=2, grid=True, title='CL vs Velocity'):

        v = np.arange(minv, maxv, incr)

        fig, axes = plt.subplots()
        fig.canvas.set_window_title(str(title))
        axes.plot(v, cl, color=str(linecolor), lw=int(lw))
        axes.set(xlabel='Velocity', ylabel='Lift Coefficient (CL)', title=str(title))
        axes.grid(grid)

        return plt.show()

    def thrustrequiredvsvelocity(self, thrust, minv, maxv, incr=0.1, linecolor='b', lw=2, grid=True, title='Thrust Required vs Velocity'):

        v = np.arange(minv, maxv, incr)

        fig, axes = plt.subplots()
        fig.canvas.set_window_title(str(title))
        axes.plot(v, thrust, color=str(linecolor), lw=int(lw))
        axes.set(xlabel='Velocity', ylabel='Thrust Required (N)', title=str(title))
        axes.grid(grid)

        return plt.show()

    def powerrequiredvsvelocity(self, power, minv, maxv, incr=0.1, linecolor='b', lw=2, grid=True, title='Power Required vs Velocity'):

        v = np.arange(minv, maxv, incr)

        fig, axes = plt.subplots()
        fig.canvas.set_window_title(str(title))
        axes.plot(v, power, color=str(linecolor), lw=int(lw))
        axes.set(xlabel='Velocity', ylabel='Power Required (W)', title=str(title))
        axes.grid(grid)

        return plt.show()

    def dragvsvelocity(self, drag, minv, maxv, incr=0.1, linecolor='b', lw=2, grid=True, title='Drag vs Velocity'):

        v = np.arange(minv, maxv, incr)

        fig, axes = plt.subplots()
        fig.canvas.set_window_title(str(title))
        axes.plot(v, drag, color=str(linecolor), lw=int(lw))
        axes.set(xlabel='Velocity', ylabel='Drag (N)', title=str(title))
        axes.grid(grid)

        return plt.show()

    def thrust2weightvswingloading(self, thrust2weight, wingloading, minv, maxv, incr=0.1, thrust2weight_linecolor='b', wingloading_linecolor='r', lw=2, grid=True, title='Thrust-to-weight Ratio vs Wing Loading'):

        v = np.arange(minv, maxv, incr)

        fig, axes = plt.subplots()
        fig.canvas.set_window_title(str(title))
        axes.plot(v, thrust2weight, color=str(thrust2weight_linecolor), lw=int(lw), label='Thrust-to-weight Ratio')
        plt.axvline(x=wingloading, label='Wing Loading', color=str(wingloading_linecolor), lw=int(lw))
        plt.xticks([])
        plt.yticks([])
        axes.set(xlabel='Wing Loading', ylabel='Thrust-to-weight Ratio', title=str(title))
        axes.grid(grid)
        axes.legend(loc='best')

        return plt.show()

    def lift2dragvsvelocity(self, ltod, minv, maxv, incr=0.1, linecolor='b', lw=2, grid=True, title='Lift-to-drag Ratio vs Velocity'):

        v = np.arange(minv, maxv, incr)

        fig, axes = plt.subplots()
        fig.canvas.set_window_title(str(title))
        axes.plot(v, ltod, color=str(linecolor), lw=int(lw))
        axes.set(xlabel='Velocity', ylabel='Lift-to-drag Ratio', title=str(title))
        axes.grid(grid)

        return plt.show()

    def thrustavailablevsthrustrequired(self, thrustavailable, thrustrequired, minv, maxv, incr=0.1, thrustrequired_linecolor='b', thrustavailable_linecolor='r', lw=2, grid=True, title='Thrust Available vs Thrust Required'):

        v = np.arange(minv, maxv, incr)

        fig, axes = plt.subplots()
        fig.canvas.set_window_title(str(title))
        axes.plot(v, thrustrequired, color=str(thrustrequired_linecolor), lw=int(lw), label='Thrust Required')
        plt.axhline(y=thrustavailable, label='Thrust Available', color=str(thrustavailable_linecolor), lw=int(lw))
        axes.set(xlabel='Velocity', ylabel='Thrust Force (N)', title=str(title))
        axes.grid(grid)
        axes.legend(loc='best')

        return plt.show()
