from cmstk.data.setfl import SetflReader
from cmstk.visualization.potential import SetflProfilePlot
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating setfl plots...")
    start = datetime.now()
    
    # Single symbol plot
    filename = os.path.join("potentials", "Mishin-Ni-1999.eam.alloy")
    setfl_reader = SetflReader(filename)
    setfl_plot = SetflProfilePlot(setfl_reader)
    print("Writing single symbol plot to file...")
    filename1 = "Mishin-Ni-1999.eam.png"
    setfl_plot.generate_plot(filename1)

    # Double symbol plot
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    setfl_reader = SetflReader(filename)
    setfl_plot = SetflProfilePlot(setfl_reader)
    print("Writing double symbol plot to file...")
    filename2 = "Mishin-Ni-Al-2004.eam.png"
    setfl_plot.generate_plot(filename2)

    # Triple symbol plot
    filename = os.path.join("potentials", "Pun-Ni-Al-Co-2015.eam.alloy")
    setfl_reader = SetflReader(filename)
    setfl_plot = SetflProfilePlot(setfl_reader)
    print("Writing triple symbol plot to file...")
    filename3 = "Pun-Ni-Al-Co-2015.eam.png"
    setfl_plot.generate_plot(filename3)

    end = datetime.now()
    total_time = (end-start).total_seconds()
    size1 = os.path.getsize(filename1)
    size2 = os.path.getsize(filename2)
    size3 = os.path.getsize(filename3)
    print("Total time: {} seconds".format(total_time))
    print("Generated {} ({} bytes)".format(filename1, size1))
    print("Generated {} ({} bytes)".format(filename2, size2))
    print("Generated {} ({} bytes)".format(filename3, size3))
