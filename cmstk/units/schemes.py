import type_sanity as ts
from cmstk.units import *

class SIScheme(BaseScheme):
    """Implementation of the SI units."""

    def __init__(self):
        units = {MassUnit: Kilogram, DistanceUnit: Meter, TimeUnit: Second,
                 EnergyUnit: Joule, SpeedUnit: MeterPerSecond, ForceUnit: Newton,
                 TemperatureUnit: Kelvin, PressureUnit: Pascal, ChargeUnit: Coulomb}
        super().__init__(units)


# TODO: add force `ElectronVoltPerAngstrom`
class MetalScheme(BaseScheme):
    """Implementation of the LAMMPS metal units."""

    def __init__(self):
        units = {MassUnit: AtomicMassUnit, DistanceUnit: Angstrom, TimeUnit: Picosecond,
                 EnergyUnit: ElectronVolt, SpeedUnit: AngstromPerPicosecond, TemperatureUnit: Kelvin,
                 PressureUnit: Bar, ChargeUnit: ElectronCharge}
        super().__init__(units)