import numpy as np
from math import pi

GRAVITY = 9.81

def wing_loading(weight: float, wing_area: float) -> float:
    """Calculates Wing Loading.
    
    Args:
        weight: Aircraft weight (N or kg force depending on context, assuming consistent units)
        wing_area: Wing area (m^2)
        
    Returns:
        Wing loading value.
    """
    return weight / wing_area

def aspect_ratio(wingspan: float, wing_area: float) -> float:
    """Calculates Aspect Ratio."""
    return (wingspan**2) / wing_area

def oswald_efficiency_estimate(aspect_ratio_val: float) -> float:
    """Estimates Oswald Efficiency Factor based on Aspect Ratio."""
    return 1.78 * (1 - 0.045 * aspect_ratio_val**0.68) - 0.64

def k_factor(aspect_ratio_val: float, oswald_eff: float) -> float:
    """Calculates K factor (Induced Drag Factor)."""
    return 1.0 / (pi * aspect_ratio_val * oswald_eff)

def drag_coefficient(cd0: float, k: float, cl: float | np.ndarray) -> float | np.ndarray:
    """Calculates Drag Coefficient (Cd)."""
    return cd0 + k * cl**2

def lift_coefficient_range(min_v: float, max_v: float, weight: float, wing_area: float, rho: float, inc: float = 0.1) -> np.ndarray:
    """Calculates Lift Coefficient (Cl) for a range of velocities."""
    v = np.arange(min_v, max_v, inc)
    # Avoid division by zero if v usually starts > 0, but good to be safe with numpy handling
    return (2 * weight * GRAVITY) / (rho * wing_area * v**2)

def lift_coefficient_at_v(v: float, weight: float, wing_area: float, rho: float) -> float:
    """Calculates Lift Coefficient (Cl) at a specific velocity."""
    return (2 * weight * GRAVITY) / (rho * wing_area * v**2)

def drag_range(min_v: float, max_v: float, wing_area: float, rho: float, cd: np.ndarray | float, inc: float = 0.1) -> np.ndarray:
    """Calculates Drag force for a range of velocities."""
    v = np.arange(min_v, max_v, inc)
    return 0.5 * wing_area * rho * cd * v**2

def thrust_required_range(min_v: float, max_v: float, wing_area: float, rho: float, cd: np.ndarray | float, inc: float = 0.1) -> np.ndarray:
    """Calculates Thrust Required for a range of velocities."""
    return drag_range(min_v, max_v, wing_area, rho, cd, inc)

def thrust_required_at_v(v: float, wing_area: float, rho: float, cd: float) -> float:
    """Calculates Thrust Required at a specific velocity."""
    return 0.5 * wing_area * rho * cd * v**2

def power_required_range(min_v: float, max_v: float, wing_area: float, rho: float, cd: np.ndarray | float, inc: float = 0.1) -> np.ndarray:
    """Calculates Power Required for a range of velocities."""
    v = np.arange(min_v, max_v, inc)
    return 0.5 * wing_area * rho * cd * v**3

def power_required_at_v(v: float, wing_area: float, rho: float, cd: float) -> float:
    """Calculates Power Required at a specific velocity."""
    return 0.5 * wing_area * rho * cd * v**3

def takeoff_distance(weight: float, wingspan: float, wing_area: float, rho: float, cd0: float, 
                     friction_coef: float, available_thrust: float, max_cl: float, oef: float) -> float:
    """Calculates Takeoff Distance."""
    ar = aspect_ratio(wingspan, wing_area)
    # Stall speed
    v_stall = (2 * weight * GRAVITY / (rho * wing_area * max_cl))**0.5
    # Average liftoff speed
    v_lo_ave = 1.2 * (0.7 * v_stall)
    
    k = k_factor(ar, oef)
    cd = drag_coefficient(cd0, k, max_cl)
    
    drag = 0.5 * rho * wing_area * cd * v_lo_ave**2
    lift = 0.5 * rho * wing_area * max_cl * v_lo_ave**2
    
    # Effective force
    f_eff = available_thrust - (drag + friction_coef * (weight - lift))
    
    return (1.44 * (GRAVITY * weight)**2) / (GRAVITY * rho * wing_area * max_cl * f_eff)

def takeoff_speed(weight: float, wing_area: float, rho: float, max_cl: float) -> float:
    """Calculates Takeoff Speed."""
    v_stall = (2 * weight * GRAVITY / (rho * wing_area * max_cl))**0.5
    return 1.2 * v_stall

def landing_distance(weight: float, wingspan: float, wing_area: float, rho: float, cd0: float, 
                     friction_coef: float, max_cl: float) -> float:
    """Calculates Landing Distance."""
    ar = aspect_ratio(wingspan, wing_area)
    v_stall = (2 * weight * GRAVITY / (rho * wing_area * max_cl))**0.5
    v_td_ave = 0.7 * (1.3 * v_stall)
    
    o_eff = oswald_efficiency_estimate(ar)
    k = k_factor(ar, o_eff)
    cd = drag_coefficient(cd0, k, max_cl)
    
    drag = 0.5 * rho * wing_area * cd * v_td_ave**2
    lift = 0.5 * rho * wing_area * max_cl * v_td_ave**2
    
    f_eff = (drag + friction_coef * (GRAVITY * weight - lift))
    
    return (1.69 * (GRAVITY * weight)**2) / (GRAVITY * rho * wing_area * max_cl * f_eff)

def landing_speed(weight: float, wing_area: float, rho: float, max_cl: float) -> float:
    """Calculates Landing Speed."""
    v_stall = (2 * weight * GRAVITY / (rho * wing_area * max_cl))**0.5
    return 1.3 * v_stall
