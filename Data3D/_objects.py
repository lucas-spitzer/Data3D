import bpy, math

class Bar:
    """ Create a singular bar object and adds the object to the active 3D scene. """

    def __init__(self, name, location=(0.0, 0.0, 1.0), rotation=(0.0, 0.0, 0.0), scale=(0.25, 0.25, 1.0), color="#20318D"):
        """
        Initializes bar object with name, location, rotation, scale, and color.

        Parameters: 
            name (str): Name of the bar object. Name of the x-value element +  a "-Bar" suffix.
            location (tuple): Location of the bar object. Default is (0.0, 0.0, 1.0), at the origin of the 3D scene.
            rotation (tuple): Rotation of the bar object. Default is (0.0, 0.0, 0.0), no rotation.
            scale (tuple): Scale of the bar object. Default is (0.25, 0.25, 1.0), a bar with a base of 0.5 meters and a height of 2 meters.
            color (str):  Hex color of the bar object. Default is "#20318D", a dark shade of blue.
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
        Material(self.name, self.color) # Set the color of the active bar object.


class Text:
    """ Create a singular text object and adds the object to the active 3D scene. """

    def __init__(self, name, text, axis, z_scale, location=(0.0, -.251, 1.0), rotation=(math.radians(90.0), 0.0, 0.0), color="#F1F8FA", unit=""):
        """
        Initializes text object with name, text, location, rotation, scale, and color.

        Parameters: 
            name (str): Name of the text object. 
            text (str): Text to be displayed.
            axis (str): Axis of the text object.
            z_scale (float): Scale of the z-axis.
            location (tuple): Location of the text object. Default is (0.0, -.251, 1.0), at the origin of the 3D scene.
            rotation (tuple): Rotation of the text object. Default is (90.0, 0.0, 0.0), no rotation.
            color (str): Hex color of the text object. Default is "#F1F8FA", off-white.
            unit (str): Unit of the text object. Default is an empty string.
        """

        self.axis = axis
        self.name = name + f"-{self.axis}Text"
        if unit == '':
            self.content = str(text)
        elif unit[0] == '.' and axis == "y":
            self.content =  str(text) + unit[1:]
        elif unit[-1] == '.' and axis == "y":
            self.content = unit[0] + str(text)
        elif unit[1] == '.' and axis == "y":
            self.content = unit[0] + str(text) + unit[2:]
        else:
            self.content = str(text)
        self.location = location
        self.rotation = rotation
        self.color = color
        self.z_scale = z_scale
        self.set_size()
        self.set_location()
        self.create()

    def create(self):
        """ Creates the text object in the active scene, sets the name, creates an accessor variable, changes text value, and adds color to the object. """

        bpy.ops.object.text_add(location=self.location, rotation=self.rotation)
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.data.align_x = 'CENTER'
        self.text = bpy.context.object # Producing a accessor to the text object.
        self.text.data.body = self.content
        self.text.data.size = self.size
        self.text.name = self.name
        Material(self.name, self.color) # Set the color of the active text object.

    def set_size(self):
        """ Scales the text object by the provided scale. """

        # Base Scaling Algorithm
        length = len(self.content)
        if length <= 5:
            self.size = .22 - (length * .02)
        elif length <= 15:
            self.size = .17 - (length * .01)
        else:
            raise ValueError("Text is too long to scale.")

    def set_location(self):
        """ Changes the z-location of the text object. """

        # Z Location Algorithm
        if self.axis == "x":
            self.location = (self.location[0], self.location[1], (self.z_scale * 2) - .2)
        elif self.axis == "y":
            self.location = (self.location[0], self.location[1], (self.z_scale * 2) - .4)
        elif self.axis == "z":
            self.location = (0, -.101, 2.45)
            self.size = .24
        else:
            raise ValueError("Axis must be either 'x' or 'y'.")

class Material:
    """ Create a singular material object and adds the material to the active object in a 3D scene. """

    def __init__(self, name, color):
        """
        Initializes material object with name and color.

        Parameters: 
            name (str): Name of the material object, based on objects the material is displayed on.
            color (str): Hex color of the material object.
        """

        self.name = name
        self.color = color
        self.create()

    def create(self):
        """ Creates the material object in the active scene, sets the name, creates an accessor variable, and adds color to the object. """

        if type(self.color) not in [str] or self.color[0] != "#" or len(self.color) != 7:
            raise TypeError("Color must be a string (Hex).")
        self.rgb = self.hex_to_rgb(self.color)
        self.material = bpy.data.materials.new(f"{self.name}-Material")
        self.material.diffuse_color = self.rgb
        active_object = bpy.data.objects.get(self.name)
        active_object.active_material = self.material

    def hex_to_rgb(self, value):
        """ Converts a hex color to a blender compatible RGB color. """

        gamma = 2.2
        value = value.lstrip('#')
        lv = len(value)
        rbg = list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        r = pow(rbg[0] / 255, gamma)
        g = pow(rbg[1] / 255, gamma)
        b = pow(rbg[2] / 255, gamma)
        rbg.clear()
        rbg.append(r)
        rbg.append(g)
        rbg.append(b)
        rbg.append(1.0)
        return tuple(rbg)
    

class Board:
    """ Overhead board object to display the title or dynamic value of the 3D bar chart. """

    def __init__(self, name, text, location=(0.0, 0.0, 2.5), scale=(1.0, .1, .2), color="#BDBDBD"):
        """
        Initializes board object with name, text, location, rotation, and color.

        Parameters: 
            name (str): Name of the board object. 
            text (str): Text to be displayed.
            location (tuple): Location of the board object. Default is (0.0, 0.0, 2.5), at the origin of the 3D scene.
            scale (tuple): Scale of the board object. Default is (1.0, .1, .2), a board with a legnth of 2 meters, width of .2 meters and a height of .4 meters.
            color (str): Hex color of the board object. Default is "#BDBDBD", a medium shade of gray.
        """

        self.name = name + "-Board"
        self.content = text
        self.location = location
        self.scale = scale
        self.color = color
        self.create()

    def create(self):
        """ Creates the board object in the active scene, sets the name, creates an accessor variable, changes text value, and adds color to the object. """

        bpy.ops.mesh.primitive_cube_add(location=self.location, scale=self.scale)
        self.board = bpy.context.object # Producing a accessor to the board object.
        self.board.name = self.name
        Material(self.name, self.color) # Set the color of the active board object.
        Text(self.name, self.content, "z", 0, color="#000000") # Set the text of the active board object.