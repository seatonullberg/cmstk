from cmstk.data.setfl import SetflReader
from cmstk.visualization.potential import SetflProfilePlot
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating cohesive energy plot...")
    start = datetime.now()
    # read a potential file
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    setfl_reader = SetflReader(filename)
    setfl_plot = SetflProfilePlot(setfl_reader)
    setfl_plot.generate_plot()