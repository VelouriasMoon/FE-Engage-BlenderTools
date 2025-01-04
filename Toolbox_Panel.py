from typing import Text
import bpy
from bpy.types import Context, Panel, PropertyGroup, Operator
from bpy_extras.io_utils import ExportHelper, ImportHelper
from bpy.props import StringProperty, BoolProperty, IntProperty

LocDic = {
    "camLookAt_loc": "c_trans",
    "camFollow_loc": "c_trans",
    "reserve1_loc": "c_trans",
    "reserve2_loc": "c_trans",
    "reserve3_loc": "c_trans",
    "reserve4_loc": "c_trans",
    "proportion_loc": "c_trans",
    "c_spine2_loc": "c_spine2_jnt",
    "c_head_loc": "c_head_jnt",
    "c_head2_loc": "c_head_jnt",
    "c_hip_loc": "c_hip_jnt",
    "lookAt_loc": "c_hip_jnt",
    "l_swdbox_loc": "c_hip_jnt",
    #"l_swdgrip_loc": "l_swdbox_loc",
    "l_leg_loc": "l_leg4_jnt",
    "r_leg_loc": "r_leg4_jnt",
    "l_shld_loc": "l_arm2_jnt",
    "l_wpn1_loc": "l_arm3_jnt",
    "r_wpn1_loc": "r_arm3_jnt",
}

class FETools_FixLocators(Operator):
    bl_idname = "fetools.fixloc"
    bl_label = "Fix Locators"
    bl_description = "Fixes Locator's parents"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if context.object != None and context.object.type == 'ARMATURE':
            Skele = context.object
            for obj in bpy.data.objects:
                if obj.type == 'EMPTY':
                    if obj.name in LocDic:
                        if obj.name == "l_swdgrip_loc":
                            if "l_swdbox_loc" in bpy.data.objects:
                                obj.parent = bpy.data.objects["l_swdbox_loc"]
                            else:
                                self.report({'INFO'}, f"Parent Locator for loc '{obj.name}' missing, expected 'l_swdbox_loc'")
                        elif LocDic[obj.name] in Skele.data.bones:
                            obj.parent = Skele
                            obj.parent_type = 'BONE'
                            obj.parent_bone = LocDic[obj.name]
                        else:
                            self.report({'INFO'}, f"Parent Bone for loc '{obj.name}' missing, expected '{LocDic[obj.name]}'")


        return {'FINISHED'}

class FETools_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FE Engage"
    bl_label = "Engage Tools"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Locator Fixer")
        if context.object != None and context.object.type == 'ARMATURE':
            row = layout.row().split(factor=0.244)
            row.column().label(text='Target:')
            row.column().label(text=context.object.name, icon='ARMATURE_DATA')
            row = layout.row()
            row.operator('fetools.fixloc', text=FETools_FixLocators.bl_label)
        else:
            layout.label(text='No armature selected', icon='ERROR')