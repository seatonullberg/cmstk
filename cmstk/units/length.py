from base import BaseUnit


class Angstrom(BaseUnit, float):

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")
        
        self.value = value        
        self.unit_name = "angstrom"
        super().__init__(value=self.value, unit_name=self.unit_name)
        
    def to_nanometer(self):
        new_value = self.value * 0.1
        return Nanometer(new_value)

    def to_picometer(self):
        new_value = self.value * 100.0
        return Picometer(new_value)


class Nanometer(BaseUnit, float):

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")
        
        self.value = value        
        self.unit_name = "nanometer"
        super().__init__(value=self.value, unit_name=self.unit_name)
        
    def to_angstrom(self):
        new_value = self.value * 10.0
        return Angstrom(new_value)

    def to_picometer(self):
        new_value = self.value * 1000.0
        return Picometer(new_value)


class Picometer(BaseUnit, float):

    def __init__(self, value):
        if type(value) is not float:
            raise TypeError("`value` must be of type float")
        
        self.value = value        
        self.unit_name = "picometer"
        super().__init__(value=self.value, unit_name=self.unit_name)
        
    def to_angstrom(self):
        new_value = self.value * 0.01
        return Angstrom(new_value)

    def to_nanometer(self):
        new_value = self.value * 0.001
        return Nanometer(new_value)

