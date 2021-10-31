import numpy as np
from math import pi

g = 9.81


class Calculate:

    def __init__(self):
        super(Calculate, self).__init__()

    def wingLoading(self, weight, wingarea):

        return weight/wingarea

    def aspectRatio(self, wingspan, wingarea):

        return (wingspan**2)/wingarea

    def oef_estimate(self, wingspan, wingarea):

        ar = (wingspan**2)/wingarea

        return 1.78*(1 - 0.045*ar**0.68) - 0.64

    def kFactor(self, wingspan, wingarea, oef):

        ar = (wingspan**2)/wingarea

        return float(1/(pi*ar*oef))

    def dragcoefficient(self, cd0, k, cl):

        return cd0 + k*cl**2

    def liftcoefficient(self, minv, maxv, weight, wingarea, rho, inc=0.1):

        v = np.arange(minv, maxv, inc)

        return (2*weight*g)/(rho*wingarea*v**2)

    def liftcoefficient_C(self, v, weight, wingarea, rho):

        return (2*weight*g)/(rho*wingarea*v**2)

    def drag(self, minv, maxv, wingarea, rho, cd, inc=0.1):

        v = np.arange(minv, maxv, inc)

        return 0.5*wingarea*rho*cd*v**2

    def thrustReq(self, minv, maxv, wingarea, rho, cd, inc=0.1):

        v = np.arange(minv, maxv, inc)

        return 0.5*wingarea*rho*cd*v**2

    def thrustReq_C(self, v, wingarea, rho, cd):

        return 0.5*wingarea*rho*cd*v**2

    def powerReq(self, minv, maxv, wingarea, rho, cd, inc=0.1):

        v = np.arange(minv, maxv, inc)

        return 0.5*wingarea*rho*cd*v**3

    def powerReq_C(self, v, wingarea, rho, cd):

        return 0.5*wingarea*rho*cd*v**3

    def takeoffDistance(self, weight, wingspan, wingarea, rho, cd0, rfriction_coef, availthrust, max_cl, oef):

        ar = (wingspan**2)/wingarea
        v_stall = (2*weight*g/(rho*wingarea*max_cl))**0.5
        v_lo_ave = 1.2*(0.7*v_stall)
        k = 1/(pi*ar*oef)
        cd = cd0 + k*max_cl**2
        drag = 0.5*rho*wingarea*cd*v_lo_ave**2
        lift = 0.5*rho*wingarea*max_cl*v_lo_ave**2

        f_eff = availthrust - (drag + rfriction_coef*(weight - lift))

        return (1.44*(g*weight)**2)/(g*rho*wingarea*max_cl*f_eff)

    def takeoffSpeed(self, weight, wingarea, rho, max_cl):

        v_stall = (2*weight*g/(rho*wingarea*max_cl))**0.5

        return 1.2*v_stall

    def landingDistance(self, weight, wingspan, wingarea, rho, cd0, rfriction_coef, max_cl):

        ar = (wingspan**2)/wingarea
        v_stall = (2*weight*g/(rho*wingarea*max_cl))**0.5
        v_td_ave = 0.7*(1.3*v_stall)
        oef = 1.78*(1 - 0.045*ar**0.68) - 0.64
        k = 1/(pi*ar*oef)
        cd = cd0 + k*max_cl**2
        drag = 0.5*rho*wingarea*cd*v_td_ave**2
        lift = 0.5*rho*wingarea*max_cl*v_td_ave**2

        f_eff = (drag + rfriction_coef*(g*weight - lift))

        return (1.69*(g*weight)**2)/(g*rho*wingarea*max_cl*f_eff)

    def landingSpeed(self, weight, wingarea, rho, max_cl):

        v_stall = (2*weight*g/(rho*wingarea*max_cl))**0.5

        return 1.3*v_stall

