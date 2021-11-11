import bpy
import numpy as np
from batoms.butils import object_mode


class BaseObject():
    def __init__(self, obj_name):
        self.obj_name = obj_name
    @property
    def obj(self):
        return self.get_obj()
    def get_obj(self):
        return bpy.data.objects[self.obj_name]
    @property
    def location(self):
        return self.get_location()
    def get_location(self):
        return np.array(self.obj.location)
    @location.setter
    def location(self, location):
        self.set_location(location)
    def set_location(self, location):
        self.obj.location = location
    @property
    def type(self):
        return self.get_type()
    # this is weak, because not work for mesh object
    @type.setter
    def type(self, type):
        self.set_type(type)
    def get_type(self):
        return self.obj.data.type
    def set_type(self, type):
        self.obj.data.type = type.upper()
    @property
    def hide(self):
        return self.get_hide()
    @hide.setter
    def hide(self, state):
        self.set_hide(state)
    def get_hide(self):
        return self.obj.hide_get()
    def set_hide(self, state):
        self.obj.hide_render = state
        self.obj.hide_set(state)
    @property
    def select(self):
        return self.get_select()
    @select.setter
    def select(self, state):
        self.set_select(state)
    def get_select(self):
        return self.obj.select_get()
    def set_select(self, state):
        self.obj.select_set(state)
    @property
    def scene(self):
        return self.get_scene()
    def get_scene(self):
        return bpy.data.scenes['Scene']
    def translate(self, displacement):
        """Translate atomic positions.

        The displacement argument is an xyz vector.

        For example, move H species molecule by a vector [0, 0, 5]

        >>> h.translate([0, 0, 5])
        """
        object_mode()
        bpy.ops.object.select_all(action='DESELECT')
        self.obj.select_set(True)
        bpy.ops.transform.translate(value=displacement)
    def rotate(self, angle, axis = 'Z', orient_type = 'GLOBAL'):
        """Rotate atomic based on a axis and an angle.

        Parameters:

        angle: float
            Angle that the atoms is rotated around the axis.
        axis: str
            'X', 'Y' or 'Z'.

        For example, rotate h2o molecule 90 degree around 'Z' axis:
        
        >>> h.rotate(90, 'Z')

        """
        object_mode()
        bpy.ops.object.select_all(action='DESELECT')
        self.obj.select_set(True)
        bpy.ops.transform.rotate(value=angle, orient_axis=axis.upper(), 
                        orient_type = orient_type)
    def lock_to(self, obj = None):
        """
        track to obj
        """
        if obj is not None:
            self.obj.constraints.new(type = 'COPY_LOCATION')
            self.obj.constraints["Copy Location"].target = obj
            self.obj.constraints.new(type = 'COPY_ROTATION')
            self.obj.constraints["Copy Rotation"].target = obj
        else:
            for c in self.obj.constraints:
                self.obj.constraints.remove(c)

class BaseCollection():
    def __init__(self, name):
        self.name = name
    @property
    def coll(self):
        return self.get_coll()
    def get_coll(self):
        return bpy.data.collections[self.name]