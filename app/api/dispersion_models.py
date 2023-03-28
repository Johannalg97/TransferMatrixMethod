from app.api.utils import get_nk_from_dielectric_fuction


class DispersionModels(object):
    """This class implements the main dispersion models"""

    def __init__(self, parameters):

        self.electron_charge = 1.602176634e-19  # in coulombs
        self.electron_mass = 9.10938356e-31  # in kilograms
        self.permitivitty_vacuum = 8.8541878128e-12  # in  F/m
        self.parameters = parameters
        # Lorenz :[electrons_per_unit, omega_0, omega, damping_coefficient]
        # Drude [electrons_per_unit, epsilon_infinito, omega, damping_coefficient]
        # Sellmeier [A, B, C, wavelength]

    def get_lorenz_model(self):
        """
        This method:
        *Calculates the epsilon_1 and epsilon_2 values of the dielectric function using the lorenz model
        *Receives a list of all parameters entered by the user
        * Return epsilon_1 and epsilon_2
        """
        a = (self.electron_charge**2 * self.parameters[0]) / (
            self.permitivitty_vacuum * self.electron_mass
        )
        b = self.parameters[1] ** 2 - self.parameters[2] ** 2
        c = self.parameters[3] * self.parameters[2]

        epsilon_1 = 1 + (a * ((b) / (b**2 + c**2)))
        epsilon_2 = a * ((c) / (b**2 + c**2))
        n_k = get_nk_from_dielectric_fuction(epsilon_1, epsilon_2)
        return n_k

    def get_drude_model(self):
        """
        This method:
        *Calculates the epsilon_1 and epsilon_2 values of the dielectric function using the drude model
        *Receives a list of all parameters entered by the user
        * Return epsilon_1 and epsilon_2
        """
        a = (self.electron_charge**2 * self.parameters[0]) / (
            self.permitivitty_vacuum * self.electron_mass
        )
        b = a * self.parameters[3]
        c = self.parameters[2] ** 2 + self.parameters[3] ** 2

        epsilon_1 = self.parameters[1] - ((a) / (c))
        epsilon_2 = (b) / (self.parameters[2] * c)
        n_k = get_nk_from_dielectric_fuction(epsilon_1, epsilon_2)
        return n_k

    def get_sellmeier_model(self):
        """
        This method:
        *Calculates the epsilon_1 and epsilon_2 values of the dielectric function using the Sellmeier model
        *Receives a list of all parameters entered by the user
        * Return epsilon_1 and epsilon_2
        """
        a = self.parameters[1] * self.parameters[2] ** 2
        b = self.parameters[2] ** 2 - self.parameters[3] ** 2

        epsilon_1 = self.parameters[0] + (a / b)
        epsilon_2 = 0
        n_k = get_nk_from_dielectric_fuction(epsilon_1, epsilon_2)
        return n_k

    def get_cauchy_model(self):
        """
        This method:
        *Calculates the epsilon_1 and epsilon_2 values of the dielectric function using the cauchy model
        *Receives a list of all parameters entered by the user
        * Return n and k
        """
        a = self.parameters[1] / self.parameters[3] ** 2
        b = self.parameters[2] / self.parameters[3]

        n = self.parameters[0] + a + b
        k = 0
        return complex(n, k)
