import numpy as np
def plot_trend(fit_results, dataname, ax):
    xs = np.linspace(*ax.get_xlim())
    ys = fit_results.predict({dataname: xs, 'host': 'rapi'})
    ax.plot(xs, ys, '-')