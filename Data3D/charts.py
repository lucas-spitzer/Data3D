import bpy

class BarChart:
    """ Create a 3D bar chart by utilizing the Bar and Text classes. """

    def __init__(self, data, x_labels, y_label, title, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), text_color="#274472", bar_color="#274472"):
        """
        Initializes 3D bar chart with data, x_labels, y_label, title, location, rotation, scale, text_color, and bar_color.

        Parameters: 
            data (dataframe): Pandas dataframe containing all data for the 3D bar chart.
            x_labels (str): String of the column name for the x-axis labels.
            y_label (str): String of the column name for the y-axis labels.
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
        self.y_label = data[y_label]
        self.title = title
        self.location = location
        self.rotation = rotation
        self.scale = scale
        self.bar_color = bar_color
        self.build()

    def build(self):
        """ Creates the 3D bar chart in the active scene. """

        bpy.ops.scene.new(type='NEW')
        bpy.context.scene.name = self.title

        # Object Placement Algorithm




        