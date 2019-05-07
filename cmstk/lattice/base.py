import math
import type_sanity as ts
from cmstk.data import ElementsReader
from cmstk.lattice.exceptions import AtomicPositionError
from cmstk.lattice.test_types_pb2 import ProtoAtom, ProtoLattice
from cmstk.units.base import BaseScheme
from cmstk.units.distance import DistanceUnit, Picometer
from cmstk.units.angle import AngleUnit, Radian
from cmstk.units.vector import Vector3D
from cmstk.units.charge import ChargeUnit
from cmstk.units.speed import SpeedUnit
from cmstk.units.mass import MassUnit


# TODO: this should be modified to return a generalized DistanceUnit
def separation_distance(p1, p2):
    """Returns the separation distance between two positions.

    Args:
        p1 (Vector3D): The first position.
        p2 (Vector3D): the second position.

    Returns:
        Picometer
    """
    pico_x1, pico_x2 = p1[0].to(Picometer), p2[0].to(Picometer)
    pico_y1, pico_y2 = p1[1].to(Picometer), p2[1].to(Picometer)
    pico_z1, pico_z2 = p1[2].to(Picometer), p2[2].to(Picometer)
    # use .value because squaring would throw conversion error
    distance = math.sqrt((pico_x1-pico_x2).value**2 + (pico_y1-pico_y2).value**2 + (pico_z1-pico_z2).value**2)
    return Picometer(distance)


class Atom(object):
    """Representation of an atom in space.
    
    Args:
        symbol (str): IUPAC chemical symbol.
        position (Vector3D): (x, y, z) spatial coordinates.
        charge (optional) (ChargeUnit): Electric charge of the atom.
        velocity (optional) (Vector3D of SpeedUnit): (x, y, z) velocity. 

    Attributes:
        symbol (str): IUPAC chemical symbol.
        position (Vector3D): (x, y, z) spatial coordinates.
        charge (ChargeUnit): Electric charge of the atom.
        velocity (Vector3D of SpeedUnit): (x, y, z) velocity.
    """

    def __init__(self, symbol, position, charge=None, velocity=None):
        ts.is_type((symbol, str, "symbol"), (position, Vector3D, "position"))
        if position.unit_kind is not DistanceUnit:
            raise TypeError("`position` must contain units of kind DistanceUnit")
        ts.is_instance_any((charge, [type(None), ChargeUnit], "charge"))
        if charge is None:
            charge = ChargeUnit(0.0)
        ts.is_type_any((velocity, [type(None), Vector3D], "velocity"))
        if velocity is None:
            velocity = (SpeedUnit(0.0), SpeedUnit(0.0), SpeedUnit(0.0))
            velocity = Vector3D(velocity)
        if velocity.unit_kind is not SpeedUnit:
            raise TypeError("`velocity` must contain units of kind SpeedUnit")

        self.symbol = symbol
        self.position = position
        self.charge = charge
        self.velocity = velocity
        self._elements_reader = ElementsReader() # store this for easy access in properties

    @property
    def atomic_radius(self):
        """Returns the Atom's radius as described in elements.json.
        
        Returns:
            Picometer
        """
        return self._elements_reader.atomic_radius(self.symbol)

    @property
    def atomic_weight(self):
        """Returns the Atom's mass as described in elements.json.

        Returns:
            AtomicMassUnit
        """
        return self._elements_reader.atomic_weight(self.symbol)

    @property
    def covalent_radius(self):
        """Returns the Atom's covalent radius as described in elements.json.
        
        Returns:
            Picometer
        """
        return self._elements_reader.covalent_radius(self.symbol)

    @property
    def crystal_structure(self):
        """Returns the Atom's crystal structure as described in elements.json.
        
        Returns:
            str
        """
        return self._elements_reader.crystal_structure(self.symbol)

    @property
    def lattice_constants(self):
        """Returns the Atom's lattice constants as described in elements.json.
        
        Returns:
            tuple of Picometer
        """
        return self._elements_reader.lattice_constants(self.symbol)


class Lattice(object):
    """Representation of a crystalline lattice.

    Args:
        atoms (list of Atom): Collection of atoms in the lattice.
    """

    # TODO: weird bug where if i initialize this as an empty list it fails to make structures
    def __init__(self, atoms=None):
        #ts.is_type((atoms, list, "atoms"))
        if atoms is None:
            atoms = []
        if type(atoms) is not list:
            raise TypeError("`atoms` must be of type list")
        for a in atoms:
            if type(a) is not Atom:
                raise TypeError("all members of list `atoms` must be of type Atom")

        self._atoms = atoms

    ################
    #  Properties  #
    ################

    @property
    def atoms(self):
        """Returns a generator of all atoms."""
        for a in self._atoms:
            yield a

    @property
    def n_atoms(self):
        """Returns the number of atoms."""
        return len(self._atoms)

    @property
    def symbols(self):
        """Returns a set of all atomic symbols."""
        syms = set()
        for a in self.atoms:
            syms.add(a.symbol)
        return syms

    @property
    def n_symbols(self):
        """Returns the number of atomic symbols."""
        return len(self.symbols)

    @property
    def bounding_box(self):
        """Returns the bounding dimensions of the lattice."""
        max_ = [DistanceUnit(-math.inf), DistanceUnit(-math.inf), DistanceUnit(-math.inf)]
        min_ = [DistanceUnit(math.inf), DistanceUnit(math.inf), DistanceUnit(math.inf)]
        for a in self.atoms:
            for i, val in enumerate(a.position):
                if val.compare_gt(max_[i]):
                    max_[i] = val
                if val.compare_lt(min_[i]):
                    min_[i] = val
        return {"max_x": max_[0], "max_y": max_[1], "max_z": max_[2],
                "min_x": min_[0], "min_y": min_[1], "min_z": min_[2]}

    #######################
    #  Atomic Operations  #
    #######################

    def add_atom(self, atom, tolerance=None):
        """Adds an atom to the lattice if the position is not already occupied.

        Args:
            atom (Atom): The atom to add.
            tolerance (optional) (DistanceUnit): Minimum separation distance for valid addition.
            - `tolerance` defaults to the covalent radius of `atom` plus that of its nearest neighbor.
        
        Raises:
            AtomicPositionError - If an atom already exists in the given position.
        """
        ts.is_type((atom, Atom, "atom"))
        if tolerance is not None:
            ts.is_instance((tolerance, DistanceUnit, "tolerance"))

        for a in self.atoms:
            if tolerance is None:
                minimum_separation = a.covalent_radius + atom.covalent_radius
            else:
                minimum_separation = tolerance.to(Picometer)
            actual_separation = separation_distance(a.position, atom.position)
            if actual_separation < minimum_separation:
                raise AtomicPositionError(position=atom.position, exists=True)
        self._atoms.append(atom)

    def remove_atom(self, position, tolerance=None):
        """Removes an atom if the position is occupied.
        
        Args:
            position (Vector3D): Verified (x, y, z) spatial coordinates.
            tolerance (optional) (DistanceUnit): Maximum separation distance from another atomic center for valid removal.
            - `tolerance` defaults to the covalent radius of `atom`'s nearest neighbor.
        
        Raises:
            AtomicPositionError - If an atom does not exist in the given position.
        """
        ts.is_type((position, Vector3D, "position"))
        if position.unit_kind is not DistanceUnit:
            raise TypeError("`position` must contain units of kind DistanceUnit")
        if tolerance is not None:
            ts.is_instance((tolerance, DistanceUnit, "tolerance"))

        for i, a in enumerate(self._atoms):  # iterate over the actual list because it may be modified intermediately
            if tolerance is None:
                maximum_separation = a.covalent_radius
            else:
                maximum_separation = tolerance.to(Picometer)

            separation = separation_distance(position, a.position)
            if separation < maximum_separation:
                del self._atoms[i]
                return
        raise AtomicPositionError(position=position, exists=False)

    # TODO
    ########################
    #  Lattice Operations  #
    ########################

    def repeat(self, dims):
        """Repeat the lattice in 3 dimensions.
    
        Args:
            dims (tuple of ints): The number of times to repeat in each direction (x, y, z).
        """
        ts.is_type((dims, tuple, "dims"))
        if len(dims) != 3:
            raise ValueError("`dims` must have length 3")
        for d in dims:
            ts.is_type((d, int))
        raise NotImplementedError

    def rotate(self, angles):
        """Rotate the lattice in 3 dimensions.

        Args:
            angles (Vector3D of AngleUnits): Angles to rotate the lattice by in (x, y, z).
        """
        ts.is_type((angles, Vector3D, "angles"))
        if angles.unit_kind is not AngleUnit:
            raise TypeError("`angles` must contain units of kind AngleUnits")
        for a in self.atoms:
            a.position.rotate(angles)

    def translate(self, dims):
        """Translate the lattice in 3 dimensions.

        Args:
            dims (Vector3D of DistanceUnit): The distance to translate the lattice by in (x, y, z).
            - Here the Vector3D functions not as a point in space but a translation factor to move all atoms by.
            - This prevents having to do the type checking on a tuple of DistanceUnits which is already handled by Vector3D.
        """
        ts.is_type((dims, Vector3D, "dims"))
        if dims.unit_kind is not DistanceUnit:
            raise TypeError("`position` must contain units of kind DistanceUnit")
        for a in self.atoms:
            a.position.translate(dims)

    ####################
    #  I/O Operations  #
    ####################

    # LAMMPS format from here: https://lammps.sandia.gov/doc/2001/data_format.html

    @classmethod
    def from_lammps(cls, path, unit_scheme, symbols):
        ts.is_type((path, str, "path"), (symbols, dict, "symbols"))
        ts.is_instance((unit_scheme, BaseScheme, "unit_scheme"))
        for k, v in symbols.items():
            ts.is_type((k, int), (v, str))

        with open(path, "r") as f:
            lines = f.readlines()
        atoms = []
        for i, line in enumerate(lines[2:]):  # always skip first 2 lines
            line = line.strip()
            if line == "Atoms":
                for line in lines[i+3:]:  # go to the next line and iterate
                    if line[0].isupper():
                        break
                    parts = line.split()
                    if len(parts) == 0:
                        continue
                    atom_type = int(float(parts[1]))
                    symbol = symbols[atom_type]  # get str symbol
                    charge = float(parts[2])
                    charge = unit_scheme[ChargeUnit](charge)
                    x, y, z = float(parts[3]), float(parts[4]), float(parts[5])
                    _type = unit_scheme[DistanceUnit]
                    position = (_type(x), _type(y), _type(z))
                    position = Vector3D(position)
                    atom = Atom(symbol=symbol, position=position, charge=charge)
                    atoms.append(atom)
            if line == "Velocities":
                for line in lines[i+3]:
                    if line[0].isupper():
                        break
                    parts = line.split()
                    if len(parts) == 0:
                        continue
                    index = parts[0]
                    vx, vy, vz = parts[1], parts[2], parts[3]
                    _type = unit_scheme[SpeedUnit]
                    velocity = (_type(vx), _type(vy), _type(vz))
                    velocity = Vector3D(velocity)
                    try:
                        atoms[index].velocity = velocity
                    except IndexError:
                        raise IndexError("index unavailable because `Velocities` was parsed before `Atoms`")
        return cls(atoms)

    def to_lammps(self, path, unit_scheme):
        ts.is_instance((path, str, "path"), (unit_scheme, BaseScheme, "unit_scheme"))
        dims = self.bounding_box
        for k, v in dims.items():
            dims[k] = v.to(unit_scheme[DistanceUnit])
        atom_types = {sym: i for i, sym in enumerate(self.symbols)}
        reader = ElementsReader()
        with open(path, "w") as f:
            f.write("Automatically generated by cmstk: https://github.com/seatonullberg/cmstk\n\n")
            f.write("{} atoms\n".format(self.n_atoms))
            f.write("{} atom types\n".format(self.n_symbols))
            f.write("{} {} xlo xhi\n".format(dims["min_x"].value, dims["max_x"].value))
            f.write("{} {} ylo yhi\n".format(dims["min_y"].value, dims["max_y"].value))
            f.write("{} {} zlo zhi\n".format(dims["min_z"].value, dims["max_z"].value))
            f.write("\nMasses\n\n")
            for i, sym in enumerate(self.symbols):
                mass = reader.atomic_weight(sym)
                mass = mass.to(unit_scheme[MassUnit])
                f.write("\t{} {}\n".format(i, mass.value))
            f.write("\nAtoms\n\n")
            for i, atom in enumerate(self.atoms):
                charge = atom.charge.to(unit_scheme[ChargeUnit]).value
                x = atom.position[0].to(unit_scheme[DistanceUnit]).value
                y = atom.position[1].to(unit_scheme[DistanceUnit]).value
                z = atom.position[2].to(unit_scheme[DistanceUnit]).value
                f.write("\t {index} {atom_type} {charge} {x} {y} {z}\n".format(index=i,
                                                                               atom_type=atom_types[atom.symbol],
                                                                               charge=charge,
                                                                               x=x, y=y, z=z))
            f.write("\nVelocities\n\n")
            for i, atom in enumerate(self.atoms):
                vx = atom.velocity[0].to(unit_scheme[SpeedUnit]).value
                vy = atom.velocity[1].to(unit_scheme[SpeedUnit]).value
                vz = atom.velocity[2].to(unit_scheme[SpeedUnit]).value
                f.write("\t {index} {atom_type} {vx} {vy} {vz}\n".format(index=i,
                                                                         atom_type=atom_types[atom.symbol],
                                                                         vx=vx,vy=vy, vz=vz))

    @classmethod
    def from_proto(cls, path):
        """Initializes a Lattice from a protobuffer file.

        Args:
            path (str): Path to the protobuffer file.

        Returns:
            Lattice
        """
        ts.is_type((path, str, "path"))
        proto_lattice = ProtoLattice()
        with open(path, "rb") as f:
            proto_lattice.ParseFromString(f.read())
        atoms = []
        for a in proto_lattice.atoms:
            pos = (Picometer(a.x), Picometer(a.y), Picometer(a.z))
            pos = Vector3D(pos)
            chg = a.charge
            chg = ChargeUnit(chg)
            vel = (SpeedUnit(a.vx), SpeedUnit(a.vy), SpeedUnit(a.vz))
            vel = Vector3D(vel)
            atom = Atom(symbol=a.symbol, position=pos, charge=chg, velocity=vel)
            atoms.append(atom)
        return cls(atoms)

    def to_proto(self, path):
        """Writes a Lattice to a protobuffer file.
        
        Args:
            path (str): Path to the protobuffer file.
        """
        ts.is_type((path, str, "path"))
        proto_atoms = []
        for a in self.atoms:
            proto_atom = ProtoAtom(
                x=a.position[0],
                y=a.position[1],
                z=a.position[2],
                radius=a.atomic_radius,
                symbol=a.symbol,
                vx=a.velocity[0],
                vy=a.velocity[1],
                vz=a.velocity[2],
                charge=a.charge
            )
            proto_atoms.append(proto_atom)
        proto_lattice = ProtoLattice(atoms=proto_atoms)
        with open(path, "wb") as f:
            f.write(proto_lattice.SerializeToString())

    @classmethod
    def from_vasp(cls, path):
        raise NotImplementedError

    def to_vasp(self, path):
        raise NotImplementedError
