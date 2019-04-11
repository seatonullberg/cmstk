from cmstk.data.setfl import SetflReader
from cmstk.visualization.potential import SetflProfilePlot
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating setfl plot...")
    start = datetime.now()
    # read a potential file
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    setfl_reader = SetflReader(filename)
    setfl_plot = SetflProfilePlot(setfl_reader)
    print("Writing plot to file...")
    # generate the plot
    filename = "Mishin-Ni-Al-2004.eam.png"
    setfl_plot.generate_plot(filename)
    end = datetime.now()
    total_time = (end-start).total_seconds()
    print("Total time: {} seconds".format(total_time))
    size = os.path.getsize(filename)
    print("Generated {} ({} bytes)".format(filename, size))