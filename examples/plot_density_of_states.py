
# DEPRECATED

from cmstk.visualization.vasp import DensityOfStatesPlot
from cmstk.vasp.vasprun import VasprunReader
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating density of states plot...")
    start = datetime.now()

    # read in the VASP data
    filename = os.path.join("vasp", "Si_fcc.vasprun.xml")
    vr = VasprunReader(filename)

    # init the plotting object
    dos_plot = DensityOfStatesPlot(vr)

    # custom title
    dos_plot.suptitle("Si FCC Density of States")

    # custom y label
    dos_plot.axes.set_ylabel("DOS")

    # custom x label
    dos_plot.axes.set_xlabel("Energy (eV)")

    # generate the plot
    dos_plot.make()
    filename = "density_of_states.png"
    print("Writing density of states plot to file...")
    dos_plot.savefig(filename, bbox_inches="tight")

    end = datetime.now()
    total_time = (end-start).total_seconds()
    size = os.path.getsize(filename)
    print("Total time: {} seconds".format(total_time))
    print("Generated {} ({} bytes)".format(filename, size))