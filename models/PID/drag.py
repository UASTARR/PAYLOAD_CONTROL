
class Drag:
    def __init__(self, T_celsius=25.0, p_atm=101.325):
        # velocity u is constant at 120kph
        self.u = 120.0*1000.0/3600.0
        self.p = p_atm * 1000.0
        self.T_Kelvin = T_celsius + 273.15
        # https://en.wikipedia.org/wiki/Drag_coefficient - cube
        self.c_d = 1.05
        self.drag_cache = 0.5 * self.u * self.u * self.c_d

    def _density_dry(self):
        """ See: https://en.wikipedia.org/wiki/Density_of_air

        Keyword arguments:
        T_celsius -- temperature in Celsius
        p - pressure in Pascals

        rho = p/(R_specific T) = (pM)/(RT) = (pm)/(k_bT)

        where
        rho = air density (kg/m**3)
        p = absolute pressure (Pa)
        T = absolute temperature (K)
        R = gas constant, 8.314 462 618 153 24 J*K^-1*mol-1
        m = molecular mass of dry air, 4.81*10**-26 kg
        k_b = Boltzmann constant
        R_specific = specific gas constant for dry air, 287.050 0676 J*kg**-1*K**-1
        """
        R_specific = 287.0500676
        return self.p/(R_specific*self.T_Kelvin)

    def _density_humid(self, humidity):
        """ rho = p_d/(R_d T) + p_v/(R_v T)

        where
        p_v = phi*p_sat = relative humidity * saturation vapor pressure
        """
        R_d = 287.058
        R_v = 461.495
        p_sat = numpy.exp(0.61078, (17.27*T_kelvin)/(T_kelvin + 237.3))
        p_v = humidity*p_sat
        return p/(R_d*self.T_Kelvin) + p_v/(R_v*self.T_Kelvin)

    def drag(self, area):
        """From wikipedia (https://en.wikipedia.org/wiki/Drag_equation):

        F_d = 1/2 rho u**2 c_d A,

        where
        F_d = force of drag
        rho = density of air
        u = velocity
        A = area
        c_d = drag co-efficient
        """
        return self.drag_cache * self._density_dry() * area

    def area(self, F):
        """Given F_d, determine the area A that produced it

        F_d = 1/2 rho u**2 c_d A,

        A = F_d/(1/2 rho u**2 c_d)
        """
        return F/(self.drag_cache * self._density_dry())

if __name__ == "__main__":
    payload = Drag()
    A = 0.05*0.05  # 5 cm^2
    f = payload.drag(A)
    print("A {}, F {}", A, f) 
    a = payload.area(f)
    print("a {}, f {}", a, f)


    
