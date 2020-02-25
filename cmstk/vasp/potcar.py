from cmstk.filetypes import TextFile
from typing import List, Optional


class PotcarFile(TextFile):
    """File wrapper for a VASP POTCAR file.

    Notes:
        POTCAR files are copyright protected. For testing purposes, the data 
        files are heavily redacted such that only header sections are visible.

    Args:
        filepath: Filepath to a POTCAR file.

    Attributes:
        filepath: Filepath to a POTCAR file.
        titles: The `TITEL` tag values.
    """
    def __init__(self, filepath: Optional[str] = None) -> None:
        if filepath is None:
            filepath = "POTCAR"
        self._titles: Optional[List[str]] = None
        super().__init__(filepath)

    @property
    def titles(self) -> List[str]:
        if self._titles is None:
            titles = []
            for line in self.lines:
                if "TITEL" in line:
                    title = line.split("=")[-1].strip()
                    titles.append(title)
            self._titles = titles
        return self._titles

    def concatenate(self, path: str) -> None:
        with open(path, "r") as f:
            new_lines = [
                line.strip() for line in f.readlines() if len(line.strip()) > 0
            ]
        # not ideal
        self._lines += new_lines  # type: ignore
        self._titles = None

    def write(self, path: Optional[str]) -> None:
        if path is None:
            path = self.filepath
        with open(path, "w") as f:
            for line in self.lines:
                f.write("{}\n".format(line))
