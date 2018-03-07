"""
Calls wrapper and produces plot given output from NN.
"""

import wrappers

def make_plot(selection, args):
    print(dir(wrappers))
    fns = [getattr(wrappers, f) for f in dir(wrappers) if f.startswith('xx_')]
    #call the function selected by NN
    fns[selection](*args)

if __name__ == "__main__":
    make_plot(1)
    pass
