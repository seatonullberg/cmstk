from cmstk.filetypes import TextFile
from cmstk.structure.atom import AtomCollection
import numpy as np

class XyzFile(TextFile):
    def __init__(self, filepath, comment, atom_collection):
        if filepath is None:
            filpath = "structure.xyz"

        if comment is None:
            comment = "comment.xyz"
        self._comment = comment
        self._atom_collection = atom_collection

        super().__init__(filepath)

        @property 
        def comment(self):
            if self._comment is None:
             self._comment = self.lines[1]
        return self._comment

        @comment.setter
        def comment(self, value):
            self._comment = value
        
        @property
        def atom_collection:
            if atom_collection is None:
                Atoms = []

                for line in self.lines:
                    parts = line.split()
                    
                    atom_type = parts[0]
                    X = parts[1]
                    Y = parts[2]
                    Z = parts[3]

                    position = np.array([X, Y, Z])

                    atom = Atom(atom_type = symbol, position = position)
                    Atoms.append(atom)

                
                
                


                    

                    
                     
            
                


        

        
