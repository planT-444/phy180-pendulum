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


import numpy as np
import statistics
from pathlib import Path
from plot_fit import plot_fit

def load_period_vs_length(filename):
    data = np.genfromtxt(filename, usecols=(0,1), skip_header=1, delimiter = ',')
    filtered_periods = {}
    
    for length, period in data:
        if length not in filtered_periods:
            filtered_periods[length] = []
        filtered_periods[length].append(period)
    print(filtered_periods)
    lengths = []
    length_error = []
    mean_periods = []
    period_error = []
    period_b_uncertainty = 0.0008 # 120 fps, 10 oscillations
    for length, periods in filtered_periods.items():
        lengths.append(length)
        length_error.append(0.005)
        mean_periods.append(np.mean(periods))
        period_error.append(max(
            period_b_uncertainty, 
            statistics.stdev(periods) / len(periods) ** 0.5
        ))
        print(period_b_uncertainty, 
            statistics.stdev(periods) / len(periods) ** 0.5)
    print(period_error)
    print(mean_periods)
    return (
        np.array(lengths), 
        np.array(mean_periods), 
        np.array(length_error), 
        np.array(period_error)
    )
    
def power_series(L, k, n):
    return k * L ** n

"""
T = k * L ** n
logT = log(k * L ** n)
     = logk + nlogL
"""

def line(x, b, m):
    return m * x + b

input_dir = Path(__file__).parent / "input-files"
if __name__ == '__main__':
    tvsl_data = load_period_vs_length(input_dir / "PHY180 Pendulum - T vs L.csv")
    plot_fit(power_series, 
             *tvsl_data,
             xaxis="Length", xunits="m",
             yaxis="Period", yunits="s",
             output_filename = "period vs length")
    plot_fit(power_series, 
             *tvsl_data,
             xaxis="Length", xunits="m",
             yaxis="Period", yunits="s",
             output_filename = "period vs length logged",
             logged=True)
    