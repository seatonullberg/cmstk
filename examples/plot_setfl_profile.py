from cmstk.data.setfl import SetflReader
from cmstk.visualization.potential import SetflProfilePlot
import os
from datetime import datetime

# Use the following paper which corresponds to the Zhou-Pd-H-2008.eam.alloy file to validate plotting is accurate
# https://pdfs.semanticscholar.org/b9c1/bcf83327f17942946b41381f9e72e5b77618.pdf

if __name__ == "__main__":
    print("Generating setfl plots...")
    start = datetime.now()

    # Single symbol plot
    # use custom viewport
    custom = {"embedding_xlim": (0.0, 2.0),
              "embedding_ylim": (-10.0, 5.0),
              "density_xlim": (0.0, 5.0),
              "density_ylim": (0.0, 1.0),
              "pair_xlim": (1.0, 5.0),
              "pair_ylim": (-0.75, 0.75)}
    filename = os.path.join("potentials", "Mishin-Ni-1999.eam.alloy")
    setfl_reader = SetflReader(filename)
    setfl_plot = SetflProfilePlot(setfl_reader)
    setfl_plot.custom = custom
    print("Writing single symbol plot to file...")
    filename1 = "Mishin-Ni-1999.eam.png"
    setfl_plot.generate_plot(filename1)


    # VALIDATION CODE <replace Mishin 2004 2 symbol section with this>
    #custom = {"embedding_xlim": (0.0, 50.0),
    #          "embedding_ylim": (-4.0, 12.0),
    #          "density_xlim": (0.0, 5.0),
    #          "density_ylim": (0.0, 5.0),
    #          "pair_xlim": (1.0, 5.0),
    #          "pair_ylim": (-1.0, 1.0)}
    #filename = os.path.join("potentials", "Zhou-Pd-H-2008.eam.alloy")
    #setfl_reader = SetflReader(filename)
    #setfl_plot = SetflProfilePlot(setfl_reader)
    #setfl_plot.custom = custom
    #print("Writing double symbol plot to file...")
    #filename2 = "Zhou-Pd-H-2008.eam.png"
    #setfl_plot.generate_plot(filename2)
    
    # Double symbol plot
    # use custom viewport
    custom = {"embedding_xlim": (0.0, 3.0),
              "embedding_ylim": (-4.0, 6.0),
              "density_xlim": (0.0, 6.0),
              "density_ylim": (0.0, 0.2),
              "pair_xlim": (1.0, 6.0),
              "pair_ylim": (-0.75, 0.75)}
    filename = os.path.join("potentials", "Mishin-Ni-Al-2004.eam.alloy")
    setfl_reader = SetflReader(filename)
    setfl_plot = SetflProfilePlot(setfl_reader)
    setfl_plot.custom = custom
    print("Writing double symbol plot to file...")
    filename2 = "Mishin-Ni-Al-2004.eam.png"
    setfl_plot.generate_plot(filename2)



    # Triple symbol plot
    # use custom viewport
    custom = {"embedding_xlim": (0.0, 3.0),
              "embedding_ylim": (-4.0, 12.0),
              "density_xlim": (3.25, 5.0),
              "density_ylim": (0.0, 0.01),
              "pair_xlim": (1.0, 5.0),
              "pair_ylim": (-0.75, 0.75)}
    filename = os.path.join("potentials", "Bonny-Fe-Ni-Cr-2011.eam.alloy")
    setfl_reader = SetflReader(filename)
    setfl_plot = SetflProfilePlot(setfl_reader)
    setfl_plot.custom = custom
    print("Writing triple symbol plot to file...")
    filename3 = "Bonny-Fe-Ni-Cr-2011.eam.png"
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
