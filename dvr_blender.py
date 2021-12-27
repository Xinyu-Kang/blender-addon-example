bl_info = {
    "name": "DVR",
    "blender": (2, 93, 4),
    "category": "Object",
}

import os
import subprocess as sp
import bpy
import time
import yaml
from math import radians
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

ABS_PATH = "<some path>/differentiable_volumetric_rendering/" # replace with your path

class DVR(Operator):

    bl_idname = "run.dvr"
    bl_label = "Run DVR"
    bl_options = {'REGISTER', 'UNDO'}
    
    directory: StringProperty(subtype="DIR_PATH")
    use_filter_folder = True

    def execute(self, context):
        """Run DVR on the selected input folder"""     
        t0 = time.time()     
        data_path = self.directory
        out = "out/blender/" + data_path.split('\\')[-2]
        config = {"inherit_from": "configs/single_view_reconstruction/multi_view_supervision/ours_combined_pretrained.yaml",
                  "data": {"dataset_name": "images", "path": data_path},
                  "training": {"out_dir": out},
                  "generation": {"generation_dir": "generation"}}
        config_path = ABS_PATH + "configs/blender/blender.yaml"
        with open(config_path, "w") as config_file:
             yaml.dump(config, config_file)   
        os_call = "activate dvr && python {}generate.py configs/blender/blender.yaml".format(ABS_PATH)  
        os.system(os_call)
        t1 = time.time()

        out_path = ABS_PATH + out + "/generation/meshes"
        try:
            out_dir = os.listdir(out_path)
            for out_class in out_dir:
                out_class_path = out_path + '/' + out_class
                out_class_dir = os.listdir(out_class_path)
                i = 0
                for mesh in out_class_dir:
                    mesh_path = out_class_path + '/' + mesh
                    try:                  
                        bpy.ops.import_mesh.ply(filepath=mesh_path)
                        image = bpy.context.selected_objects[0].name
                        
                        bpy.data.objects[image].location = (0, 1.5*i, 0)
                        bpy.data.objects[image].rotation_euler = (radians(90.0), 0, 0)
                        # bpy.data.objects[image].scale = (scale, scale, scale)
                        i += 1
                    except:
                        print("Couldn't import ", mesh_path)
        except:
            print("Couldn't find output folder: ", out_path)
        t2 = time.time()
        print("DVR time: ", t1 - t0)
        print("Import PLY files time: ", t2 - t1)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        """Open up a file selector"""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    self.layout.operator(DVR.bl_idname)


addon_keymaps = []


def register():
    """Enable the add-on; setup keymap"""
    bpy.utils.register_class(DVR) # Enable add-on
    bpy.types.VIEW3D_MT_add.append(menu_func) # Add the operator to the "Add" menu.
    # Handle keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(DVR.bl_idname, 'Y', 'PRESS', ctrl=True, shift=True)
        addon_keymaps.append((km, kmi))


def unregister():
    """Disable the add-on; unload setup by register"""
    bpy.types.VIEW3D_MT_add.remove(menu_func) # Remove operator from menu
    # Handle keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(DVR)  



if __name__ == "__main__":
    register()
    bpy.ops.run.dvr('INVOKE_DEFAULT')
