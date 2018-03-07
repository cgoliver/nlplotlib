"""
Calls wrapper and produces plot given output from NN.
"""

import wrappers

def make_plot(selection, args):
    fns = [getattr(wrappers, f) for f in dir(wrappers) if f.startswith('xx_')]
    #call the function selected by NN
    figpath = fns[selection]()
    return figpath

if __name__ == "__main__":
    make_plot(1, [])
    pass
