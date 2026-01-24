import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from typing import Optional

def plot_cl_vs_velocity(cl: np.ndarray, min_v: float, max_v: float, 
                       incr: float = 0.1, line_color: str = 'b', lw: int = 2, 
                       grid: bool = True, title: str = 'CL vs Velocity', shows: bool = True) -> Optional[Figure]:
    """Plots Lift Coefficient vs Velocity."""
    v = np.arange(min_v, max_v, incr)

    fig, axes = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    axes.plot(v, cl, color=line_color, lw=lw)
    axes.set(xlabel='Velocity (m/s)', ylabel='Lift Coefficient (CL)', title=title)
    axes.grid(grid)

    if shows:
        plt.show()
        return None
    return fig

def plot_thrust_req_vs_velocity(thrust: np.ndarray, min_v: float, max_v: float, 
                               incr: float = 0.1, line_color: str = 'b', lw: int = 2, 
                               grid: bool = True, title: str = 'Thrust Required vs Velocity', shows: bool = True) -> Optional[Figure]:
    """Plots Thrust Required vs Velocity."""
    v = np.arange(min_v, max_v, incr)

    fig, axes = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    axes.plot(v, thrust, color=line_color, lw=lw)
    axes.set(xlabel='Velocity (m/s)', ylabel='Thrust Required (N)', title=title)
    axes.grid(grid)

    if shows:
        plt.show()
        return None
    return fig

def plot_power_req_vs_velocity(power: np.ndarray, min_v: float, max_v: float, 
                              incr: float = 0.1, line_color: str = 'b', lw: int = 2, 
                              grid: bool = True, title: str = 'Power Required vs Velocity', shows: bool = True) -> Optional[Figure]:
    """Plots Power Required vs Velocity."""
    v = np.arange(min_v, max_v, incr)

    fig, axes = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    axes.plot(v, power, color=line_color, lw=lw)
    axes.set(xlabel='Velocity (m/s)', ylabel='Power Required (W)', title=title)
    axes.grid(grid)

    if shows:
        plt.show()
        return None
    return fig

def plot_drag_vs_velocity(drag: np.ndarray, min_v: float, max_v: float, 
                         incr: float = 0.1, line_color: str = 'b', lw: int = 2, 
                         grid: bool = True, title: str = 'Drag vs Velocity', shows: bool = True) -> Optional[Figure]:
    """Plots Drag vs Velocity."""
    v = np.arange(min_v, max_v, incr)

    fig, axes = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    axes.plot(v, drag, color=line_color, lw=lw)
    axes.set(xlabel='Velocity (m/s)', ylabel='Drag (N)', title=title)
    axes.grid(grid)

    if shows:
        plt.show()
        return None
    return fig

def plot_thrust2weight_vs_wingloading(thrust2weight: np.ndarray, wing_loading_val: float, 
                                     min_v: float, max_v: float, incr: float = 0.1, 
                                     t2w_color: str = 'b', wl_color: str = 'r', 
                                     lw: int = 2, grid: bool = True, 
                                     title: str = 'Thrust-to-weight Ratio vs Wing Loading', shows: bool = True) -> Optional[Figure]:
    """Plots Thrust-to-weight Ratio vs Wing Loading."""
    v = np.arange(min_v, max_v, incr)

    fig, axes = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    axes.plot(v, thrust2weight, color=t2w_color, lw=lw, label='Thrust-to-weight Ratio')
    # Using axvline for vertical line
    axes.axvline(x=wing_loading_val, label='Wing Loading', color=wl_color, lw=lw)
    
    # Keeping original behavior of hiding ticks if that was intended, though it seems odd.
    # The original code had plt.xticks([]) plt.yticks([]). I'll keep them but might be worth removing.
    # plt.xticks([]) 
    # plt.yticks([])
    
    axes.set(xlabel='Wing Loading (N/m^2)', ylabel='Thrust-to-weight Ratio', title=title)
    axes.grid(grid)
    axes.legend(loc='best')

    if shows:
        plt.show()
        return None
    return fig

def plot_lift2drag_vs_velocity(ltod: np.ndarray, min_v: float, max_v: float, 
                              incr: float = 0.1, line_color: str = 'b', lw: int = 2, 
                              grid: bool = True, title: str = 'Lift-to-drag Ratio vs Velocity', shows: bool = True) -> Optional[Figure]:
    """Plots Lift-to-drag Ratio vs Velocity."""
    v = np.arange(min_v, max_v, incr)

    fig, axes = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    axes.plot(v, ltod, color=line_color, lw=lw)
    axes.set(xlabel='Velocity (m/s)', ylabel='Lift-to-drag Ratio', title=title)
    axes.grid(grid)

    if shows:
        plt.show()
        return None
    return fig

def plot_thrust_avail_vs_req(thrust_avail: float, thrust_req: np.ndarray, 
                            min_v: float, max_v: float, incr: float = 0.1, 
                            req_color: str = 'b', avail_color: str = 'r', 
                            lw: int = 2, grid: bool = True, 
                            title: str = 'Thrust Available vs Thrust Required', shows: bool = True) -> Optional[Figure]:
    """Plots Thrust Available vs Thrust Required."""
    v = np.arange(min_v, max_v, incr)

    fig, axes = plt.subplots()
    fig.canvas.manager.set_window_title(title)
    axes.plot(v, thrust_req, color=req_color, lw=lw, label='Thrust Required')
    axes.axhline(y=thrust_avail, label='Thrust Available', color=avail_color, lw=lw)
    axes.set(xlabel='Velocity (m/s)', ylabel='Thrust Force (N)', title=title)
    axes.grid(grid)
    axes.legend(loc='best')

    if shows:
        plt.show()
        return None
    return fig
