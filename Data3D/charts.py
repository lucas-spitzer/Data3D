import pandas, bpy
from _objects import Bar, Text, Board

class BarChart:
    """ Create a 3D bar chart by utilizing the Bar and Text classes. """

    def __init__(self, data, x_labels, y_values, unit="", title="", text_color='#F1F8FA', bar_color="#20318D"):
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
            text_color (str): Hex color of the text object. Default is "#F1F8FA", off-white.
            bar_color (str or dict): Color of the bar objects. Dict translates key names to x_column string anmes to Hex. Default is "#20318D", a dark shade of blue.
        """
        
        self.data = data
        data[x_labels] = data[x_labels].astype('string')
        self.x_labels = data[x_labels]
        data[y_values] = data[y_values].apply(float)
        self.y_values = data[y_values]
        self.x_col = x_labels
        self.y_col = y_values
        self.title = title
        self.bar_color = bar_color
        self.text_color = text_color
        self.unit = unit
        self.objects = []
        self.check_types()
        self.build()


    def build(self):
        """ Creates the 3D bar chart in the active scene. """

        bpy.ops.scene.new(type='NEW')
        bpy.context.scene.name = self.title
        Board(name=self.title, text=self.title)

        # Sort and Scaling Algorithm
        df_sorted = self.data.sort_values(by=self.y_col, ascending=False)
        max_value = df_sorted[self.y_col].max()
        
        # Object Placement Algorithm
        x_position = ((len(df_sorted) * -1) + 1) / 2

        # Color Assignment Algorithms and Bar Creation
        if type(self.bar_color) == str:
            for _, row in df_sorted.iterrows():
                z_scale = row[self.y_col]/max_value
                self.objects.append(Bar(name=row[self.x_col], location=(x_position, 0.0, z_scale), scale=(.25, .25, z_scale), color=self.bar_color))
                x_position += 1
        elif type(self.bar_color) == dict:
            for _, row in df_sorted.iterrows():
                z_scale = row[self.y_col]/max_value
                for color in self.bar_color:
                    if row[self.x_col] == color:
                        self.objects.append(Bar(name=row[self.x_col], location=(x_position, 0.0, z_scale), scale=(.25, .25, z_scale), color=self.bar_color[color]))
                x_position += 1
        
        # Text Creation Algorithm
        axis = ["x", "y"]
        x_position = ((len(df_sorted) * -1) + 1) / 2
        for _, row in df_sorted.iterrows():
            z_scale = row[self.y_col]/max_value
            for ax in axis:
                if ax == "x":
                    self.objects.append(Text(name=row[self.x_col], text=row[self.x_col], z_scale=z_scale, location=(x_position, -.251, 5.0), color=self.text_color, axis=ax, unit=self.unit))
                elif ax == "y":
                    self.objects.append(Text(name=row[self.x_col], text=row[self.y_col], z_scale=z_scale, location=(x_position, -.251, 5.0), color=self.text_color, axis=ax, unit=self.unit))
            x_position += 1


    def check_types(self):
        """ Checks the types of all parameters. If type is incorrect, a TypeError is raised."""

        if type(self.data) not in [pandas.DataFrame]:
            raise TypeError("Data must be a pandas dataframe.")
        if type(self.title) not in [str]:
            raise TypeError("Title must be a string.")
        if type(self.bar_color) not in [str, dict]:
            raise TypeError("Bar color must be a string or dictionary.")
        if type(self.text_color) not in [str]:
            raise TypeError("Text color must be a string or dictionary.")
        
        # WRITE A FUNCTION TO CHECK IF THE X_LABELS ARE STRINGS AND Y_LABELS ARE NUMERICAL.
        # Dataframe types complicate this process.


class AnimatedBarChart(BarChart):
    """ Create an animated 3D bar chart by utilizing the Bar and Text classes. """

    def __init__(self, data, x_labels, y_values, dynamic, title="", text_color="#F1F8FA", bar_color="#20318D"):
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
            text_color (str): Hex color of the text object. Default is "#FAF9F6", off-white.
            bar_color (str or dict): Color of the bar objects. Dict translates key names to x_column string anmes to Hex. Default is "#20318D", a dark shade of blue.
        """
        
        super().__init__(data, x_labels, y_values, title, text_color, bar_color)
        self.dynamic = data[dynamic]
        self.dynamic_col = dynamic
        self.animate()
        Board(name=self.title, text=self.dynamic_col) # Dynamic not col later on.


    def animate(self):
        """ Animates the 3D bar chart by utilizing the Bar and Text classes. """

        self.full_data = self.data
        min_date = self.data['Date'].min()
        self.data = self.data[self.data['Date'] == min_date] # Mimimun date dataframe.

        super().build()
        # Animation Algorithm