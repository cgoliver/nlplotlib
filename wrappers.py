"""
Plotting wrappers.
"""
import uuid
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def xx_make_line_plot(data=None):
    if not data:
        xs = np.random.randn(10)
        fig, ax = plt.subplots()
        ax.plot(xs)
        fig.savefig("static/{}.png".format(uuid.uuid1()), format="png")
        
def xx_make_scatter_plot(data=None):
    if not data:
        xs = np.random.randn(10)
        ys = np.random.randn(10)
        plt.scatter(ys)
        fig.savefig("static/{}.png".format(uuid.uuid1()), format="png")

if __name__ == "__main__":
    xx_make_line_plot()
    pass
