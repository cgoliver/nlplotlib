"""
Plotting wrappers.
"""
import matplotlib.pyplot as plt

def xx_make_line_plot(data=None):
    if not data:
        xs = np.random.randn(10)
        plt.plot(xs)
        plt.savefig("static/plot.png", format="png")
        
def xx_make_scatter_plot(data=None):
    if not data:
        xs = np.random.randn(10)
        ys = np.random.randn(10)
        plt.scatter(ys)
        plt.savefig("static/plot.png", format="png")

if __name__ == "__main__":
    pass
