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

bl_info = {
    "name": "SXL Bezier curve exporter",
    "author": "Ville Valtokari",
    "version": (1, 0, 0),
    "blender": (2, 71, 0),
    "location": "File > Export > Bezier curve (.sxl)",
    "description": "Export Bezier curves to SXL format for Megashapes "
                   "Unity plugin",
    "warning": "",
    "wiki_url": "https://github.com/denvil/io_scene_sxl",
    "category": "Import-Export",
}

# To support reload properly, try to access a package var,
# if it's there, reload everything
if "bpy" in locals():
    import imp
    if "export_sxl" in locals():
        imp.reload(export_sxl)

import bpy

from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       )
from bpy_extras.io_utils import ExportHelper, ImportHelper, axis_conversion


class ExportSXL(bpy.types.Operator, ExportHelper):

    """Save a SXL file"""

    bl_idname = "export_curve.sxl"
    bl_label = "Export SXL"
    bl_options = {'PRESET'}

    filename_ext = ".sxl"
    filter_glob = StringProperty(
        default="*.sxl",
        options={'HIDDEN'},
    )
    # context group
    use_selection = BoolProperty(
        name="Selection Only",
        description="Export selected curves only",
        default=True,
    )
    ignore_tilt = BoolProperty(
        name="Ignore Tilt",
        description="Don't export tilt",
        default=False,
    )
    axis_forward = EnumProperty(
        name="Forward",
        items=(('X', "X Forward", ""),
               ('Y', "Y Forward", ""),
               ('Z', "Z Forward", ""),
               ('-X', "-X Forward", ""),
               ('-Y', "-Y Forward", ""),
               ('-Z', "-Z Forward", ""),
               ),
        default='Z',
    )
    axis_up = EnumProperty(
        name="Up",
        items=(('X', "X Up", ""),
               ('Y', "Y Up", ""),
               ('Z', "Z Up", ""),
               ('-X', "-X Up", ""),
               ('-Y', "-Y Up", ""),
               ('-Z', "-Z Up", ""),
               ),
        default='Y',
    )
    global_scale = FloatProperty(
        name="Scale",
        min=0.01, max=1000.0,
        default=1.0,
    )

    def execute(self, context):
        from . import export_sxl
        from mathutils import Matrix
        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "global_scale",
                                            "filter_glob",
                                            "check_existing"))
        global_matrix = (Matrix.Scale(self.global_scale, 4) *
                         axis_conversion(to_forward=self.axis_forward,
                                         to_up=self.axis_up,
                                         ).to_4x4())

        keywords["global_matrix"] = global_matrix
        return export_sxl.save(self, context, **keywords)


def menu_func_export(self, context):
    self.layout.operator(ExportSXL.bl_idname, text="Bezier curve (.sxl)")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)

    bpy.types.INFO_MT_file_export.remove(menu_func_export)

    if __name__ == "__main__":
        register()
