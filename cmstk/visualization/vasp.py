from cmstk.utils import consecutive_percent_difference
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt


class ConvergeEncutPlot(object):
    """Implementation of a plot displaying the results of an ENCUT convergence 
       calculation.
    
    Args:
        encut_values: The tested values of ENCUT.
        toten_values: The resulting TOTEN values corresponding to each ENCUT.
    """
    def __init__(self, encut_values, toten_values):
        self.encut_values = encut_values
        self.toten_values = toten_values
        self.fig, self.axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 4))

    def make(self):
        """Plots the available data."""
        self.axes.set_xlabel("ENCUT Value (eV)")
        self.axes.set_ylabel("TOTEN Value (eV)")
        self.axes.set_title("ENCUT Convergence Results")
        self.axes.plot(self.encut_values, self.toten_values)
        for i, delta in enumerate(consecutive_percent_difference(self.toten_values)):
            annotation = "{}%".format(delta)
            self.axes.annotate(
                annotation, 
                (self.encut_values[i], self.toten_values[i])
            )
        self.fig.tight_layout()

    def summarize(self):
        s = "ENCUT Convergence Results\n\n"
        s += "ENCUT (eV)\t\tTOTEN (eV)\t\tDELTA\n\n"
        for encut, toten, delta in zip(self.encut_values, 
                                       self.toten_values, 
                                       consecutive_percent_difference(self.toten_values)):
            s += "{0:.0f}\t\t\t{1:.4f}\t\t{2:.2f}%\n".format(encut, toten, delta)
        path = "converge_encut_summary.txt"
        with open(path, "w") as f:
            f.write(s)


class ConvergeKpointsPlot(object):
    """Implementation of a plot displaying the results of a KPOINTS convergence 
       calculation.
    
    Args:
        kpoint_sizes: The tested mesh sizes.
        toten_values: The resulting TOTEN values corresponding to each mesh size.
    """
    def __init__(self, kpoint_sizes, toten_values):
        self.kpoint_sizes = kpoint_sizes
        self.toten_values = toten_values