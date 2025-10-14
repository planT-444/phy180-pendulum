# -*- coding: utf-8 -*-
"""
This program will find the best fit of a given function to a given set
of data (including errorbars). It prints the results, with uncertainties.
Then it plots the graph and displays it to the screen, and also saves
a copy to a file in the local directory. Below the main graph is a 
residuals graph, the difference between the data and the best fit line.

There is also a function which will load data from a file. More convenient.
The first line of the file is ignored (assuming it's the name of the variables).
After that the data file needs to be formatted: 
number space number space number space number newline
Do NOT put commas in your data file!! You can use tabs instead of spaces.
The data file should be in the same directory as this python file.
The data should be in the order:
x_data y_data x_uncertainty y_uncertainty
"""


import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
import statistics
from pathlib import Path

def load_fit_exponential_amplitudes(lengths):
    output = ""
    input_dir = Path(__file__).parent / "input-files"

    for length in lengths:
        filename = input_dir / f"PHY180 Pendulum - L={length}.csv"
        times, amplitudes = np.genfromtxt(filename, usecols=(0,1), skip_header=1, unpack = True, delimiter = ',')
        time_error = np.array([1/120] * len(times))
        amplitude_error = np.array([np.deg2rad(0.2)] * len(amplitudes))
        print(times)
        print(amplitudes)
               
        popt, pcov = optimize.curve_fit(exponential, times, amplitudes, sigma=amplitude_error, p0=None, absolute_sigma=True)
        # The best fit values are popt[], while pcov[] tells us the uncertainties.

        puncert = np.sqrt(np.diagonal(pcov))
        # The uncertainties are the square roots of the diagonal of the covariance matrix
        output += f"Length {length}:\n"
        for i in range(len(popt)):
            output += f"{popt[i]} +/- {puncert[i]}\n"
        output += "\n"
        
    output_dir = Path(__file__).parent / "output-files"
        
    with open(output_dir / ("lengths and taus.txt"), 'w') as f:
        f.write("Best fit parameters, with uncertainties, but not rounded off properly:\n")
        f.write(output)

def exponential(time, theta_0, tau):
    return theta_0 * np.e ** -(time/tau)


if __name__ == '__main__':
    load_fit_exponential_amplitudes([36.5])