import json
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

system_name = "bigO"

def compute_aic(nobs, rss, k=2):
    """
    Compute AIC for a model.
    AIC = n * ln(RSS/n) + 2*k
    """
    if nobs < 2 or rss <= 0:
        return np.inf
    return nobs * np.log(rss / nobs) + 2 * k

def fit_power_law(n, y):
    """
    O(n^b):
    log(y) = b*log(n) + log(c)
    """
    n = np.array(n, dtype=float)
    y = np.array(y, dtype=float)
    mask = (n > 0) & (y > 0)
    n = n[mask]
    y = y[mask]
    if len(n) < 2:
        return None
    log_n = np.log(n)
    log_y = np.log(y)
    slope, intercept, r, p, stderr = linregress(log_n, log_y)
    pred_log_y = intercept + slope * log_n
    pred_y = np.exp(pred_log_y)
    rss = np.sum((y - pred_y)**2)
    aic = compute_aic(len(n), rss)
    return ("O(n^b)", slope, intercept, r, p, stderr, n, pred_y, aic)

def fit_log_n(n, y):
    """
    O(log n):
    y = c*log(n) + const
    """
    n = np.array(n, dtype=float)
    y = np.array(y, dtype=float)
    mask = (n > 1) & (y > 0)
    n = n[mask]
    y = y[mask]
    if len(n) < 2:
        return None
    log_n = np.log(n)
    slope, intercept, r, p, stderr = linregress(log_n, y)
    pred_y = intercept + slope * log_n
    rss = np.sum((y - pred_y)**2)
    aic = compute_aic(len(n), rss)
    return ("O(log n)", slope, intercept, r, p, stderr, n, pred_y, aic)

def fit_n_log_n(n, y):
    """
    O(n log n):
    y = c*(n log n) + const
    """
    n = np.array(n, dtype=float)
    y = np.array(y, dtype=float)
    mask = (n > 1) & (y > 0)
    n = n[mask]
    y = y[mask]
    if len(n) < 2:
        return None
    x = n * np.log(n)
    slope, intercept, r, p, stderr = linregress(x, y)
    pred_y = intercept + slope * x
    rss = np.sum((y - pred_y)**2)
    aic = compute_aic(len(n), rss)
    return ("O(n log n)", slope, intercept, r, p, stderr, n, pred_y, aic)

def fit_linear(n, y):
    """
    O(n):
    y = c*n + const
    """
    n = np.array(n, dtype=float)
    y = np.array(y, dtype=float)
    mask = (n > 0) & (y > 0)
    n = n[mask]
    y = y[mask]
    if len(n) < 2:
        return None
    slope, intercept, r, p, stderr = linregress(n, y)
    pred_y = intercept + slope * n
    rss = np.sum((y - pred_y)**2)
    aic = compute_aic(len(n), rss)
    return ("O(n)", slope, intercept, r, p, stderr, n, pred_y, aic)

def fit_quadratic(n, y):
    """
    O(n^2):
    y = c*n^2 + const
    """
    n = np.array(n, dtype=float)
    y = np.array(y, dtype=float)
    mask = (n > 0) & (y > 0)
    n = n[mask]
    y = y[mask]
    if len(n) < 2:
        return None
    x = n**2
    slope, intercept, r, p, stderr = linregress(x, y)
    pred_y = intercept + slope * x
    rss = np.sum((y - pred_y)**2)
    aic = compute_aic(len(n), rss)
    return ("O(n^2)", slope, intercept, r, p, stderr, n, pred_y, aic)

def choose_best_fit(n, y):
    """
    Choose best fit among O(n^b), O(log n), O(n log n), O(n), O(n^2)
    by minimizing AIC.
    """
    fits = []
    for fit_func in [fit_power_law, fit_log_n, fit_n_log_n, fit_linear, fit_quadratic]:
        result = fit_func(n, y)
        if result is not None:
            fits.append(result)
    if not fits:
        return None
    best = min(fits, key=lambda x: x[8])  # x[8] is the AIC
    return best

def format_model_name(model_name, slope):
    # If O(n^b), format exponent
    if model_name == "O(n^b)":
        return f"O(n^{slope:.2f})"
    else:
        return model_name

def remove_outliers(n, y):
    """
    Remove outliers using IQR method.
    """
    y = np.array(y, dtype=float)
    n = np.array(n, dtype=float)
    if len(y) < 4:
        return n, y
    Q1, Q3 = np.percentile(y, [25, 75])
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    mask = (y >= lower_bound) & (y <= upper_bound)
    return n[mask], y[mask]

def plot_complexities_from_file(filename=f'{system_name}_data.json'):
    with open(filename, 'r') as f:
        data = json.load(f)
        
    entries = []
    for key, records in data.items():
        key_str = key.strip("()")
        parts = key_str.split(",")
        function_name = parts[0].strip().strip("'\"")
        file_name = parts[1].strip().strip("'\"")
        
        lengths = [r["length"] for r in records]
        times = [r["time"] for r in records]
        mems = [r["memory"] for r in records]
        
        entries.append((function_name, file_name, lengths, times, mems))
    
    n_entries = len(entries)
    
    sns.set_style("whitegrid")
    # Use squeeze=False to always get a 2D array of axes

    plot_memory = True

    if plot_memory:
        fig, axes = plt.subplots(nrows=n_entries, ncols=2, figsize=(12, 4 * n_entries), squeeze=False)
    else:
        fig, axes = plt.subplots(nrows=n_entries, ncols=1, figsize=(6, 4 * n_entries), squeeze=False)
    
    for i, (func, filepath, lengths, times, mems) in enumerate(entries):
        # Remove outliers
        n_time, y_time = remove_outliers(lengths, times)
        time_fit = choose_best_fit(n_time, y_time)
        
        n_mem, y_mem = remove_outliers(lengths, mems)
        mem_fit = choose_best_fit(n_mem, y_mem)
        
        # Time plot (axes[i,0])
        ax_time = axes[i, 0]
        ax_time.plot(n_time, y_time, 'o', color='blue', label='Data (outliers removed)')
        if time_fit is not None:
            model_name, slope, intercept, r, p, stderr, fit_x, fit_y, aic = time_fit
            sort_idx = np.argsort(fit_x)
            ax_time.plot(fit_x[sort_idx], fit_y[sort_idx], '-', color='blue', linewidth=1, label='Fit')
            model_display = format_model_name(model_name, slope)
            title = f"{func} (Time): {model_display}\nR={r:.3f}, p={p:.3g}, AIC={aic:.2f}"
        else:
            title = f"{func} (Time): No fit"
        ax_time.set_xlabel('Input Size (n)')
        ax_time.set_ylabel('Time')
        ax_time.set_title(title, fontsize=12)
        ax_time.legend()

        if plot_memory:
            # Memory plot (axes[i,1])
            ax_mem = axes[i, 1]
            ax_mem.plot(n_mem, y_mem, 'o', color='red', label='Data (outliers removed)')
            if mem_fit is not None:
                model_name, slope, intercept, r, p, stderr, fit_x, fit_y, aic = mem_fit
                sort_idx = np.argsort(fit_x)
                ax_mem.plot(fit_x[sort_idx], fit_y[sort_idx], '-', color='red', linewidth=1, label='Fit')
                model_display = format_model_name(model_name, slope)
                title = f"{func} (Memory): {model_display}\nR={r:.3f}, p={p:.3g}, AIC={aic:.2f}"
            else:
                title = f"{func} (Memory): No fit"
            ax_mem.set_xlabel('Input Size (n)')
            ax_mem.set_ylabel('Memory')
            ax_mem.set_title(title, fontsize=12)
            ax_mem.legend()
    
    plt.tight_layout()
    filename = f"{system_name}.pdf"
    plt.savefig(filename)
    print(f"{filename} written.")
    # plt.show()

if __name__ == "__main__":
    fname = f'{system_name}_data.json'
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    plot_complexities_from_file(fname)
