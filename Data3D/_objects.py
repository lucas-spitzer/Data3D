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
        Material(self.color) # Set the color of the active bar object.


class Text:
    """ Create a singular text object and adds the object to the active 3D scene. """

    def __init__(self, name, text, axis, side, location=(0.0, 0.0, 1.0), rotation=(math.radians(90.0), 0.0, 0.0), scale=(0.25, 0.25, 5.0), color="#FAF9F6"):
        """
        Initializes text object with name, text, location, rotation, scale, and color.

        Parameters: 
            name (str): Name of the text object. 
            text (str): Text to be displayed.
            location (tuple): Location of the text object. Default is (0.0, 0.0, 2.0), at the origin of the 3D scene.
            rotation (tuple): Rotation of the text object. Default is (0.0, 0.0, 0.0), no rotation.
            scale (tuple): Scale of the text object. Default is (1.0, 1.0, 1.0), a text with a scale of 1.
            color (str): Hex color of the text object. Default is "#FAF9F6", off-white.
        """

        self.side = side
        self.axis = axis
        self.name = name + f"-{self.axis}Text-{self.side}"
        self.text = text
        self.location = location
        self.rotation = rotation
        self.scale = scale
        self.color = color
        self.scale()
        self.location()
        self.create()

    def create(self):
        """ Creates the text object in the active scene, sets the name, creates an accessor variable, changes text value, and adds color to the object. """

        bpy.ops.object.text_add(location=self.location, rotation=self.rotation, scale=self.scale)
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        self.text = bpy.context.object # Producing a accessor to the text object.
        self.text.data.body = self.text
        self.text.name = self.name
        Material(self.color) # Set the color of the active text object.

    def scale(self):
        """ Scales the text object by the provided scale. """

        # Base Scaling Algorithm
        length = len(self.text)

        if length <= 7:
            scale = .275 - (length * .025)
            self.text.scale = (scale, scale, 5.0)
        elif length == 8:
            scale = .09
            self.text.scale = (scale, scale, 5.0)
        elif length <= 10:
            scale = .09 - ((length - 8) * .025)
            self.text.scale = (scale, scale, 5.0)
        else:
            raise ValueError("Text is too long to scale.")
        

    def location(self):
        """ Changes the z-location of the text object. """

        # Z Location Algorithm
        if self.axis.lower() == "x":
            z_scale = self.scale[2]
            self.location[2] = (z_scale * 2) - .2
            if self.side == 'Front':
                self.location[1] = -.275
            elif self.side == 'Back':
                self.location[1] = .275
                self.rotation[2] = math.radians(180.0)
        elif self.axis.lower() == "y":
            z_scale = self.scale[2]
            self.location[2] = (z_scale * 2) - .4
        else:
            raise ValueError("Axis must be either 'x' or 'y'.")

class Material:
    """ Create a singular material object and adds the material to the active object in a 3D scene. """

    def __init__(self, name, color):
        """
        Initializes material object with name and color.

        Parameters: 
            color (str or tuple): Color of the material object. Tuples translate to RGB and strings to Hex. Default is off-white or dark blue depending on the object type.
        """

        self.name = name
        self.color = color
        self.create()

    def create(self):
        """ Creates the material object in the active scene, sets the name, creates an accessor variable, and adds color to the object. """

        if type(self.color) not in [str] or self.color[0] != "#" or len(self.color) != 7:
            raise TypeError("Color must be a string (Hex).")
        self.color = self.hex_to_rgb(self.color)
        self.material = bpy.data.materials.new(f"{self.name}-Material")
        self.material.diffuse_color = self.color
        active_object = bpy.data.objects.get(self.name)
        active_object.active_material = self.material

    def hex_to_rgb(value):
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