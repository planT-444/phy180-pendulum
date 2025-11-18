import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import statistics


def plot_fit(my_func, xdata, ydata, xerror=None, yerror=None, init_guess=None, font_size=35,
             xaxis="", yaxis="", xunits="", yunits="",
             output_filename = "graph.png",
             logged=False,
             figsize = (18, 9)
             ):    
    plt.rcParams.update({'font.size': font_size})
    plt.rcParams['figure.figsize'] = figsize
    # Change the fontsize of the graphs to make it easier to read.
    # Also change the picture size, useful for the save-to-file option.
    
    popt, pcov = optimize.curve_fit(my_func, xdata, ydata, sigma=yerror, p0=init_guess, absolute_sigma=True)
    # The best fit values are popt[], while pcov[] tells us the uncertainties.

    puncert = np.sqrt(np.diagonal(pcov))
    # The uncertainties are the square roots of the diagonal of the covariance matrix
    
    start = min(xdata)
    stop = max(xdata)    
    xs = np.arange(start,stop,(stop-start)/1000) 
    curve = my_func(xs, *popt) 
    # (x,y) = (xs,curve) is the line of best fit for the data in (xdata,ydata).
    # It has 1000 points to make it look smooth.
    # Note: the "*" tells Python to send all the popt values in a readable way.
    if logged:
        fig, ax1 = plt.subplots()
    else:
        fig, (ax1,ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})
    # Make 2 graphs above/below each other: ax1 is top, ax2 is bottom.
    # The gridspec_kw argument makes the top plot 2 times taller than the bottom plot.
    # You can adjust the relative heights by, say, changing [2, 1] to [3, 1].
    
    if logged:
        yerror = 0 * yerror
        xerror = 0 * xerror
    
    ax1.errorbar(xdata, ydata, yerr=yerror, xerr=xerror, fmt=".", label="data", color="black")
    # Plot the data with error bars, fmt makes it data points not a line, label is
    # a string which will be printed in the legend, you should edit this string.

    ax1.plot(xs, curve, label="best fit", color="black")
    # Plot the best fit curve on top of the data points as a line.
    # NOTE: you may want to change the value of label to something better!!

    ax1.legend(loc='upper right' if output_filename=="amplitude vs. time" else 'lower right')
    # Prints a box using what's in the "label" strings in the previous two lines.
    # loc specifies the location

    if xunits != "":
        xunits = f"({xunits})"
    if yunits != "":
        yunits = f"({yunits})"
    
    ax1.set_xlabel(f"{xaxis} {xunits}")
    ax1.set_ylabel(f"{yaxis} {yunits}")
    # label the axes and set a title
    
    if not logged:
        residual = ydata - my_func(xdata, *popt)
        ax2.errorbar(xdata, residual, yerr=yerror, xerr=xerror, fmt=".", color="black")
        # Plot the residuals with error bars.
        
        ax2.axhline(y=0, color="black")    
        # Plot the y=0 line for context.
        
        ax2.set_xlabel(f"{xaxis} {xunits}")
        ax2.set_ylabel(f"Residuals {yunits}")
        # ax2.set_title("Residuals of the fit")
        # Here is where you change how your graph is labelled.

    fig.tight_layout()
    # Does a decent cropping job of the two figures.
    
    y_fit = my_func(xdata, *popt)
    r_2 = 1 - np.sum((ydata - y_fit)**2) / np.sum((ydata - np.mean(ydata))**2)

    output_dir = Path(__file__).parent / "output-files"
    
    with open(output_dir / (output_filename + ".txt"), 'w') as f:
        f.write("Best fit parameters, with uncertainties, but not rounded off properly:\n")
        for i in range(len(popt)):
            f.write(f"{popt[i]} +/- {puncert[i]}\n")
        f.write(f"R-squared: {r_2}")
    
    fig.savefig(output_dir / (output_filename + ".png"))


# test!!!