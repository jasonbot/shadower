# -*- coding: utf-8 -*-
import math
import os

import arcpy

def geometry_slices(geometry, xadd, yadd):
    for pt in geometry.getPart(0):
        if pt is None:
            return
        yield (pt, arcpy.Point(pt.X + xadd, pt.Y + yadd))

def window(iterator, window_size):
    window = ()
    for item in iterator:
        window += (item,)
        if len(window) >= window_size:
            yield window
            window = window[1:]

def shadow_geometry(geometry, xadd, yadd, in_sr):
    parts = []
    for w1, w2 in window(geometry_slices(geometry, xadd, yadd), 2):
        pt1, pt2 = w1
        pt3, pt4 = w2
        parts.append(
            arcpy.Polygon(
                arcpy.Array(
                    arcpy.Array([pt1, pt2, pt4, pt3, pt1])),
                in_sr))
    return reduce(lambda x, y: x.union(y), parts)

def make_shadows(in_fc, out_fc, angle, length, is_meters=False):
    in_sr = arcpy.Describe(in_fc).spatialReference
    arcpy.management.CreateFeatureclass(os.path.dirname(out_fc),
                                        os.path.basename(out_fc),
                                        'POLYGON',
                                        spatial_reference=in_sr)
    if is_meters:
        length /= in_sr.metersPerUnit
    radian_angle = math.radians(angle)
    xmul, ymul = math.sin(radian_angle), math.cos(radian_angle)
    xadd, yadd = length * xmul, length * ymul
    row_count = int(arcpy.management.GetCount(in_fc)[0])
    arcpy.AddMessage("Shadowing {} features".format(row_count))
    arcpy.SetProgressor("step", "Shadowing", 0, row_count)
    with arcpy.da.SearchCursor(in_fc, ['SHAPE@']) as in_cur, \
         arcpy.da.InsertCursor(out_fc, ['SHAPE@']) as out_cur:
        for row_idx, row in enumerate(in_cur):
            out_cur.insertRow([shadow_geometry(row[0], xadd, yadd, in_sr)])
            if row_idx % 100 == 1:
                arcpy.SetProgressorPosition(row_idx)

class Toolbox(object):
    def __init__(self):
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
        out_fc.direction = 'Output'
        out_fc.datatype = u'Feature Class'
        out_fc.symbology = os.path.join(os.path.dirname(__file__),
                                        "shadow_symbology.lyr")

        shadow_angle = arcpy.Parameter()
        shadow_angle.name = u'shadow_angle'
        shadow_angle.displayName = u'Angle in Degrees'
        shadow_angle.parameterType = 'Required'
        shadow_angle.direction = 'Input'
        shadow_angle.datatype = u'Double'
        shadow_angle.value = 45.

        shadow_length = arcpy.Parameter()
        shadow_length.name = u'shadow_length'
        shadow_length.displayName = u'Length of Shadow'
        shadow_length.parameterType = 'Required'
        shadow_length.direction = 'Input'
        shadow_length.datatype = u'Double'
        shadow_length.value = 0.0125

        length_units = arcpy.Parameter()
        length_units.name = u'length_units'
        length_units.displayName = u'Length is in'
        length_units.parameterType = 'Required'
        length_units.direction = 'Input'
        length_units.datatype = u'String'
        length_units.filter.list = ['Map Units', 'Meters']
        length_units.value = 'Map Units'
        length_units.enabled = False

        return [in_layer, out_fc, shadow_angle, shadow_length, length_units]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        pass

    def updateMessages(self, parameters):
        pass

    def execute(self, parameters, messages):
        in_fc = parameters[0].valueAsText
        out_fc = parameters[1].valueAsText
        angle = parameters[2].value
        length = parameters[3].value
        make_shadows(in_fc, out_fc, angle, length, is_meters=False)