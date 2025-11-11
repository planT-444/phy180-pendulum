import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
import statistics
from pathlib import Path
from plot_fit import plot_fit

def load_data_calculate_Qs():
    output = ""
    input_dir = Path(__file__).parent / "input-files"
    period_filename = input_dir / "PHY180 Pendulum - T vs L.csv"

    data = np.genfromtxt(period_filename, usecols=(0,1), skip_header=1, delimiter = ',')
    filtered_periods = {}
    
    for length, period in data:
        if length not in filtered_periods:
            filtered_periods[length] = []
        filtered_periods[length].append(period)

    lengths = []
    mean_periods = []
    period_error = []
    period_b_uncertainty = 0.0008 # 120 fps, 10 oscillations
    for length, periods in filtered_periods.items():
        lengths.append(length)
        mean_periods.append(np.mean(periods))
        period_error.append(max(
            period_b_uncertainty, 
            statistics.stdev(periods) / len(periods) ** 0.5
        ))

    lengths, mean_periods, period_error = zip(
        *sorted(
            zip(lengths, mean_periods, period_error)
        )
    )
    print(lengths)
    print(mean_periods)
    print('\n\n\n')
    
    Qs = []
    Q_uncertainties = []
    for length_i, length in enumerate(sorted(lengths)):
        print(f"PHY180 Pendulum - L={length * 100:.1f}.csv")
        
        filename = input_dir / f"PHY180 Pendulum - L={length * 100:.1f}.csv"
        times, amplitudes = np.genfromtxt(filename, usecols=(3,4), skip_header=1, unpack = True, delimiter = ',')
        time_error = np.array([1/120] * len(times))
        amplitude_error = np.array([np.deg2rad(0.3)] * len(amplitudes))
        popt, pcov = optimize.curve_fit(exponential, times, amplitudes, sigma=amplitude_error, p0=None, bounds = ([0,0], [np.inf, np.inf]), absolute_sigma=True)
        # The best fit values are popt[], while pcov[] tells us the uncertainties.

        puncert = np.sqrt(np.diagonal(pcov))
        # The uncertainties are the square roots of the diagonal of the covariance matrix

        tau = popt[1]
        tau_uncert = puncert[1]
        T = mean_periods[length_i]
        Qs.append(np.pi * tau/T)
        Q_uncertainties.append(
            np.pi * tau/T * max(
                period_error[length_i] / T,
                tau_uncert / tau
            )
        )

        output += f"Length {length}:\n"
        output += f"theta_0: {popt[0]} +/- {puncert[0]}\n"
        output += f"tau: {popt[1]} +/- {puncert[1]}\n"
        output += f"Q: {Qs[length_i]} +/- {Q_uncertainties[length_i]}\n"
        output += "\n"
        
    output_dir = Path(__file__).parent / "output-files"
        
    with open(output_dir / ("lengths and taus.txt"), 'w') as f:
        f.write("Best fit parameters, with uncertainties, but not rounded off properly:\n")
        f.write(output)
    
    return (
        np.array(lengths), 
        np.array(Qs), 
        np.array([0.005] * len(lengths)), 
        np.array(Q_uncertainties)
    ) 

def exponential(time, theta_0, tau):
    return theta_0 * np.exp(-time/tau)

def quadratic(length, a, b, c):
    return a * length ** 2 + b * length + c 

def line(length, m, b):
    return m * length + b

def sqrt(length, a, b):
    return a * length ** 0.5 + b

def logarithm(length, a, b):
    return a * np.log(length) + b

if __name__ == '__main__':
    plot_fit(line, *load_data_calculate_Qs(),
        xaxis="Length", xunits="m",
        yaxis="Q factor",
        output_filename = "Q vs. length linear")
    
    plot_fit(quadratic, *load_data_calculate_Qs(),
        xaxis="Length", xunits="m",
        yaxis="Q factor",
        output_filename = "Q vs. length quadratic")
    
    plot_fit(logarithm, *load_data_calculate_Qs(),
        xaxis="Length", xunits="m",
        yaxis="Q factor",
        output_filename = "Q vs. length log")
    
    plot_fit(sqrt, *load_data_calculate_Qs(),
        xaxis="Length", xunits="m",
        yaxis="Q factor",
        output_filename = "Q vs. length sqrt")

    
