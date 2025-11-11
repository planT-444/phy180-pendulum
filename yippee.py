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
from plot_fit import plot_fit


def load_period_vs_amplitude(filename):
    data = np.genfromtxt(filename, usecols=(0,1), skip_header=1, delimiter = ',')
    filtered_periods = {}
    
    for amplitude, period in data:
        if amplitude not in filtered_periods:
            filtered_periods[amplitude] = []
        filtered_periods[amplitude].append(period)
    print(filtered_periods)
    amplitudes = []
    amplitude_error = []
    mean_periods = []
    period_error = []
    period_b_uncertainty = 3e-3 # 120 fps, 3 oscillations: 1/120/3 = 2.78e-3 ~ 3e-3
    for amplitude, periods in filtered_periods.items():
        amplitudes.append(amplitude)
        amplitude_error.append(np.deg2rad(0.5))
        mean_periods.append(np.mean(periods))
        period_error.append(max(
            period_b_uncertainty, 
            statistics.stdev(periods) / len(periods) ** 0.5
        ))
        print(period_b_uncertainty, 
            statistics.stdev(periods) / len(periods) ** 0.5)
    print(period_error)
    return np.array(amplitudes), np.array(mean_periods), np.array(amplitude_error), np.array(period_error)


def load_exponential_amplitude(filename):
    times, amplitudes = np.genfromtxt(filename, usecols=(0,1), skip_header=1, unpack = True, delimiter = ',')
    time_error = np.array([1/120] * len(times))
    amplitude_error = np.array([np.deg2rad(0.2)] * len(amplitudes))
    return times, amplitudes, time_error, amplitude_error
    
def power_series(theta, a, b, c):
    return a * (1 + b * theta + c * theta ** 2)

def exponential(time, theta_0, tau):
    return theta_0 * np.e ** -(time/tau)


input_dir = Path(__file__).parent / "input-files"
if __name__ == '__main__':
    plot_fit(power_series, 
             *load_period_vs_amplitude(input_dir / "PHY180 Pendulum - Sheet2.csv"),
             xaxis="Initial Amplitude", xunits="rad",
             yaxis="Period", yunits="s",
             output_filename = "period vs amplitude")
    plot_fit(exponential, *load_exponential_amplitude(input_dir / "PHY180 Pendulum - Sheet4.csv"),
             xaxis="Time", xunits="s",
             yaxis="Amplitude", yunits="rad",
             output_filename = "amplitude vs. time")
