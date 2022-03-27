"""
Author: Samuel Lehmann
Network with him at: https://www.linkedin.com/in/samuellehmann/
"""

import math
import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.spatial import ConvexHull
import numpy as np
import Field
import Main

# GUI Elements
window, figure, hover_label, mat_info_label, slope_field, slope_label, x_combo, y_combo = (None for i in range(8))

# Checkbox values
x_axis_checked, y_axis_checked, add_line_checked = (None for i in range(3))

update_graph_callback = None

#  AxisTypes
LOG, SEMILOGX, SEMILOGY, LINEAR = range(0, 4)
current_axis_type = LINEAR

LINE_CLOSENESS = 0.01
added_lines = []
initialized = False


def create_window(update_plot):
    global window, figure, x_combo, y_combo, add_line_checked, slope_field, slope_label, x_axis_checked, \
        y_axis_checked, update_graph_callback

    update_graph_callback = update_plot

    window = tk.Tk()
    window.title("OpenAshby: Material Property Charts")
    window.geometry("1000x1000")
    window.configure(bg="White")

    # Define and arrange GUI elements
    tk.Label(window, text="X-Axis: ", bg="White").place(x=350, y=10)

    x_combo = tk.ttk.Combobox(window, width=70, state='readonly')
    filtered_fields = list(Field.FIELDS[Field.FIELDS["Graphable"]]["Text"])
    x_combo['values'] = filtered_fields
    x_combo.place(x=400, y=10)
    x_combo.set(Main.DEFAULT_X_CAT)
    x_combo.bind("<<ComboboxSelected>>", update_graph_callback)

    tk.Label(window, text="Y-Axis: ", bg="White").place(x=350, y=50)

    y_combo = tk.ttk.Combobox(window, width=70, state='readonly')
    y_combo['values'] = filtered_fields
    y_combo.place(x=400, y=50)
    y_combo.set(Main.DEFAULT_Y_CAT)
    y_combo.bind("<<ComboboxSelected>>", update_graph_callback)

    add_line_checked = tk.IntVar()
    tk.Checkbutton(window, text="Add Line", variable=add_line_checked, command=add_lines_check_change,
                   bg="White").place(x=350,
                                     y=90)

    class RestrictedEntry(tk.Entry):
        """A child of the entry class that is restricted to only allow floats to be entered"""

        def __init__(self, master=None, **kwargs):
            self.var = tk.StringVar()
            tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
            self.old_value = ''
            self.var.trace('w', self.check)
            self.get, self.set = self.var.get, self.var.set

        def check(self, *args):
            try:
                float(self.get())
                # The current value is a valid float
                self.old_value = self.get()
                if add_line_checked.get() and not math.isclose(add_line_checked.get(), 0.0):
                    add_overlay_line(float(slope_field.get()))
            except ValueError:
                # Not a valid float -> reject
                self.set(self.old_value)

    slope_label = tk.Label(window, text="Line Slope: ", bg="White")
    slope_label.place(x=400, y=90)
    slope_label.place_forget()

    slope_field = RestrictedEntry(window, width=30)
    slope_field.insert(tk.END, "1")
    slope_field.place(x=440, y=90)
    slope_field.place_forget()

    x_axis_checked = tk.IntVar()
    y_axis_checked = tk.IntVar()
    tk.Checkbutton(window, text="Logarithmic X Axis", variable=x_axis_checked, command=axis_check_change,
                   bg="White").place(x=430, y=130)
    tk.Checkbutton(window, text="Logarithmic Y Axis", variable=y_axis_checked, command=axis_check_change,
                   bg="White").place(x=570, y=130)

    # Embed the plot in the tkinter window
    figure = plt.figure(figsize=(10, 8))
    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().place(x=0, y=150)


def add_lines_check_change():
    """Handles a change in the draw lines check box"""

    if add_line_checked.get():
        slope_label.place(x=440, y=90)
        slope_field.place(x=510, y=90)
        add_overlay_line(float(slope_field.get()))
    else:
        for line in added_lines:
            line.pop(0).remove()
        added_lines.clear()
        slope_field.place_forget()
        slope_label.place_forget()
        refresh()


def axis_check_change():
    """Handles a change in either of the logarithmic axis check boxes"""

    global current_axis_type
    if x_axis_checked.get():
        if y_axis_checked.get():
            current_axis_type = LOG
        else:
            current_axis_type = SEMILOGX
    else:
        if y_axis_checked.get():
            current_axis_type = SEMILOGY
        else:
            current_axis_type = LINEAR

    # Update the graph accordingly
    if initialized:
        update_graph_callback()


def identify_hovered_node(event):
    """Identifies if the passed event refers to a visible line. If yes, the x,y coordinates of this point are
    returned. If no, None is returned """

    for line in figure.gca().lines:
        cont, ind = line.contains(event)
        if cont:
            x, y = line.get_data()
            x = x[ind["ind"][0]]
            y = y[ind["ind"][0]]
            return x, y
    return None


def build_figure(x_cat, y_cat, hover_event=None, click_event=None):
    """Figure building: axes labeling/figure titling etc."""

    global hover_label, mat_info_label, initialized

    figure.clf()

    if hover_event:
        figure.canvas.mpl_connect("motion_notify_event", hover_event)
        figure.canvas.mpl_connect("button_press_event", click_event)

    plt.xlabel(x_cat)
    plt.ylabel(y_cat)
    plt.title(y_cat + " As a Function Of " + x_cat)

    hover_label = figure.get_axes()[0].annotate("", xy=(0, 0), xytext=(-20, 20), textcoords="offset points",
                                                bbox=dict(boxstyle="round", fc="w"),
                                                arrowprops=dict(arrowstyle="->"), ha="center")
    hover_label.set_visible(False)

    mat_info_label = figure.get_axes()[0].text(1, 1, "", transform=figure.get_axes()[0].transAxes,
                                               horizontalalignment="right", verticalalignment="top",
                                               bbox=dict(boxstyle="round", fc="w"))
    mat_info_label.set_visible(False)

    plt.grid()

    initialized = True


def add_overlay_line(slope):
    """Adds overlay lines with a given slope in accordance with the Ashby method"""

    for line in added_lines:
        line.pop(0).remove()
    added_lines.clear()

    old_x_lim = plt.xlim()
    old_y_lim = plt.ylim()

    primary_axes = figure.gca()

    # Overlay a new axis that is linear-linear over the old axis. This allows the plotting of straight lines with a
    # log or a semilog regular axis secondary_axis = figure.add_axes(figure.gca().get_position(), frameon=False)
    secondary_axis = figure.add_axes(plt.gca().get_position(), frameon=False)
    secondary_axis.get_xaxis().set_visible(False)
    secondary_axis.get_yaxis().set_visible(False)

    x = np.array(range(math.floor(old_x_lim[1])), dtype=np.float64)

    y = slope * x + 1
    added_lines.append(secondary_axis.plot(x, y, linestyle="dotted", color="gray"))

    plt.xlim(old_x_lim)
    plt.ylim(old_y_lim)
    figure.sca(primary_axes)

    refresh()


def add_to_plot(data_points, category):
    """Add datapoints to the plot, generates convex hulls, and labels them appropriately"""

    if current_axis_type == LOG:
        plt.loglog(data_points[:, 0], data_points[:, 1], label=category, linestyle="", marker="o")
    elif current_axis_type == SEMILOGX:
        plt.semilogx(data_points[:, 0], data_points[:, 1], label=category, linestyle="", marker="o")
        plt.ylim(bottom=0)
    elif current_axis_type == SEMILOGY:
        plt.semilogy(data_points[:, 0], data_points[:, 1], label=category, linestyle="", marker="o")
        plt.xlim(left=0)
    elif current_axis_type == LINEAR:
        plt.plot(data_points[:, 0], data_points[:, 1], label=category, linestyle="", marker="o")
        plt.xlim(left=0)
        plt.ylim(bottom=0)

    colour = plt.gca().lines[-1].get_color()

    # Convex hull based on category
    hull = ConvexHull(data_points)

    hull_points = [data_points[hull.vertices, 0], data_points[hull.vertices, 1]]
    hull_points[0] = np.concatenate((hull_points[0], [hull_points[0][0]]))
    hull_points[1] = np.concatenate((hull_points[1], [hull_points[1][0]]))

    plt.plot(hull_points[0], hull_points[1], color=colour)
    plt.fill_between(hull_points[0], hull_points[1], alpha=0.1, color=colour)

    # Make the label 2 lines if it is suitably long
    label_text = category
    if len(label_text) > 8:
        split_index = label_text.find(" ", 5, -1)
        if (split_index > 0):
            label_text = label_text[:split_index] + "\n" + label_text[split_index:]

    # Add Label
    plt.annotate(label_text, [np.median(data_points[:, 0]), np.median(data_points[:, 1])], color=colour,
                 weight="bold", backgroundcolor="#ffffff80", fontsize=8, va="center", ha='center')

    # recompute the ax.dataLim
    figure.gca().relim()
    # update ax.viewLim using the new dataLim
    figure.gca().autoscale()


def refresh():
    """Updates the plot so any changes are visible"""

    figure.canvas.draw()
    figure.canvas.flush_events()


def create_annotation(text, x, y):
    """Adds an annotation for a given text and x/y coordinate"""

    hover_label.xy = (x, y)
    hover_label.set_text(text)
    hover_label.get_bbox_patch().set_alpha(1)
    hover_label.set_visible(True)
    figure.canvas.draw_idle()


def create_mat_details(text):
    """Displays material details box for the given text"""

    mat_info_label.set_text(text)
    mat_info_label.get_bbox_patch().set_alpha(1)
    mat_info_label.set_visible(True)


def get_selected_categories():
    """Returns a tuple of the currently selected x and y categories"""

    return x_combo.get(), y_combo.get()


def hide_hover_annotation():
    hover_label.set_visible(False)


def hide_mat_details():
    mat_info_label.set_visible(False)


def start_loop():
    window.mainloop()
