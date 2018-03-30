from matplotlib import pyplot as plt
import pickle
import pandas
import matplotlib
import numpy as np
import uuid
import os


def save_fig(fig, name=None, data=None):
    if not name:
        name =  str(uuid.uuid1())
    path = os.path.join("static", "plots",name)
    fig.savefig(path+".png", format="png")
    pickle.dump(fig, open(path + ".pickle", "wb"))
    if data:
        pickle.dump(data, open(path + ".pickle.data", "wb"))
    return name

def pandas_from_file(file):
    df = pandas.DataFrame.from_csv(file,header=0)
    return df

#returns a column from a pandas dataframe.
def file_to_column(file,col):
    df = pandas_from_file(file)
    if col not in df.columns.values:
        for colname in df.columns.values:
            if col in colname:
                col=colname
    col = df[col].tolist()
    return col

#draws plot from input command column names parsed directly from the text, hard coded from info from the attached csv.
def xx_draw_plot(actions, values, id):
    """
    values is a tuple (datafile, columns)
    action is a list of words
    """
    file, columns = values
    fig = plt.figure()
    to_plot = []
    if "line" in actions:
        for data in columns:
            to_plot = file_to_column(file,data)
            plt.plot(to_plot)
    elif "scatter" in actions:
        to_plot = []
        for data in columns:
            to_plot.append(file_to_column(file,data))

        plt.scatter(*to_plot)
    return save_fig(fig, data=to_plot, name=id)

# plot =draw_plot(["draw", "scatter", "plot"], ("grades.csv",["Test2","Final"]))
# plt.show(plot)
# plot =draw_plot(["draw", "line", "plot"], ("grades.csv",["Test2","Final"]))
# plt.show(plot)


def yy_add_title(action, values, id):
    maxl = -1
    this_title = ""
    for elements in values:
        if len(elements)> maxl:
            this_title = elements
    plot = pickle.load(open('plot.pickle','rb'))
    plot.suptitle(this_title)
    # pickle.dump(plot,open('plot.pickle','wb'))
    return save_fig(plot, name=id)
# add_title(["add","title"],["This is a title"])

def yy_set_ax_title(action,values, id):
    maxl = -1
    this_title = ""
    for elements in values:
        if len(elements) > maxl:
            this_title = elements
    plot = pickle.load(open('plot.pickle','rb'))
    ax = plot.get_axes()[0]
    if "x-" in "".join(action) or " x " in "".join(action):
        ax.set_xlabel(this_title)
    elif "y-" in "".join(action) or " y " in "".join(action):
        ax.set_ylabel(this_title)
    # pickle.dump(plot,open('plot.pickle','wb'))
    return save_fig(plot, name=id)
# plot = set_ax_title(["add","y-title"],["This is an ax"])
# plt.show(plot)

def yy_change_color(action,values, id):
    colorlist =[ x[0] for x in matplotlib.colors.cnames.items()]
    this_color = 'black'
    for element in values:
        if element in colorlist:
            this_color = element
    plot = pickle.load(open('plot.pickle', 'rb'))
    ax = plot.get_axes()[0]
    children = ax.get_children()
    children[0].set_color(this_color)
    # pickle.dump(plot,open('plot.pickle','wb'))
    return save_fig(plot, name=id)
# plot = change_color(["change","final"],["red"])
# plt.show(plot)

def yy_add_line(action,values, id):
    data_list = pickle.load(open("plot_data.pickle","rb"))
    file,columns = values
    plot = pickle.load(open('plot.pickle', 'rb'))
    ax = plot.get_axes()[0]

    for data in columns:
        to_plot = file_to_column(file,data)
        data_list.append(to_plot)
        ax = plot.get_axes()[0]
        ax.plot(to_plot)
    return save_fig(plot, data=data_list,  name=id)
    # pickle.dump(plot,open('plot.pickle','wb'))
    # pickle.dump(data_list,open('plot_data.pickle','wb'))
    # return plot
# plot = add_line(["add","line"],("grades.csv",["Test1"]))
# plt.show(plot)

def yy_set_axis_range(action,values, id):
    start,end = values
    plot = pickle.load(open('plot.pickle', 'rb'))
    ax = plot.get_axes()[0]
    if "x-" in "".join(action) or " x " in "".join(action):
        ax.set_xlim(start,end)
    elif "y-" in "".join(action) or " y " in "".join(action):
        ax.set_ylim(start, end)
    # pickle.dump(plot,open('plot.pickle','wb'))
    return save_fig(plot, name=id)
    # return plot

def yy_set_n_ticks(action,values, id):
    for val in values:
        if val.isdigit():
            n = val

    plot = pickle.load(open('plot.pickle', 'rb'))
    ax = plot.get_axes()[0]
    if "x-" in "".join(action) or " x " in "".join(action):
        ax.set_xticks(np.arange(n))
    elif "y-" in "".join(action) or " y " in "".join(action):
        ax.set_yticks(np.arange(n))
    # pickle.dump(plot,open('plot.pickle','wb'))
    return save_fig(plot, name=id)
    # return plot

def yy_add_ticks_labels(action,values, id):
    data_list = pickle.load(open("plot_data.pickle","rb"))
    file,columns = values
    plot = pickle.load(open('plot.pickle', 'rb'))
    ax = plot.get_axes()[0]
    ticks = file_to_column(file,columns[0])
    if "x-" in "".join(action) or " x " in "".join(action):
        ax.set_xticks(np.arange(len(ticks)),ticks)
    elif "y-" in "".join(action) or " y " in "".join(action):
        ax.set_yticks(np.arange(len(ticks)),ticks)
    # pickle.dump(plot,open('plot.pickle','wb'))
    # pickle.dump(data_list,open('plot_data.pickle','wb'))
    # return plot
    return save_fig(plot, data=data_list, name=id)
# plot = add_ticks_labels(["set","x-","ticks"],("grades.csv",["First name"]))
# plt.show(plot)
