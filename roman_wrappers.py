import shutil
import pickle
import pandas
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import uuid
import os
import matplotlib.patches as mpatches
import random
def save_fig(fig, plot_id, data=None):
    path = os.path.join("static", "plots", plot_id)
    fig.savefig(path+"/plot.png", format="png")
    pickle.dump(fig, open(path + "/plot.pickle", "wb"))
    if data:
        pickle.dump(data, open(path + "/data.pickle", "wb"))
    return plot_id 

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
def xx_draw_plot(actions, values, plot_id):
    """
    values is a tuple (datafile, columns)
    action is a list of words
    """
    print(f"actions: {actions}")
    file, columns = values
    print(f"wrapper {columns}")
    file = os.path.join("static", "plots", plot_id, "data.csv")
    fig = plt.figure()
    to_plot = []
    colorlist =[ x[0] for x in matplotlib.colors.cnames.items()]
    patches = []
    columns_in_data = []
    if "line" in actions:
        print("DOING LINE")
        for index,data in enumerate(columns):
            columns_in_data.append(data)
            to_plot = file_to_column(file,data)
            print(f"{to_plot}")
            this_color = random.choice(colorlist)
            plt.plot(to_plot, color=this_color)
            colorlist.remove(this_color)
            patches.append(mpatches.Patch(color=this_color, label = data))
    elif "scatter" in actions:
        print("DOING SCATTER")
        to_plot = []
        for data in columns:
            columns_in_data.append(data)
            this_plot = file_to_column(file,data)
            to_plot.append(this_plot)
        plt.scatter(*to_plot)

    elif "histogram" in actions or 'bar' in actions:
        print("DOING HISTOGRAM")
        to_plot = []
        for index,data in enumerate(columns):
            columns_in_data.append(data)
            to_plot = file_to_column(file,data)
            this_color = random.choice(colorlist)
            colorlist.remove(this_color)
            patches.append(mpatches.Patch(color=this_color, label = data))
            plt.hist(to_plot, color=this_color,alpha=0.7)
    plt.legend(handles=patches)
    return save_fig(fig, plot_id, data=(columns_in_data,to_plot))

#plot =xx_draw_plot(["draw", "scatter", "plot"], ("grades.csv",["Test2","Final"]),"AA")
#plt.show(plot)
# plot =xx_draw_plot(["draw", "line", "plot"], ("grades.csv",["Test2","Final"]),"AA")
# plt.show(plot)
#plot =xx_draw_plot(["draw", "histogram", "plot"], ("grades.csv",["Final"]),"AA")
#plt.show(plot)

def yy_add_title(action, values, plot_id):
    maxl = -1
    this_title = ""
    for elements in values:
        if len(elements)> maxl:
            this_title = elements
            maxl = len(this_title)
    plot = pickle.load(open("static/plots/"+str(plot_id)+"/plot.pickle",'rb'))
    print(this_title)
    plot.suptitle(this_title)
    # pickle.dump(plot,open('plot.pickle','wb'))
    return save_fig(plot, plot_id)
# plot = yy_add_title(["add","title"],["This is a title"],"AA")
# plt.show()

def yy_set_ax_title(action,values, plot_id):
    maxl = -1
    this_title = ""
    for elements in values:
        if len(elements) > maxl:
            this_title = elements
    plot = pickle.load(open("static/plots/"+str(plot_id)+"/plot.pickle",'rb'))
    ax = plot.get_axes()[0]
    if "x-" in "".join(action) or " x " in "".join(action):
        ax.set_xlabel(this_title)
    elif "y-" in "".join(action) or " y " in "".join(action):
        ax.set_ylabel(this_title)
    # pickle.dump(plot,open('plot.pickle','wb'))
    return save_fig(plot, plot_id)
# plot = yy_set_ax_title(["add","y-title"],["This is an ax"],"AA")
# plt.show(plot)

def yy_change_color(action,values, plot_id):
    colorlist =[ x[0] for x in matplotlib.colors.cnames.items()]
    this_color = 'black'
    for element in values:
        if element in colorlist:
            this_color = element
    plot = pickle.load(open("static/plots/"+str(plot_id)+"/plot.pickle",'rb'))
    ax = plot.get_axes()[0]
    children = ax.get_children()
    print(len(children))
    if len(children)<=12:
        children[0].set_color(this_color)
    else:
        data = pickle.load(open("static/plots/" + str(plot_id) + "/data.pickle", 'rb'))
        cols = data[0]
        #print(data)
        for index, col in enumerate(cols):
            new_patches = []
            if col in action or col in values:
                children[index].set_color(this_color)
                L=ax.get_legend()
                L.set_visible(False)

    # pickle.dump(plot,open('plot.pickle','wb'))
    return save_fig(plot, plot_id)
# plot = yy_change_color(["change","Final"],["red"], "AA")
# plt.show(plot)

def yy_add_line(action,values, plot_id):
    data = pickle.load(open("static/plots/" + str(plot_id) + "/data.pickle", 'rb'))
    data_headers = data[0]
    data_list = data[1]
    file,columns = values
    plot = pickle.load(open("static/plots/"+str(plot_id)+"/plot.pickle",'rb'))
    ax = plot.get_axes()[0]

    for data in columns:
        to_plot = file_to_column(file,data)
        data_list.append(to_plot)
        data_headers=data
        ax = plot.get_axes()[0]
        ax.plot(to_plot)
    return save_fig(plot, plot_id, data=(data_headers,data_list))
    # pickle.dump(plot,open('plot.pickle','wb'))
    # pickle.dump(data_list,open('plot_data.pickle','wb'))
    # return plot
# plot = yy_add_line(["add","line"],("grades.csv",["Test1"]),"AA")
# plt.show(plot)

def yy_set_axis_range(action,values, plot_id):
    start,end = values
    start = start
    end = end
    plot = pickle.load(open("static/plots/"+str(plot_id)+"/plot.pickle",'rb'))
    ax = plot.get_axes()[0]
    if "x-" in "".join(action) or " x " in "".join(action):
        ax.set_xlim(start,end)
    elif "y-" in "".join(action) or " y " in "".join(action):
        ax.set_ylim(start, end)
    # pickle.dump(plot,open('plot.pickle','wb'))
    return save_fig(plot, plot_id)
    # return plot

# plot = yy_set_axis_range(["add","y-title"],[0,5],"AA")
# plt.show(plot)


def yy_set_n_ticks(action,values, plot_id):
    values = [i for i in values]
    for val in values:
        if str(val).isdigit():
            n = val

    plot = pickle.load(open("static/plots/"+str(plot_id)+"/plot.pickle",'rb'))
    ax = plot.get_axes()[0]
    if "x-" in "".join(action) or " x " in "".join(action):
        ax.set_xticks(np.arange(n))
    elif "y-" in "".join(action) or " y " in "".join(action):
        ax.set_yticks(np.arange(n))
    # pickle.dump(plot,open('plot.pickle','wb'))
    return save_fig(plot, plot_id)
    # return plot
# plot = yy_set_n_ticks(["set","y-ticks"],[40],"AA")
# plt.show(plot)
#def yy_add_ticks_labels(action,values, id):
#    data_list = pickle.load(open("plot_data.pickle","rb"))
#    file,columns = values
#    plot = pickle.load(open('plot.pickle', 'rb'))
#    ax = plot.get_axes()[0]
#    ticks = file_to_column(file,columns[0])
#    if "x-" in "".join(action) or " x " in "".join(action):
#        ax.set_xticks(np.arange(len(ticks)),ticks)
#    elif "y-" in "".join(action) or " y " in "".join(action):
#        ax.set_yticks(np.arange(len(ticks)),ticks)
##    # pickle.dump(plot,open('plot.pickle','wb'))
#    # pickle.dump(data_list,open('plot_data.pickle','wb'))
#    # return plot
#    return save_fig(plot, data=data_list, name=id)
#plot = add_ticks_labels(["set","x-","ticks"],("grades.csv",["First name"]))
#plt.show(plot)
