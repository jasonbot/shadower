# -*- coding: utf-8 -*-
import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = u'Create Shadows'
        self.alias = u'shadows'
        self.tools = [MakeShadows]

class MakeShadows(object):
    def __init__(self):
        self.label = u'Make Shadows'
        self.canRunInBackground = False
    def getParameterInfo(self):
        in_layer = arcpy.Parameter()
        in_layer.name = u'in_layer'
        in_layer.displayName = u'Input Layer'
        in_layer.parameterType = 'Required'
        in_layer.direction = 'Input'
        in_layer.datatype = u'Feature Layer'

        out_fc = arcpy.Parameter()
        out_fc.name = u'out_fc'
        out_fc.displayName = u'Output Feature Class'
        out_fc.parameterType = 'Required'
        out_fc.direction = 'Input'
        out_fc.datatype = u'Feature Class'

        shadow_angle = arcpy.Parameter()
        shadow_angle.name = u'shadow_angle'
        shadow_angle.displayName = u'Angle in Degrees'
        shadow_angle.parameterType = 'Required'
        shadow_angle.direction = 'Input'
        shadow_angle.datatype = u'Double'

        shadow_length = arcpy.Parameter()
        shadow_length.name = u'shadow_length'
        shadow_length.displayName = u'Length of Shadow'
        shadow_length.parameterType = 'Required'
        shadow_length.direction = 'Input'
        shadow_length.datatype = u'Double'

        length_units = arcpy.Parameter()
        length_units.name = u'length_units'
        length_units.displayName = u'Length is in'
        length_units.parameterType = 'Required'
        length_units.direction = 'Input'
        length_units.datatype = u'String'
        length_units.filter.list = [u'Map Units', u'Meters']

        return [in_layer, out_fc, shadow_angle, shadow_length, length_units]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        pass

    def updateMessages(self, parameters):
        pass

    def execute(self, parameters, messages):
        raise NotImplementedError("Sorry.")

def makeshadows(in_fc, out_fc, angle, length):
    arcpy.AddMessage("HI! {} {} {} {}".format(in_fc, out_fc, angle, length))