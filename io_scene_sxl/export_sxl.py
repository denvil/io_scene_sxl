# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import os
import bpy
import mathutils
import math
import bpy_extras.io_utils


def write_file(filepath, objects,
               path_mode='AUTO',
               ignore_tilt=False,
               global_matrix=None):
    """
    Write objects in Shape-Spline xml format.
    This exporter supports exporting all splines,
    but Megashapes supports only one spline.
    Also Tilt is exporter and with small modification to
    current Megashapes this value is used for Twist
    """

    if global_matrix is None:
        global_matrix = mathutils.Matrix()

    print('SXL Export path: %r' % filepath)
    file = open(filepath, "w", encoding="utf8", newline="\n")
    fw = file.write

    for shape in objects:

        fw("<Shape name=\"%s\">\n" % shape.name)
        for spline in shape.data.splines:
            closed_spline = 0

            # check if closed spline
            if spline.use_cyclic_u:
                closed_spline = 1

            fw("\t<Spline closed=\"%s\">\n" % closed_spline)

            # Write spline knots
            for point in spline.bezier_points:
                #convert radians to degrees
                tilt = math.degrees(point.tilt)
                if ignore_tilt:
                    tilt = 0

                #handle coordinate change
                point_co = global_matrix * point.co
                handle_left = global_matrix * point.handle_left
                handle_right = global_matrix * point.handle_right
                fw("\t\t<K p=\"%g %g %g\" i=\"%g %g %g\" o=\"%g %g %g\" t=\"%g\"/>\n" %
                    (point_co.x, point_co.y, point_co.z,
                     handle_left.x, handle_left.y, handle_left.z,
                     handle_right.x, handle_right.y, handle_right.z,
                     tilt))

            fw("\t</Spline>\n")
        fw("</Shape>\n")

    file.close()


def save(operator, context, filepath="",
         use_selection=True,
         ignore_tilt=False,
         global_matrix=None,
         path_mode='AUTO'):

    scene = context.scene
    # Exit edit mode
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    # Select only curve objects
    if use_selection:
        objects = [i for i in context.selected_objects if i.type == 'CURVE']
    else:
        objects = [i for i in scene.objects if i.type == 'CURVE']

    write_file(filepath, objects, path_mode, ignore_tilt, global_matrix)

    return {'FINISHED'}
