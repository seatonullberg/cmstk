import numpy as np
import copy


class UnitCell(object):

    def __init__(self, a0, atoms=[], basis_vectors=None):
        assert type(a0) is float
        self.a0 = a0
        assert type(atoms) is list
        self._atoms = atoms
        self._basis_vectors = basis_vectors

    ################
    #  Properties  #
    ################

    @property
    def basis_vectors(self):
        if self._basis_vectors is None:
            return np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        else:
            return copy.deepcopy(self._basis_vectors)

    @basis_vectors.setter
    def basis_vectors(self, vecs):
        # check type
        if not isinstance(vecs, np.ndarray):
            raise TypeError("`vecs` must be instance of type np.ndarray")
        # check shape
        nrows, ncols = vecs.shape
        if not nrows == ncols == 3:
            raise ValueError("`vecs` should be a 3x3 matrix")
        self._basis_vectors = vecs

    @property
    def atoms(self):
        yield copy.deepcopy(self._atoms)

    @atoms.setter
    def atoms(self):
        raise RuntimeError("`atoms` is a read-only attribute")

    ######################
    #  External Methods  #
    ######################

    def add_atom(self, atom):
        # add an Atom object to self._atoms
        pass

    def remove_atom(self, miller_position):
        # remove an Atom object from self._atoms
        pass

    def atoms_absolute(self):
        # convert the miller indices of atoms in self._atoms
        # to absolute distances based on self.a0
        pass


class FaceCenteredCubic(UnitCell):

    def __init__(self, a0, atoms=[], basis_vectors=None):
        super().__init__(a0=a0, atoms=atoms, basis_vectors=basis_vectors)

    ################
    #  Properties  #
    ################

    @property
    def lattice_sites(self):
        # the miller indices of all possible lattice sites
        pass

    @lattice_sites.setter
    def lattice_sites(self):
        raise RuntimeError("`lattice_sites` is a read-only attribute")
       
    @property
    def tetrahedral_sites(self):
        # the miller indices of all possible tetrahedral sites
        pass

    @tetrahedral_sites.setter
    def tetrahedral_sites(self):
        raise RuntimeError("`tetrahedral_sites` is a read-only attribute")

    @property
    def octahedral_sites(self):
        # the miller indices of all possible octahedral sites
        pass

    @octahedral_sites.setter
    def octahedral_sites(self):
        raise RuntimeError("`octahedral_sites` is a read-only attribute")


class BodyCenteredCubic(UnitCell):

    def __init__(self, a0, atoms=[], basis_vectors=None):
        super().__init__(a0=a0, atoms=atoms, basis_vectors=basis_vectors)

    ################
    #  Properties  #
    ################

    @property
    def lattice_sites(self):
        # the miller indices of all possible lattice sites
        pass

    @lattice_sites.setter
    def lattice_sites(self):
        raise RuntimeError("`lattice_sites` is a read-only attribute")
       
    @property
    def tetrahedral_sites(self):
        # the miller indices of all possible tetrahedral sites
        pass

    @tetrahedral_sites.setter
    def tetrahedral_sites(self):
        raise RuntimeError("`tetrahedral_sites` is a read-only attribute")

    @property
    def octahedral_sites(self):
        # the miller indices of all possible octahedral sites
        pass

    @octahedral_sites.setter
    def octahedral_sites(self):
        raise RuntimeError("`octahedral_sites` is a read-only attribute")


class SimpleCubic(UnitCell):

    def __init__(self, a0, atoms=[], basis_vectors=None):
        super().__init__(a0=a0, atoms=atoms, basis_vectors=basis_vectors)

    ################
    #  Properties  #
    ################

    @property
    def lattice_sites(self):
        # the miller indices of all possible lattice sites
        pass

    @lattice_sites.setter
    def lattice_sites(self):
        raise RuntimeError("`lattice_sites` is a read-only attribute")
       
    @property
    def tetrahedral_sites(self):
        # the miller indices of all possible tetrahedral sites
        pass

    @tetrahedral_sites.setter
    def tetrahedral_sites(self):
        raise RuntimeError("`tetrahedral_sites` is a read-only attribute")

    @property
    def octahedral_sites(self):
        # the miller indices of all possible octahedral sites
        pass

    @octahedral_sites.setter
    def octahedral_sites(self):
        raise RuntimeError("`octahedral_sites` is a read-only attribute")

