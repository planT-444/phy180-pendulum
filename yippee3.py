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
    