from cProfile import label
from statistics import mode
from textwrap import wrap
from turtle import color
import matplotlib.pyplot as plt
import os
import numpy as np
import argparse

# Basic Default Settings
input_location = "/home/aakash/Downloads/test.csv"
output_location = "/home/aakash/Downloads/test.svg"
chart_type = "line" # Options : line, scatter, bar, donut
bar_width = 0.5 # For bar chart
stacking = True
error_bars = False
show_mode = True
transparency = True

parser = argparse.ArgumentParser()
parser.add_argument("input_location", help="address of the input CSV data", type=str)
parser.add_argument("output_location", help="location to save the chart to", type=str)
parser.add_argument("type", help="type of chart", type=str)
parser.add_argument("--show", help="Show the chart instead of saving to file.", action="store_true")
parser.add_argument("--stacked", help="Stack the series in the chart", action="store_true")
parser.add_argument("--transparency", help="Make the chart background opaque", action="store_true")

args = parser.parse_args()

input_location = args.input_location
output_location = args.output_location
chart_type = args.type
show_mode = args.show
stacking = args.stacked
transparency = args.transparency

line_styles = ["","-","--"]
marker_styles = ["o","x","*"]


input_data = np.genfromtxt(input_location, delimiter=",")

data_point_quantiity = len(input_data)-2
series_quantity = input_data.shape[1]-1
print("Total data points = " + str(data_point_quantiity) + " | Series quantity = "  + str(series_quantity))

fig, ax = plt.subplots()

def list_sum(listt):
    sum = 0
    for element in listt:
        sum+=element
    return sum

def read_raw_column(col_index:int):
    """
    Reads a column directly from the CSV file, and returns it as an array of strings
    """
    filee = open(input_location, "r")
    read_data = filee.readlines()
    filee.close()

    raw_data = []
    for i in range(2,len(read_data)):
        raw_data.append(read_data[i].split(",")[col_index])
    
    return raw_data

def data_type(some_list):
    for element in some_list:
        if type(float(element)) != "float":
            return "string"
    
    for count in range(some_list):
        some_list[count] = float(some_list)
    
    return some_list

# Reading CSV Headers
filee = open(input_location, "r")
data = filee.readlines()
filee.close()

header_data = data[1].split(",")
title = data[0].split(",")[0]

if chart_type == "donut":
    # Read Independent data
    independent_param = read_raw_column(0)

    dependent_param = input_data[2:,1]

    wedges, texts = ax.pie(dependent_param, wedgeprops=dict(width=0.5), startangle=-40)

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72, facecolor="lightgrey", edgecolor="none")
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=0, va="center")
    
    labels = []
    for counter in range(len(independent_param)):
        labels.append(str(independent_param[counter]) + " : " + str(dependent_param[counter]) + "\n ("  +str(round(dependent_param[counter]*100/list_sum(dependent_param),2)) + " %)")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)

    font = {'family': 'serif',
        'color':  'black',
        'weight': 'bold',
        }
    #txt = plt.text(0.5, 0.5 title, wrap=True, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontdict=font, clip_on=False)
    #plt.legend(independent_param)
    #txt._get_wrap_line_width = lambda : 167
    plt.title(title.title(),y=1.08,fontdict=font)
    plt.text(0.5, 0.5, "\nvs\n".join(header_data),fontdict=font, va="center", ha="center", transform = ax.transAxes)

    if show_mode:    
        plt.show()
    else:
        plt.savefig(output_location, transparent=transparency, bbox_inches="tight")
    exit()
elif chart_type == "bar":
    if stacking == True:
        # Make stacked bar plot
        x_data = input_data[2:,0].tolist()
        cumu_y_data = np.zeros((1,data_point_quantiity),dtype=float)
        x_visible_data = (2*bar_width*np.array(list(range(1,1+data_point_quantiity*(series_quantity+1),series_quantity+1)))).tolist()  
        for count in range(len(input_data[0])-1):  
            y_data = input_data[2:,1+count].tolist()
            plt.bar(x_visible_data,y_data, label=header_data[count+1], bottom=cumu_y_data[0])
            cumu_y_data += np.array(y_data)
        plt.xticks(x_visible_data,x_data)
    else:
        # Make normal bar chart
        x_data = input_data[2:,0].tolist()

        # Show top values
        cumu_x_visible_data = np.zeros((1,data_point_quantiity),dtype=float)
        for count in range(len(input_data[0])-1):  
            y_data = input_data[2:,1+count].tolist()
            x_visible_data = (2*bar_width*np.array(list(range(1+count,1+data_point_quantiity*(series_quantity+1)+count,series_quantity+1)))).tolist()  
            plt.bar(x_visible_data,y_data, label=header_data[count+1])
            cumu_x_visible_data += np.array(x_visible_data)
        
        #ax.invert_xaxis()

        plt.xticks((np.array(cumu_x_visible_data)/series_quantity).tolist()[0],read_raw_column(0), rotation=45)
elif stacking == False:
    if chart_type == "line":
        chart_style = "-o"
    elif chart_type == "scatter":
        chart_style = "o"

    # Data Set to Plot
    x_data = input_data[2:,0].tolist()

    for count in range(len(input_data[0])-1):
        y_data = input_data[2:,1+count].tolist()
        plt.plot(x_data,y_data, chart_style)
elif stacking == True:
    # Data Set to Plot
    x_data = input_data[2:,0].tolist()

    all_y_data = []
    for count in range(len(input_data[0])-1):
        all_y_data.append(input_data[2:,1+count].tolist())
        
    plt.stackplot(x_data,*all_y_data)

if chart_type != "donut":
    # Plotting Data+
    plt.grid(color="white")
    plt.xlabel(header_data[0], fontdict={"weight":"bold"})
    plt.ylabel(header_data[1], fontdict={"weight":"bold"})

# Post Processing
plt.legend(header_data[1:])
plt.title(title, y=1.08, fontweight="bold")
ax.set_facecolor(color=(0.9,0.9,0.9,1))

ax.set_axisbelow(True)

# Showing Plot
if show_mode:
    plt.show()
else:
    # Save the plot to SVG
    plt.savefig(output_location, transparent=transparency, bbox_inches="tight")

#print(x_data, y_data)
