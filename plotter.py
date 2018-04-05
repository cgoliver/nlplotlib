"""
Calls wrapper and produces plot given output from NN.
"""

import roman_wrappers
import time

def make_plot(selection, actions, values, plot_id):
    fns = [getattr(roman_wrappers, f) for f in dir(roman_wrappers) if f.startswith('yy_')]
    #call the function selected by NN
    figpath = fns[selection](actions, values, plot_id)
    return (figpath, time.time())

if __name__ == "__main__":
    # make_plot(1, [])
    pass
