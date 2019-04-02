from exceptions import UnlikeUnitsError


class BaseUnit(object):

    def __init__(self, value, unit_name):
        self.value = value
        assert type(unit_name) is str
        self.unit_name = unit_name

    def __add__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="add", a=self.unit_name, b=other.unit_name)
        else:
            return self.value + other.value

    def __sub__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="subtract", a=self.unit_name, b=other.unit_name)
        else:
            return self.value - other.value

    def __mul__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="multiply", a=self.unit_name, b=other.unit_name)
        else:
            return self.value * other.value

    def __truediv__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="divide", a=self.unit_name, b=other.unit_name)
        else:
            return self.value / other.value

    def __floordiv__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="divide", a=self.unit_name, b=other.unit_name)
        else:
            return self.value // other.value

    def __mod__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="take remainder of", a=self.unit_name, b=other.unit_name)
        else:
            return self.value % other.value

    def __lt__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value < other.value

    def __le__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value <= other.value

    def __eq__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value == other.value

    def __ne__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value != other.value

    def __gt__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value > other.value

    def __ge__(self, other):
        if self.unit_name is not other.unit_name:
            raise UnlikeUnitsError(operation="compare", a=self.unit_name, b=other.unit_name)
        else:
            return self.value >= other.value