import numpy as np
from math import pi
from math import sqrt
from math import log

g = 9.81


class Calculate:

    def __init__(self):
        super(Calculate, self).__init__()

        #####################
        # Setting flag for aircraft type #
        self.AIRCRAFT_TYPE_JET = "Jet"
        self.AIRCRAFT_TYPE_PROPELLER = "Propeller"

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

        return (1.3*v_stall)

    def breguet_range(self, ac_type, cl, cd, rho, weight, fuel, wingarea, sfc, prop_eff=0):

        if ac_type == self.AIRCRAFT_TYPE_JET:
            sfc_conv = sfc / 1000000
            range_numerator = 2 * sqrt(2) * sqrt(cl) * (sqrt(weight) - sqrt(weight - fuel))
            range_denominator = sfc_conv * cd * sqrt((rho * wingarea))
            range = range_numerator / range_denominator
            return (range/1000)
        else:
            sfc_conv = sfc / (1000*3600*1000)
            range = ((prop_eff / 100) * cl * log(weight / (weight - fuel))) / (sfc_conv * cd * 1000)
            return range

    def breguet_endurance(self, ac_type, cl, cd, rho, weight, fuel, sfc, wingarea, prop_eff=0):

        if ac_type == self.AIRCRAFT_TYPE_JET:
            sfc_conv = sfc / 1000000
            endurance = (cl * log(weight / (weight - fuel))) / (sfc_conv * cd)
            return (endurance/3600)
        else:
            sfc_conv = sfc / (1000*3600*1000)
            weight_factor = ((1/sqrt(weight - fuel))-(1/sqrt(weight)))
            endurance_numerator = weight_factor * (prop_eff / 100) * sqrt(2 * rho * wingarea) * sqrt(cl**3)
            endurance_denominator = sfc_conv * cd
            endurance = endurance_numerator / endurance_denominator
            return (endurance/3600)
