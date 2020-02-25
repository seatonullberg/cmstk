from cmstk.eam import SetflFile
from cmstk.util import data_directory
from cmstk.visualization.potential import setfl_profile_plot
import os
from datetime import datetime

# This example reproduces Fig. 2 from the following paper:
# https://pdfs.semanticscholar.org/b9c1/bcf83327f17942946b41381f9e72e5b77618.pdf

if __name__ == "__main__":
    print("Generating setfl plot...")
    start = datetime.now()

    # load plotting data
    path = os.path.join(data_directory(), "potentials",
                        "Zhou-Pd-H-2008.eam.alloy")
    setfl = SetflFile(path)
    setfl.load()
    fig, axes = setfl_profile_plot(setfl)

    # customize the plot
    axes[0].set_xlim((0.0, 50.0))
    axes[0].set_ylim((-4.0, 12.0))
    axes[1].set_xlim((0.0, 5.0))
    axes[1].set_ylim((0.0, 5.0))
    axes[2].set_xlim((1.0, 5.0))
    axes[2].set_ylim((-1.0, 1.0))
    filename = "Zhou-Pd-H-2008.eam.png"
    fig.savefig(filename)

    end = datetime.now()
    total_time = (end - start).total_seconds()
    size = os.path.getsize(filename)
    print("Total time: {} seconds".format(total_time))
    print("Generated {} ({} bytes)".format(filename, size))
