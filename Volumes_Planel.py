from typing import Text
import bpy
from bpy.types import Context, Panel, PropertyGroup, Operator
from bpy_extras.io_utils import ExportHelper, ImportHelper
from bpy.props import StringProperty, BoolProperty, IntProperty

BoneList = [
     "c_trans",
     "c_head_jnt",
     "c_spine1_jnt",
     "c_spine2_jnt",
     "l_leg1_jnt",
     "r_leg1_jnt",
     "l_cla_jnt",
     "r_cla_jnt",
     "l_leg3_jnt",
     "r_leg3_jnt",
     "l_arm1_jnt",
     "r_arm1_jnt",
     "l_arm3_jnt",
     "r_arm3_jnt",
     "l_shldrArmr_jnt",
     "r_shldrArmr_jnt",
     "l_arm1vol_jnt",
     "r_arm1vol_jnt",
     "l_arm2vol_jnt",
     "r_arm2vol_jnt",
     "l_leg1vol_jnt",
     "l_leg2vol_jnt",
     "r_leg1vol_jnt",
     "r_leg2vol_jnt",
     "r_bust_jnt",
     "l_bust_jnt",
     "c_spine1vol_jnt",
     "c_spine2vol_jnt"
]

class FEVolumesPropGroup(PropertyGroup):
    ScaleAll        : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    ScaleHead       : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    ScaleNeck       : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    ScaleTorso      : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    ScaleShoulders  : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    ScaleArms       : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    ScaleHands      : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    ScaleLegs       : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    ScaleFeet       : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    VolumeArms      : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    VolumeLegs      : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    VolumeBust      : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    VolumeAbdomen   : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    VolumeTorso     : bpy.props.FloatProperty(default=1.0, min=0.1, max= 2.0) # type: ignore
    HipJointHeight  : bpy.props.FloatProperty(default=0.1098901, precision=7) # type: ignore

class FEVolumes_Apply(Operator):
    bl_idname = "fevolumes.apply"
    bl_label = "Apply"
    bl_description = "Apply volumes to Skeleton"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        volprops = context.scene.feengagevolumes
        if context.object != None and context.object.type == 'ARMATURE':
            Skele = context.object

            # Joints
            if Skele.pose.bones.get("c_trans").constraints.find("FEVolume") < 0:
                c_trans = Skele.pose.bones.get("c_trans").constraints.new("LIMIT_SCALE")
                c_trans.name = "FEVolume"
            else:
                c_trans = Skele.pose.bones.get("c_trans").constraints.get("FEVolume")
            SetJointValues(c_trans, volprops.ScaleAll * volprops.ScaleLegs)

            if Skele.pose.bones.get("c_head_jnt").constraints.find("FEVolume") < 0:
                c_head_jnt = Skele.pose.bones.get("c_head_jnt").constraints.new("LIMIT_SCALE")
                c_head_jnt.name = "FEVolume"
            else:
                c_head_jnt = Skele.pose.bones.get("c_head_jnt").constraints.get("FEVolume")
            SetJointValues(c_head_jnt, volprops.ScaleHead / volprops.ScaleNeck)

            if Skele.pose.bones.get("c_spine1_jnt").constraints.find("FEVolume") < 0:
                c_spine1_jnt = Skele.pose.bones.get("c_spine1_jnt").constraints.new("LIMIT_SCALE")
                c_spine1_jnt.name = "FEVolume"
            else:
                c_spine1_jnt = Skele.pose.bones.get("c_spine1_jnt").constraints.get("FEVolume")
            SetJointValues(c_spine1_jnt, ((volprops.ScaleLegs * 0.5 + 0.5) * ((volprops.ScaleTorso * 0.2 + 0.8) / volprops.ScaleLegs) / ((volprops.HipJointHeight * volprops.ScaleFeet - volprops.HipJointHeight) + 1.0)))

            if Skele.pose.bones.get("c_spine2_jnt").constraints.find("FEVolume") < 0:
                c_spine2_jnt = Skele.pose.bones.get("c_spine2_jnt").constraints.new("LIMIT_SCALE")
                c_spine2_jnt.name = "FEVolume"
            else:
                c_spine2_jnt = Skele.pose.bones.get("c_spine2_jnt").constraints.get("FEVolume")
            SetJointValues(c_spine2_jnt, ((volprops.ScaleTorso * 0.8 + 0.2) / (volprops.ScaleLegs * 0.5 + 0.5)))

            if Skele.pose.bones.get("l_leg1_jnt").constraints.find("FEVolume") < 0:
                l_leg1_jnt = Skele.pose.bones.get("l_leg1_jnt").constraints.new("LIMIT_SCALE")
                l_leg1_jnt.name = "FEVolume"
            else:
                l_leg1_jnt = Skele.pose.bones.get("l_leg1_jnt").constraints.get("FEVolume")
            SetJointValues(l_leg1_jnt, (1.0 / ((volprops.HipJointHeight * volprops.ScaleFeet - volprops.HipJointHeight) + 1.0)))

            if Skele.pose.bones.get("r_leg1_jnt").constraints.find("FEVolume") < 0:
                r_leg1_jnt = Skele.pose.bones.get("r_leg1_jnt").constraints.new("LIMIT_SCALE")
                r_leg1_jnt.name = "FEVolume"
            else:
                r_leg1_jnt = Skele.pose.bones.get("r_leg1_jnt").constraints.get("FEVolume")
            SetJointValues(r_leg1_jnt, (1.0 / ((volprops.HipJointHeight * volprops.ScaleFeet - volprops.HipJointHeight) + 1.0)))

            if Skele.pose.bones.get("l_cla_jnt").constraints.find("FEVolume") < 0:
                l_cla_jnt = Skele.pose.bones.get("l_cla_jnt").constraints.new("LIMIT_SCALE")
                l_cla_jnt.name = "FEVolume"
            else:
                l_cla_jnt = Skele.pose.bones.get("l_cla_jnt").constraints.get("FEVolume")
            SetJointValues(l_cla_jnt, volprops.ScaleShoulders)

            if Skele.pose.bones.get("r_cla_jnt").constraints.find("FEVolume") < 0:
                r_cla_jnt = Skele.pose.bones.get("r_cla_jnt").constraints.new("LIMIT_SCALE")
                r_cla_jnt.name = "FEVolume"
            else:
                r_cla_jnt = Skele.pose.bones.get("r_cla_jnt").constraints.get("FEVolume")
            SetJointValues(r_cla_jnt, volprops.ScaleShoulders)

            if Skele.pose.bones.get("l_leg3_jnt").constraints.find("FEVolume") < 0:
                l_leg3_jnt = Skele.pose.bones.get("l_leg3_jnt").constraints.new("LIMIT_SCALE")
                l_leg3_jnt.name = "FEVolume"
            else:
                l_leg3_jnt = Skele.pose.bones.get("l_leg3_jnt").constraints.get("FEVolume")
            SetJointValues(l_leg3_jnt, volprops.ScaleFeet)

            if Skele.pose.bones.get("r_leg3_jnt").constraints.find("FEVolume") < 0:
                r_leg3_jnt = Skele.pose.bones.get("r_leg3_jnt").constraints.new("LIMIT_SCALE")
                r_leg3_jnt.name = "FEVolume"
            else:
                r_leg3_jnt = Skele.pose.bones.get("r_leg3_jnt").constraints.get("FEVolume")
            SetJointValues(r_leg3_jnt, volprops.ScaleFeet)

            if Skele.pose.bones.get("l_arm1_jnt").constraints.find("FEVolume") < 0:
                l_arm1_jnt = Skele.pose.bones.get("l_arm1_jnt").constraints.new("LIMIT_SCALE")
                l_arm1_jnt.name = "FEVolume"
            else:
                l_arm1_jnt = Skele.pose.bones.get("l_arm1_jnt").constraints.get("FEVolume")
            SetJointValues(l_arm1_jnt, (volprops.ScaleArms / volprops.ScaleShoulders / volprops.ScaleTorso))

            if Skele.pose.bones.get("r_arm1_jnt").constraints.find("FEVolume") < 0:
                r_arm1_jnt = Skele.pose.bones.get("r_arm1_jnt").constraints.new("LIMIT_SCALE")
                r_arm1_jnt.name = "FEVolume"
            else:
                r_arm1_jnt = Skele.pose.bones.get("r_arm1_jnt").constraints.get("FEVolume")
            SetJointValues(r_arm1_jnt, (volprops.ScaleArms / volprops.ScaleShoulders / volprops.ScaleTorso))

            if Skele.pose.bones.get("l_arm3_jnt").constraints.find("FEVolume") < 0:
                l_arm3_jnt = Skele.pose.bones.get("l_arm3_jnt").constraints.new("LIMIT_SCALE")
                l_arm3_jnt.name = "FEVolume"
            else:
                l_arm3_jnt = Skele.pose.bones.get("l_arm3_jnt").constraints.get("FEVolume")
            SetJointValues(l_arm3_jnt, volprops.ScaleHands)

            if Skele.pose.bones.get("r_arm3_jnt").constraints.find("FEVolume") < 0:
                r_arm3_jnt = Skele.pose.bones.get("r_arm3_jnt").constraints.new("LIMIT_SCALE")
                r_arm3_jnt.name = "FEVolume"
            else:
                r_arm3_jnt = Skele.pose.bones.get("r_arm3_jnt").constraints.get("FEVolume")
            SetJointValues(r_arm3_jnt, volprops.ScaleHands)

            # Volumes
            if Skele.pose.bones.get("l_shldrArmr_jnt").constraints.find("FEVolume") < 0:
                l_shldrArmr_jnt = Skele.pose.bones.get("l_shldrArmr_jnt").constraints.new("LIMIT_SCALE")
                l_shldrArmr_jnt.name = "FEVolume"
            else:
                l_shldrArmr_jnt = Skele.pose.bones.get("l_shldrArmr_jnt").constraints.get("FEVolume")
            SetVolumeValues(l_shldrArmr_jnt, volprops.VolumeArms)

            if Skele.pose.bones.get("r_shldrArmr_jnt").constraints.find("FEVolume") < 0:
                r_shldrArmr_jnt = Skele.pose.bones.get("r_shldrArmr_jnt").constraints.new("LIMIT_SCALE")
                r_shldrArmr_jnt.name = "FEVolume"
            else:
                r_shldrArmr_jnt = Skele.pose.bones.get("r_shldrArmr_jnt").constraints.get("FEVolume")
            SetVolumeValues(r_shldrArmr_jnt, volprops.VolumeArms)

            if Skele.pose.bones.get("l_arm1vol_jnt").constraints.find("FEVolume") < 0:
                l_arm1vol_jnt = Skele.pose.bones.get("l_arm1vol_jnt").constraints.new("LIMIT_SCALE")
                l_arm1vol_jnt.name = "FEVolume"
            else:
                l_arm1vol_jnt = Skele.pose.bones.get("l_arm1vol_jnt").constraints.get("FEVolume")
            SetVolumeValues(l_arm1vol_jnt, volprops.VolumeArms)

            if Skele.pose.bones.get("r_arm1vol_jnt").constraints.find("FEVolume") < 0:
                r_arm1vol_jnt = Skele.pose.bones.get("r_arm1vol_jnt").constraints.new("LIMIT_SCALE")
                r_arm1vol_jnt.name = "FEVolume"
            else:
                r_arm1vol_jnt = Skele.pose.bones.get("r_arm1vol_jnt").constraints.get("FEVolume")
            SetVolumeValues(r_arm1vol_jnt, volprops.VolumeArms)

            if Skele.pose.bones.get("l_arm2vol_jnt").constraints.find("FEVolume") < 0:
                l_arm2vol_jnt = Skele.pose.bones.get("l_arm2vol_jnt").constraints.new("LIMIT_SCALE")
                l_arm2vol_jnt.name = "FEVolume"
            else:
                l_arm2vol_jnt = Skele.pose.bones.get("l_arm2vol_jnt").constraints.get("FEVolume")
            SetVolumeValues(l_arm2vol_jnt, volprops.VolumeArms)

            if Skele.pose.bones.get("r_arm2vol_jnt").constraints.find("FEVolume") < 0:
                r_arm2vol_jnt = Skele.pose.bones.get("r_arm2vol_jnt").constraints.new("LIMIT_SCALE")
                r_arm2vol_jnt.name = "FEVolume"
            else:
                r_arm2vol_jnt = Skele.pose.bones.get("r_arm2vol_jnt").constraints.get("FEVolume")
            SetVolumeValues(r_arm2vol_jnt, volprops.VolumeArms)

            if Skele.pose.bones.get("l_leg1vol_jnt").constraints.find("FEVolume") < 0:
                l_leg1vol_jnt = Skele.pose.bones.get("l_leg1vol_jnt").constraints.new("LIMIT_SCALE")
                l_leg1vol_jnt.name = "FEVolume"
            else:
                l_leg1vol_jnt = Skele.pose.bones.get("l_leg1vol_jnt").constraints.get("FEVolume")
            SetVolumeValues(l_leg1vol_jnt, volprops.VolumeLegs)

            if Skele.pose.bones.get("l_leg2vol_jnt").constraints.find("FEVolume") < 0:
                l_leg2vol_jnt = Skele.pose.bones.get("l_leg2vol_jnt").constraints.new("LIMIT_SCALE")
                l_leg2vol_jnt.name = "FEVolume"
            else:
                l_leg2vol_jnt = Skele.pose.bones.get("l_leg2vol_jnt").constraints.get("FEVolume")
            SetVolumeValues(l_leg2vol_jnt, volprops.VolumeLegs)

            if Skele.pose.bones.get("r_leg1vol_jnt").constraints.find("FEVolume") < 0:
                r_leg1vol_jnt = Skele.pose.bones.get("r_leg1vol_jnt").constraints.new("LIMIT_SCALE")
                r_leg1vol_jnt.name = "FEVolume"
            else:
                r_leg1vol_jnt = Skele.pose.bones.get("r_leg1vol_jnt").constraints.get("FEVolume")
            SetVolumeValues(r_leg1vol_jnt, volprops.VolumeLegs)

            if Skele.pose.bones.get("r_leg2vol_jnt").constraints.find("FEVolume") < 0:
                r_leg2vol_jnt = Skele.pose.bones.get("r_leg2vol_jnt").constraints.new("LIMIT_SCALE")
                r_leg2vol_jnt.name = "FEVolume"
            else:
                r_leg2vol_jnt = Skele.pose.bones.get("r_leg2vol_jnt").constraints.get("FEVolume")
            SetVolumeValues(r_leg2vol_jnt, volprops.VolumeLegs)

            if Skele.pose.bones.get("r_bust_jnt").constraints.find("FEVolume") < 0:
                r_bust_jnt = Skele.pose.bones.get("r_bust_jnt").constraints.new("LIMIT_SCALE")
                r_bust_jnt.name = "FEVolume"
            else:
                r_bust_jnt = Skele.pose.bones.get("r_bust_jnt").constraints.get("FEVolume")
            SetJointValues(r_bust_jnt, volprops.VolumeBust)

            if Skele.pose.bones.get("l_bust_jnt").constraints.find("FEVolume") < 0:
                l_bust_jnt = Skele.pose.bones.get("l_bust_jnt").constraints.new("LIMIT_SCALE")
                l_bust_jnt.name = "FEVolume"
            else:
                l_bust_jnt = Skele.pose.bones.get("l_bust_jnt").constraints.get("FEVolume")
            SetJointValues(l_bust_jnt, volprops.VolumeBust)

            if Skele.pose.bones.get("c_spine1vol_jnt").constraints.find("FEVolume") < 0:
                c_spine1vol_jnt = Skele.pose.bones.get("c_spine1vol_jnt").constraints.new("LIMIT_SCALE")
                c_spine1vol_jnt.name = "FEVolume"
            else:
                c_spine1vol_jnt = Skele.pose.bones.get("c_spine1vol_jnt").constraints.get("FEVolume")
            SetAbdomen(c_spine1vol_jnt, (volprops.VolumeAbdomen * 1.9 + -0.9), volprops.VolumeAbdomen)

            if Skele.pose.bones.get("c_spine2vol_jnt").constraints.find("FEVolume") < 0:
                c_spine2vol_jnt = Skele.pose.bones.get("c_spine2vol_jnt").constraints.new("LIMIT_SCALE")
                c_spine2vol_jnt.name = "FEVolume"
            else:
                c_spine2vol_jnt = Skele.pose.bones.get("c_spine2vol_jnt").constraints.get("FEVolume")
            SetVolumeValues(c_spine2vol_jnt, volprops.VolumeTorso)


        return {'FINISHED'}
        

class FEVloumes_Clear(Operator):
    bl_idname = "fevolumes.clear"
    bl_label = "Clear"
    bl_description = "Clear all volumes from Skeleton"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        volprops = context.scene.feengagevolumes
        if context.object != None and context.object.type == 'ARMATURE':
            Skele = context.object
            for bone in BoneList:
                if Skele.pose.bones.get(bone).constraints.find("FEVolume") >= 0:
                    Skele.pose.bones.get(bone).constraints.remove(Skele.pose.bones.get(bone).constraints.get("FEVolume"))

        return {'FINISHED'}

class FEVolumes_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FEEngageVolumes"
    bl_label = "Engage Volumes"

    def draw(self, context):
        volprops = context.scene.feengagevolumes
        layout = self.layout
        if context.object != None and context.object.type == 'ARMATURE':
            row = layout.row()
            row.label(text="FE Engage Volume Control")
            row = layout.row().split(factor=0.244)
            row.column().label(text='Target:')
            row.column().label(text=context.object.name, icon='ARMATURE_DATA')
            row = layout.row()
            row.column().operator('fevolumes.apply', text=FEVolumes_Apply.bl_label)
            row.column().operator('fevolumes.clear', text=FEVloumes_Clear.bl_label)
            row = layout.row()
            row.label(text="Joints")
            col = layout.column(align=True)
            col.prop(volprops, "ScaleAll")
            col.prop(volprops, "ScaleHead")
            col.prop(volprops, "ScaleNeck")
            col.prop(volprops, "ScaleTorso")
            col.prop(volprops, "ScaleShoulders")
            col.prop(volprops, "ScaleArms")
            col.prop(volprops, "ScaleHands")
            col.prop(volprops, "ScaleLegs")
            col.prop(volprops, "ScaleFeet")
            row = layout.row()
            row.label(text="Volumes")
            col = layout.column(align=True)
            col.prop(volprops, "VolumeArms")
            col.prop(volprops, "VolumeLegs")
            col.prop(volprops, "VolumeBust")
            col.prop(volprops, "VolumeAbdomen")
            col.prop(volprops, "VolumeTorso")
            row = layout.row()
            row.prop(volprops, "HipJointHeight")

        else:
            layout.label(text='No armature selected', icon='ERROR')


def SetVolumeValues(Constraint, value):
    Constraint.owner_space = 'LOCAL'
    Constraint.use_max_y = True
    Constraint.use_max_z = True
    Constraint.use_min_y = True
    Constraint.use_min_z = True
    Constraint.max_y = value
    Constraint.max_z = value
    Constraint.min_y = value
    Constraint.min_z = value

def SetJointValues(Constraint, value):
    Constraint.owner_space = 'LOCAL'
    Constraint.use_max_x = True
    Constraint.use_max_y = True
    Constraint.use_max_z = True
    Constraint.use_min_x = True
    Constraint.use_min_y = True
    Constraint.use_min_z = True
    Constraint.max_x = value
    Constraint.max_y = value
    Constraint.max_z = value
    Constraint.min_x = value
    Constraint.min_y = value
    Constraint.min_z = value

def SetAbdomen(Constraint, valueY, valueZ):
    Constraint.owner_space = 'LOCAL'
    Constraint.use_max_y = True
    Constraint.use_max_z = True
    Constraint.use_min_y = True
    Constraint.use_min_z = True
    Constraint.max_y = valueY
    Constraint.max_z = valueZ
    Constraint.min_y = valueY
    Constraint.min_z = valueZ