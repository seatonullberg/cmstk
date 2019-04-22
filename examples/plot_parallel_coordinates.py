from cmstk.visualization.multivariate import ParallelCoordinatesPlot
import numpy as np
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating parallel coordinates plot...")
    start = datetime.now()

    # generate random data
    orange_data = np.random.normal(size=(25, 5))
    blue_data = np.random.normal(size=(25, 5))
    green_data = np.random.normal(size=(25, 5))

    # specify settings
    title = "Test Title"
    xlabels = ["x0", "x1", "x2", "x3", "x4"]
    ylabel = "Cost"
    
    # init the plotting object
    pcp = ParallelCoordinatesPlot(title, xlabels, ylabel)

    # add each dataset as a separate group
    pcp.add_data(data=orange_data, color="#f47a42", label="orange")
    pcp.add_data(data=blue_data, color="#4268f4", label="blue")
    pcp.add_data(data=green_data, color="#28a83f", label="green")

    # set custom viewport
    pcp.custom["ylim"] = (-3, 3)

    # generate the plot
    filename = "parallel_coordinates.png"
    print("Writing parallel coordinates plot to file...")
    pcp.generate_plot(filename)

    end = datetime.now()
    total_time = (end-start).total_seconds()
    size = os.path.getsize(filename)
    print("Total time: {} seconds".format(total_time))
    print("Generated {} ({} bytes)".format(filename, size))
