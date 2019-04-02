

class Atom(object):

    def __init__(self, symbol, miller_position):
        # symbol should be an IUPAC element symbol
        assert type(symbol) is str
        self.symbol = symbol
        # miller_position should be the atom's lattice site in miller indices
        assert type(miller_position) is tuple
        self.miller_position = miller_position