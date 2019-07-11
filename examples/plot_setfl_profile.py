
# DEPRECATED

from cmstk.eam import SetflFile
from cmstk.visualization.potential import SetflProfilePlot
import os
from datetime import datetime

# Use the following paper which corresponds to the Zhou-Pd-H-2008.eam.alloy file to validate plotting is accurate
# https://pdfs.semanticscholar.org/b9c1/bcf83327f17942946b41381f9e72e5b77618.pdf

if __name__ == "__main__":
    print("Generating setfl plot...")
    start = datetime.now()

    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.join(path, "data", "potentials", 
                        "Zhou-Pd-H-2008.eam.alloy")
    setfl = SetflFile(path)
    setfl.read()
    setfl_plot = SetflProfilePlot(setfl)
    
    # viewport customization
    custom = {"embedding_xlim": (0.0, 50.0),
              "embedding_ylim": (-4.0, 12.0),
              "density_xlim": (0.0, 5.0),
              "density_ylim": (0.0, 5.0),
              "pair_xlim": (1.0, 5.0),
              "pair_ylim": (-1.0, 1.0)}

    setfl_plot = SetflProfilePlot(setfl)
    setfl_plot.custom = custom
    filename = "Zhou-Pd-H-2008.eam.png"
    setfl_plot.make()
    setfl_plot.fig.savefig(filename)

    end = datetime.now()
    total_time = (end-start).total_seconds()
    size = os.path.getsize(filename)
    print("Total time: {} seconds".format(total_time))
    print("Generated {} ({} bytes)".format(filename, size))
