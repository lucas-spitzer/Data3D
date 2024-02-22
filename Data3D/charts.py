import pandas, bpy
from _objects import Bar, Text, Board

def _check_types(data, title, x_col, y_col, x_vals, y_vals, unit, bar_color, text_color):
    """ Checks the types of all parameters. If type is incorrect, a TypeError is raised. """

    if type(data) not in [pandas.DataFrame]:
        raise TypeError("Data must be a pandas dataframe.")
    if type(title) not in [str]:
        raise TypeError("Title must be a string.")
    if type(x_col) not in [str]:
        raise TypeError("X-Column identifier must be a string.")
    if type(y_col) not in [str]:
        raise TypeError("Y-Column identifier must be a string.")
    if type(x_vals) not in [pandas.Series] and not x_vals.apply(lambda x: isinstance(x, (str))).any():
        raise TypeError("X-Values must be string values within a pandas dataframe.")
    if type(y_vals) not in [pandas.Series] and not y_vals.apply(lambda x: isinstance(x, (float, int))).any():
        raise TypeError("Y-Values must be numerical values within a pandas dataframe.")
    if type(unit) not in [str]:
        raise TypeError("Unit must be a string.")
    if type(bar_color) not in [str, dict]:
        raise TypeError("Bar color must be a string or dictionary.")
    if type(text_color) not in [str]:
        raise TypeError("Text color must be a string or dictionary.")


def bar(data, x_col, y_col, unit="", title="", text_color='#F1F8FA', bar_color="#20318D"):
    """ Create a 3D bar chart by utilizing the Bar and Text classes.         
    
        Parameters: 
            data (dataframe): Pandas dataframe containing all data for the 3D bar chart.
            x_col (str): String of the column name for the x-axis labels.
            y_col (str): String of the column name for the y-axis labels.
            unit (str): String of the unit to be displayed on the y-axis labels. Default is an empty string.
            title (str): Title of the 3D bar chart.
            text_color (str): Hex color of the text object. Default is "#F1F8FA", off-white.
            bar_color (str or dict): Color of the bar objects. Dict translates key names to x_column string anmes to Hex. Default is "#20318D", a dark shade of blue.
    """

    # Dataframe Column Assignment to Variables
    x_vals = data[x_col]
    y_vals = data[y_col]

    # Type Conversion from Pandas to Python
    data[x_col] = data[x_col].astype('string')
    data[y_col] = data[y_col].apply(float)

    # Initialize List to Add Blender Objects
    objects = []

    # Type Checking Function
    _check_types(data, title, x_col, y_col, x_vals, y_vals, unit, bar_color, text_color)

    # Scene Creation Commands
    bpy.ops.scene.new(type='NEW')
    bpy.context.scene.name = title
    Board(name=title, text=title)

    # Data Sorting Algorithm
    df_sorted = data.sort_values(by=y_col, ascending=False)
    max_value = df_sorted[y_col].max()

    # Object Placement Algorithm
    unique = df_sorted[x_col].nunique()
    x_position = ((unique * -1) + 1) / 2

    # Color Assignment Algorithms and Bar Creation
    duplicate = False
    if type(bar_color) == str:
        for _, row in df_sorted.iterrows():
            for object in objects:
                if object.name == row[x_col] + "-Bar":
                    duplicate = True
                    break
            if duplicate:
                break
            z_scale = row[y_col]/max_value
            objects.append(Bar(name=row[x_col], location=(x_position, 0.0, z_scale), scale=(.25, .25, z_scale), color=bar_color))
            x_position += 1
    elif type(bar_color) == dict:
        for _, row in df_sorted.iterrows():
            for object in objects:
                if object.name == row[x_col] + "-Bar":
                    duplicate = True
                    break
            if duplicate:
                break
            z_scale = row[y_col]/max_value
            for color in bar_color:
                if row[x_col] == color:
                    objects.append(Bar(name=row[x_col], location=(x_position, 0.0, z_scale), scale=(.25, .25, z_scale), color=bar_color[color]))
            x_position += 1

    # Text Creation Algorithm
    duplicate = False
    axis = ["x", "y"]
    x_position = ((unique * -1) + 1) / 2
    for _, row in df_sorted.iterrows():
        for object in objects:
            if object.name == row[x_col] + "-xText" or object.name == row[x_col] + "-yText":
                duplicate = True
                break
        if duplicate:
            break
        z_scale = row[y_col]/max_value
        for ax in axis:
            if ax == "x":
                objects.append(Text(name=row[x_col], text=row[x_col], z_scale=z_scale, location=(x_position, -.251, 5.0), color=text_color, axis=ax, unit=unit))
            elif ax == "y":
                objects.append(Text(name=row[x_col], text=row[y_col], z_scale=z_scale, location=(x_position, -.251, 5.0), color=text_color, axis=ax, unit=unit))
        x_position += 1

    return objects


def animated_bar(data, x_col, y_col, dynamic, unit="", title="", text_color='#F1F8FA', bar_color="#20318D"):
    """ Create an animated 3D bar chart by utilizing the Bar and Text classes.         
    
        Parameters: 
            data (dataframe): Pandas dataframe containing all data for the 3D bar chart.
            x_labels (str): String of the column name for the x-axis labels.
            y_values (str): String of the column name for the y-axis labels.
            dynamic (str): String of the column name for the dynamic (actively changing) value.
            title (str): Title of the 3D bar chart.
            text_color (str): Hex color of the text object. Default is "#FAF9F6", off-white.
            bar_color (str or dict): Color of the bar objects. Dict translates key names to x_column string anmes to Hex. Default is "#20318D", a dark shade of blue.
    """

    # Create Traditional Bar Chart for Initial Frame
    bar(data, x_col, y_col, unit, title, text_color, bar_color)

    suffixes = ["-Bar", "-xText", "-yText"]
    for suffix in suffixes:
        active_object = bpy.data.objects.get(x_col + suffix)
        # Calculate and Assign Animation Keyframes
    # TBD: Create Animation for Dynamic Input Column