import bpy, math

class Bar:
    """ Create a singular bar object and adds the object to the active 3D scene. """

    def __init__(self, name, location=(0.0, 0.0, 1.0), rotation=(0.0, 0.0, 0.0), scale=(0.25, 0.25, 1.0), color="#274472"):
        """
        Initializes bar object with name, location, rotation, scale, and color.

        Parameters: 
            name (str): Name of the bar object. Name of the x-value element +  a "-Bar" suffix.
            location (tuple): Location of the bar object. Default is (0.0, 0.0, 1.0), at the origin of the 3D scene.
            rotation (tuple): Rotation of the bar object. Default is (0.0, 0.0, 0.0), no rotation.
            scale (tuple): Scale of the bar object. Default is (0.25, 0.25, 1.0), a bar with a base of 0.5 meters and a height of 2 meters.
            color (str or tuple): Color of the bar object. Tuples translate to RGB and strings to Hex. Default is "#274472", a dark sahde of blue.
        """
        self.name = name + "-Bar"
        self.location = location
        self.rotation = rotation
        self.scale = scale
        self.color = color
        self.create()

    def create(self):
        """ Creates the bar object in the active scene, sets the name, creates an accessor variable, and adds color to the object. """
        bpy.ops.mesh.primitive_cube_add(location=self.location, rotation=self.rotation, scale=self.scale)
        self.bar = bpy.context.object # Producing a accessor to the bar object.
        self.bar.name = self.name
        # Set the color of the bar object.


class Text:
    """ Create a singular text object and adds the object to the active 3D scene. """

    def __init__(self, name, text, axis, location=(0.0, 0.0, 2.0), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0), color="#000000"):
        """
        Initializes text object with name, text, location, rotation, scale, and color.

        Parameters: 
            name (str): Name of the text object. 
            text (str): Text to be displayed.
            location (tuple): Location of the text object. Default is (0.0, 0.0, 2.0), at the origin of the 3D scene.
            rotation (tuple): Rotation of the text object. Default is (0.0, 0.0, 0.0), no rotation.
            scale (tuple): Scale of the text object. Default is (1.0, 1.0, 1.0), a text with a scale of 1.
            color (str or tuple): Color of the text object. Tuples translate to RGB and strings to Hex. Default is "#000000", black.
        """
        self.axis = axis
        self.name = name + f"-{self.axis}Text"
        self.text = text
        self.location = location
        self.rotation = rotation
        self.scale = scale
        self.color = color
        self.create()

    def create(self):
        """ Creates the text object in the active scene, sets the name, creates an accessor variable, changes text value, and adds color to the object. """
        bpy.ops.object.text_add(location=self.location, rotation=self.rotation, scale=self.scale)
        self.text = bpy.context.object # Producing a accessor to the text object.
        self.text.data.body = self.text
        self.text.name = self.name
        # Set the color of the text object.

