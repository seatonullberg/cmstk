from cmstk.visualization.multivariate import ParallelPlot
import numpy as np
import os
from datetime import datetime


if __name__ == "__main__":
    print("Generating parallel plot...")
    start = datetime.now()

    # generate random data
    orange_data = np.random.normal(size=(25, 5))
    blue_data = np.random.normal(size=(25, 5))
    green_data = np.random.normal(size=(25, 5))
    
    # specify settings
    title = "Test Parallel Plot Title"
    xlabels = ["x0", "x1", "x2", "x3", "x4"]
    ylabel = "Cost"
    
    # init the plotting object
    pp = ParallelPlot(title, xlabels, ylabel)

    # add each dataset as a separate group
    pp.add_data(data=orange_data, color="#f47a42", label="orange")
    pp.add_data(data=blue_data, color="#4268f4", label="blue")
    pp.add_data(data=green_data, color="#28a83f", label="green")

    # set custom viewport
    pp.custom["ylim"] = (-3, 3)

    # generate the plot
    filename = "test_parallel.png"
    print("Writing parallel plot to file...")
    pp.generate_plot(filename)

    end = datetime.now()
    total_time = (end-start).total_seconds()
    size = os.path.getsize(filename)
    print("Total time: {} seconds".format(total_time))
    print("Generated {} ({} bytes)".format(filename, size))
