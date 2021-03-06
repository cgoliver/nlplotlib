"""
Plotting wrappers.
"""
import uuid
import os
import shutil
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def xx_make_line_plot():
    xs = np.random.randn(10)
    fig, ax = plt.subplots()
    ax.plot(xs)
    name =  str(uuid.uuid1())
    path = os.path.join("static", "plots", name)
    os.makedirs(path)
    fig.savefig(os.path.join(path, "plot.png"), format="png")
    return name 
def xx_make_scatter_plot():
    xs = np.random.randn(10)
    ys = np.random.randn(10)
    fig, ax = plt.subplots()
    plt.scatter(xs, ys)
    name =  str(uuid.uuid1())
    path = os.path.join("static", "plots",name)
    os.makedirs(path)
    fig.savefig(os.path.join(path, "plot.png"), format="png")
    return name 

if __name__ == "__main__":
    xx_make_line_plot()
    pass
