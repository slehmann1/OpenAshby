"""
Author: Samuel Lehmann
Network with him at: https://www.linkedin.com/in/samuellehmann/
"""
import math
import pandas as pd
import numpy as np
import Field
import Interface

FILENANE = "MaterialDatabase.csv"
HULL_SEPARATOR = "Subcategory"
DEFAULT_X_CAT = "Elongation (%)"
DEFAULT_Y_CAT = "Ultimate Tensile Strength (MPa)"

mat_data, x_combo, y_combo = (None for i in range(3))
x_cat = DEFAULT_X_CAT
y_cat = DEFAULT_Y_CAT


def generate_plot():
    """Builds and populates the window. Uses x_cat & y_cat globals to define this"""

    Interface.build_figure(x_cat, y_cat, hover, click)
    subcats = mat_data[HULL_SEPARATOR].unique()

    for category in subcats:
        # Determine & Sanitize Data
        data_points = mat_data[mat_data[HULL_SEPARATOR] == category]
        data_points = np.array([data_points[x_cat].astype(float), data_points[y_cat].astype(float)]).T
        data_points = data_points[~np.isnan(data_points).any(axis=1)]

        if not (len(data_points)):
            continue

        Interface.add_to_plot(data_points, category)

    Interface.refresh()


def get_hover_text(x, y):
    """Provides the hover text for a given x, y coordinate based on the current x & y categories
    Returns None if no valid point at the x,y coordinates """

    filt_data = mat_data[mat_data[x_cat] == x]
    filt_data = filt_data[filt_data[y_cat] == y]

    try:
        if str(filt_data["Treatment or Temper"].iloc[0]) == "nan":
            return f'{filt_data["Name"].iloc[0]} \n ({x},{y}) \n Click For Details'

        return f'{filt_data["Name"].iloc[0]}, ' \
               f'{filt_data["Treatment or Temper"].iloc[0]} \n ({x},{y}) \n Click For Details'
    except IndexError:
        #The x,y coordinates do not correspond to a data point. Return None
        return None


def update_plot(*kwargs):
    """Updates the plot"""

    global x_cat, y_cat

    [x_cat, y_cat] = Interface.get_selected_categories()
    generate_plot()


def hover(event):
    """Handles actions when a data point is hovered over"""

    coords = Interface.identify_hovered_node(event)
    if coords:
        text = get_hover_text(coords[0], coords[1])
        Interface.create_annotation(text, coords[0], coords[1])


def click(event):
    """Handles actions when a data point is clicked"""

    coords = Interface.identify_hovered_node(event)
    if coords:
        text = (get_mat_info_text(coords[0], coords[1]))
        Interface.create_mat_details(text)
    else:
        Interface.hide_mat_details()


def get_mat_info_text(x, y):
    """Generates the text string for the detailed material information"""

    # Identifies the point selected
    filt_data = mat_data[mat_data[x_cat] == x]
    filt_data = filt_data[filt_data[y_cat] == y]
    filt_data = filt_data.iloc[0]

    # Large amounts of string processing
    # Note: many entries will be blank, hence the necessity

    return_string = f'Material  Name: {filt_data["Name"]}\n'
    if isinstance(filt_data[Field.get_text(Field.SUBCATEGORY)], str):
        if isinstance(filt_data[Field.get_text(Field.SUB_SUBCATEGORY)], str):
            return_string += f' Category: {filt_data[Field.get_text(Field.CATEGORY)]}, ' \
                             f'{filt_data[Field.get_text(Field.TYPE)]}, {filt_data[Field.get_text(Field.SUBCATEGORY)]}, ' \
                             f'{filt_data[Field.get_text(Field.SUB_SUBCATEGORY)]}  \n'
        else:
            return_string += f' Category: {filt_data[Field.get_text(Field.CATEGORY)]}, ' \
                         f'{filt_data[Field.get_text(Field.TYPE)]}, {filt_data[Field.get_text(Field.SUBCATEGORY)]}  \n'
    else:
        return_string += f' Category: {filt_data[Field.get_text(Field.CATEGORY)]}, ' \
                         f'{filt_data[Field.get_text(Field.TYPE)]}, {filt_data[Field.get_text(Field.SUBCATEGORY)]}\n'

    if isinstance(filt_data[Field.get_text(Field.TREATMENT)], str):
        if isinstance(filt_data[Field.get_text(Field.TREATMENT_TEMP_C)], str):
            return_string += f'Treatment: {filt_data[Field.get_text(Field.TREATMENT)]} ' \
                             f'With a treatment temperature of {filt_data[Field.get_text(Field.TREATMENT_TEMP_C)]} ' \
                             f'°C or {filt_data[Field.get_text(Field.TREATMENT_TEMP_F)]} °F'
        else:
            return_string += f'Treatment: {filt_data[Field.get_text(Field.TREATMENT)]}'

        if isinstance(filt_data[Field.get_text(Field.QUENCHED)], str):
            return_string += 'And Water Quenched'

        return_string += '\n'

    if not math.isnan(filt_data[Field.get_text(Field.UTS_PSI)]):
        if not math.isnan(filt_data[Field.get_text(Field.MIN_UTS_PSI)]):
            return_string += f'Ultimate Tensile Strength: Minimum: {filt_data[Field.get_text(Field.MIN_UTS_MPA)]} MPa ' \
                             f'({filt_data[Field.get_text(Field.MIN_UTS_PSI)] / 1000} ksi), Maximum: ' \
                             f'{filt_data[Field.get_text(Field.MAX_UTS_MPA)]} MPa ' \
                             f'({filt_data[Field.get_text(Field.MAX_UTS_PSI)] / 1000} ' \
                             f'ksi), Average: {filt_data[Field.get_text(Field.UTS_MPA)]} ' \
                             f'MPa ({filt_data[Field.get_text(Field.UTS_PSI)] / 1000} ksi)'
        else:
            return_string += f'Ultimate Tensile Strength: {filt_data[Field.get_text(Field.UTS_MPA)]} ' \
                             f'MPa ({filt_data[Field.get_text(Field.UTS_PSI)] / 1000} ksi)'
        return_string += '\n'

    if not math.isnan(filt_data[Field.get_text(Field.YS_PSI)]):
        if not math.isnan(filt_data[Field.get_text(Field.MIN_YS_PSI)]):
            return_string += f'Yield Strength: Minimum: {filt_data[Field.get_text(Field.MIN_YS_MPA)]} MPa ' \
                             f'({filt_data[Field.get_text(Field.MIN_YS_PSI)] / 1000} ksi), Maximum: ' \
                             f'{filt_data[Field.get_text(Field.MAX_YS_MPA)]} MPa ' \
                             f'({filt_data[Field.get_text(Field.MAX_YS_PSI)] / 1000} ' \
                             f'ksi), Average: {filt_data[Field.get_text(Field.YS_MPA)]} ' \
                             f'MPa ({filt_data[Field.get_text(Field.YS_PSI)] / 1000} ksi)'
        else:
            return_string += f'Yield Strength: {filt_data[Field.get_text(Field.YS_MPA)]} ' \
                             f'MPa ({filt_data[Field.get_text(Field.YS_PSI)]/1000} ksi)'
        return_string += '\n'

    if not math.isnan(filt_data[Field.get_text(Field.ELONGATION)]):
        if not math.isnan(filt_data[Field.get_text(Field.MIN_ELONGATION)]):
            return_string += f'Elongation: Minimum: {filt_data[Field.get_text(Field.MIN_ELONGATION)]}%, ' \
                             f'Maximum: {filt_data[Field.get_text(Field.MAX_ELONGATION)]}%, ' \
                             f'Average: {filt_data[Field.get_text(Field.ELONGATION)]}%'

        else:
            return_string += f'Percent Elongation: {filt_data[Field.get_text(Field.ELONGATION)]}% '
        return_string += '\n'

    if not math.isnan(filt_data[Field.get_text(Field.CSA_REDUCTION)]):
        return_string += f'Reduction in Cross-Sectional Area: {filt_data[Field.get_text(Field.CSA_REDUCTION)]}% \n'

    if not math.isnan(filt_data[Field.get_text(Field.BRINELL_HARDNESS)]):
        return_string += f'Brinell Hardness: {filt_data[Field.get_text(Field.BRINELL_HARDNESS)]}% \n'

    if isinstance(filt_data[Field.get_text(Field.ROCKWELL_HARDNESS)], str):
        return_string += f'Rockwell Hardness: {filt_data[Field.get_text(Field.ROCKWELL_HARDNESS)]}% \n'

    if not math.isnan(filt_data[Field.get_text(Field.IZOD_IMPACT_FTLB)]):
        return_string += f'Izod Impact Strength: {filt_data[Field.get_text(Field.IZOD_IMPACT_NM)]}Nm ' \
                         f'({filt_data[Field.get_text(Field.IZOD_IMPACT_Nm)]}ft-lb)\n'

    if not math.isnan(filt_data[Field.get_text(Field.ULT_SHEAR_MPA)]):
        return_string += f'Ultimate Shearing Strength: {filt_data[Field.get_text(Field.ULT_SHEAR_MPA)]}Nm ' \
                         f'({filt_data[Field.get_text(Field.ULT_SHEAR_PSI)]/1000}ksi)\n'

    if not math.isnan(filt_data[Field.get_text(Field.ENDURANCE_LIMIT_MPA)]):
        return_string += f'Endurance Limit: {filt_data[Field.get_text(Field.ENDURANCE_LIMIT_MPA)]}MPa ' \
                         f'({filt_data[Field.get_text(Field.ENDURANCE_LIMIT_KSI)]}ksi)\n'

    return_string += f'Material Data Source: {filt_data[Field.get_text(Field.DATA_SOURCE)]}'

    return return_string


if __name__ == '__main__':
    mat_data = pd.read_csv(FILENANE)
    Interface.create_window(update_plot)
    generate_plot()
    Interface.start_loop()
