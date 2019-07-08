from typing import List, Optional, Sequence


class PotcarFile(object):
    """File wrapper for a VASP POTCAR file.

    Notes:
        POTCAR files are copyright protected. For testing purposes, the data 
        files are heavily redacted such that only header sections are visible.
    
    Args:
        filepaths: Filepaths to any number of POTCAR files.

    Attributes:
        filepaths: Filepaths to any number of POTCAR files.

    Properties:
        titles: The `TITEL` tag value of each included POTCAR
        - Note: length of `titles` will be greater than `filepaths` if reading
          from an already concatenated POTCAR.
    """
    
    def __init__(self, filepaths: Optional[Sequence[str]] = None) -> None:
        if filepaths is None:
            filepaths = []
        self.filepaths = filepaths
        self._titles: List[str] = []

    @property
    def titles(self) -> List[str]:
        return self._titles

    def read(self, paths: Optional[Sequence[str]] = None) -> None:
        """Reads one or many POTCAR files.
        
        Args:
            paths: The filepaths to read

        Returns:
            None
        """
        self._titles = []  # reset the existing titles each read
        if paths is None:
            paths = self.filepaths
        for path in paths:
            with open(path, "r") as f:
                lines = f.readlines()
            for line in lines:
                if "TITEL" in line:
                    title = line.split("=")[-1].strip()
                    self._titles.append(title)

    def write(self, path: Optional[str] = None) -> None:
        """Writes a POTCAR file.
        
        Args:
            path: The filepath to write to.

        Returns:
            None
        """
        if path is None:
            write_path = "POTCAR"
        else:
            write_path = path
        potcars_in = []
        for read_path in self.filepaths:
            with open(read_path, "r") as f:
                potcars_in.append(f.read())
        potcar_out = "".join(potcars_in)
        with open(write_path, "w") as f:
            f.write(potcar_out)
