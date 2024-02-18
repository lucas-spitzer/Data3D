import pandas, bpy
from _objects import Bar, Text

class BarChart:
    """ Create a 3D bar chart by utilizing the Bar and Text classes. """

    def __init__(self, data, x_labels, y_values, title, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), text_color="#274472", bar_color="#274472"):
        """
        Initializes 3D bar chart with data, x_labels, y_label, title, location, rotation, scale, text_color, and bar_color.

        Parameters: 
            data (dataframe): Pandas dataframe containing all data for the 3D bar chart.
            x_labels (str): String of the column name for the x-axis labels.
            y_values (str): String of the column name for the y-axis labels.
            title (str): Title of the 3D bar chart.
            location (tuple): Location of the 3D bar chart. Default is (0.0, 0.0, 0.0), at the origin of the 3D scene.
            rotation (tuple): Rotation of the 3D bar chart. Default is (0.0, 0.0, 0.0), no rotation.
            scale (tuple): Scale of the 3D bar chart. Default is (1.0, 1.0, 1.0), a 3D bar chart with a scale of 1.
            text_color (str or dict): Color of the text objects. Dict translate to RGB and strings to Hex. Default is "#274472", a dark sahde of blue.
            bar_color (str or dict): Color of the bar objects. Dict translate to RGB and strings to Hex. Default is "#274472", a dark sahde of blue.
        """
        
        # create a function to confirm data is a dataframe.
        self.data = data
        # create a function to confirm y_labels are numerical / quantitative.
        self.x_labels = data[x_labels]
        self.y_values = data[y_values]
        self.x_col = x_labels
        self.y_col = y_values
        self.title = title
        self.location = location
        self.rotation = rotation
        self.scale = scale
        self.bar_color = bar_color
        self.text_color = text_color
        self.objects = []
        self.check_types()
        self.build()

    def build(self):
        """ Creates the 3D bar chart in the active scene. """

        bpy.ops.scene.new(type='NEW')
        bpy.context.scene.name = self.title

        # Sort and Scaling Algorithm
        df_sorted = self.data.sort_values(by=self.y_values, ascending=False)
        max_value = df_sorted[self.y_values].max()

        # Color Assignment Algorithm

        # Object Placement Algorithm
        x_position = (len(df_sorted) * -1) + 1
        for i in df_sorted:
            self.objects.append(Bar(name=df_sorted.iloc[i][self.x_col], location=(x_position, 0.0, 0.0), scale=(.25, .25, (df_sorted[self.y_col].iloc[i])/max_value), color=self.bar_color))
            x_position += 2
            


    def check_types(self):
        """ Checks the types of all parameters. If type is incorrect, a TypeError is raised."""

        if type(self.data) not in [pandas.DataFrame]:
            raise TypeError("Data must be a pandas dataframe.")
        if type(self.y_values) not in [int, float]:
            raise TypeError("Y-label must be a numerical value.")
        if type(self.x_labels) not in [str]:
            raise TypeError("X-labels must be a string.")
        if type(self.title) not in [str]:
            raise TypeError("Title must be a string.")
        if type(self.location) not in [tuple]:
            raise TypeError("Location must be a tuple.")
        if type(self.rotation) not in [tuple]:
            raise TypeError("Rotation must be a tuple.")
        if type(self.scale) not in [tuple]:
            raise TypeError("Scale must be a tuple.")
        if type(self.bar_color) not in [str, dict]:
            raise TypeError("Bar color must be a string or dictionary.")
        if type(self.text_color) not in [str, dict]:
            raise TypeError("Text color must be a string or dictionary.")




        