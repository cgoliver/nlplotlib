"""
Plotting wrappers.
"""
import uuid
import os
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def xx_make_line_plot(*args, data=None):
    if not data:
        xs = np.random.randn(10)
        fig, ax = plt.subplots()
        ax.plot(xs)
        path =  "static/{}.png".format(uuid.uuid1())
        fig.savefig(path, format="png")
        
        return path
    return 0
def xx_make_scatter_plot(data=None):
    if not data:
        xs = np.random.randn(10)
        ys = np.random.randn(10)
        fig, ax = plt.subplots()
        plt.scatter(xs, ys)
        name =  str(uuid.uuid1()) + '.png'
        path = os.path.join("static", "plots",name)
        fig.savefig(path, format="png")
        return name  
    return 0

if __name__ == "__main__":
    xx_make_line_plot()
    pass
