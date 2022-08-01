bl_info = {
    "name": "DVR", # The add-on name
    "blender": (3, 1, 0), # Blender version for the add-on
    "category": "Object", 
}

import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
import os
import time
from math import radians
import yaml # Blender doesn't have yaml in its built-in python; need to install manually

# Path to the directory containing the python script for inferencing
# Replace with your own path
ABS_PATH = "C:/Users/CreatorAI/DVR/differentiable_volumetric_rendering/"

# constants
VERTEX_COLOR = 0
NORMAL_MAP = 1

class DVR(Operator):
    """
    The DVR Blender add-on.
    #####################################################################
    #                         Methods explained                         #
    #####################################################################
    invoke:
        Contains the steps that should be immediately executed as soon as
        we run the add-on. For DVR, invoke() opens a file explorer for
        user to select the input directory.
    execute:
        Contains the rest of the steps after the user confirms the file
        selection. It is the main function for any Blender add-on.
        For DVR, the steps are
        1. Get the selected input directory path, figure out the ouput
           directory path, and write both to the configuration file
        2. Execute a system call which activates the conda environment
           and runs DVR with the given input
        3. Iterate through the output folder and import all meshes twice
           (one with vertex color and one with normal map) which is
           handled in the helper method import_meshes()
        4. Display the latency breakdown and number of vertices
    import_meshes:
        Imports a mesh with specified material type and x/y-axis.
    #####################################################################
    """

    bl_idname = "run.dvr" # ID of this add-on
    bl_label = "Run DVR" # The button text for running the execute() method
    bl_options = {'REGISTER', 'UNDO'}
    
    # Only display folders in the file selector
    use_filter_folder = True
    # Make sure it is a valid directory path  
    directory: StringProperty(subtype="DIR_PATH")
    
    def execute(self, context):
        """Run DVR on the selected input folder"""     
        t0 = time.time()     

        # Handle input directory and configuration file
        data_path = self.directory
        out = "out/blender/" + data_path.split('\\')[-2]
        config = {"inherit_from": "configs/single_view_reconstruction/multi_view_supervision/ours_combined_pretrained.yaml",
                  "data": {"dataset_name": "images", "path": data_path},
                  "training": {"out_dir": out},
                  "generation": {"generation_dir": "generation"}}
        config_path = ABS_PATH + "configs/blender/blender.yaml"
        with open(config_path, "w") as config_file:
            print("load config")
            yaml.dump(config, config_file)   

        # Make system call
        os_call = 'activate dvr && python "{}generate.py" configs/blender/blender.yaml'.format(ABS_PATH)  
        print("====================================================")
        print("Executing system call...\n")        
        os.system(os_call)
        t1 = time.time()
        print("\nDone system call (activate conda & run AI inference)")

        # Import output meshes
        print("====================================================")
        print("Importing meshes...\n")
        out_path = ABS_PATH + out + "/generation/meshes"
        try:
            out_dir = os.listdir(out_path)
            for out_class in out_dir:
                out_class_path = out_path + '/' + out_class
                out_class_dir = os.listdir(out_class_path)
                i = 0
                num_vertices_list = []
                for mesh in out_class_dir:
                    mesh_path = out_class_path + '/' + mesh
                    try:
                        num_vertices = self.import_meshes(mesh_path, VERTEX_COLOR, 3, 3 + 5*i)
                        num_vertices_list.append(num_vertices)
                        self.import_meshes(mesh_path, NORMAL_MAP, -3.5, 3 + 5*i)                  
                        i += 1
                    except Exception as e: 
                        print(e)
                        print("Couldn't import ", mesh_path)
        except:
            print("Couldn't find output folder: ", out_path)
        t2 = time.time()
        print("\nDVR time: ", t1 - t0)
        print("Import meshes time: ", t2 - t1)

        # Display latency breakdown and number of vertices
        blender_font_curve = bpy.data.curves.new(type="FONT", name="Latency Font Curve")
        blender_font_curve.body = "DVR total time: {}s\nBlender import total time: {}s\nNumber of vertices: {}".format(
            round(t1 - t0, 4), round(t2 - t1, 4), num_vertices_list)
        blender_font_obj = bpy.data.objects.new(name="Blender Latency", object_data=blender_font_curve)
        bpy.context.scene.collection.objects.link(blender_font_obj)
        bpy.data.objects["Blender Latency"].scale = (0.5, 0.5, 0.5)
        bpy.data.objects["Blender Latency"].location = (0, -8, 0)
        bpy.data.objects["Blender Latency"].rotation_euler = (0, 0, radians(90.0))

        return {'FINISHED'}

    def import_meshes(self, mesh_path, material, x, y):
        """Import mesh from mesh_path with material and x-axis location at x and y-axis location at y"""

        # Import mesh
        bpy.ops.import_mesh.ply(filepath=mesh_path)
        # Get the mesh's name in order to manipulate it later
        mesh = bpy.context.selected_objects[0].name
        # Get the number of vertices of the imported mesh
        num_vertices = len(bpy.data.meshes[mesh].vertices)
        # Set the location, rotation and scale
        bpy.data.objects[mesh].location = (x, y, 0)
        bpy.data.objects[mesh].rotation_euler = (radians(90.0), 0, 0)
        bpy.data.objects[mesh].scale = (5, 5, 5)

        # Link the mesh to the specified material
        mat = bpy.data.materials.new(name=mesh)
        mat.use_nodes = True
        if material == VERTEX_COLOR: 
            shader_node = mat.node_tree.nodes.new('ShaderNodeVertexColor')
            bsdf_node =  mat.node_tree.nodes["Principled BSDF"]
            mat.node_tree.links.new(shader_node.outputs["Color"], bsdf_node.inputs["Base Color"])
        elif material == NORMAL_MAP:
            shader_node = mat.node_tree.nodes.new('ShaderNodeNormalMap')
            bsdf_node =  mat.node_tree.nodes["Principled BSDF"]
            mat.node_tree.links.new(shader_node.outputs["Normal"], bsdf_node.inputs["Base Color"])
        bpy.data.objects[mesh].data.materials.append(mat)
        return num_vertices
    
    def invoke(self, context, event):
        """Open up a file selector"""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

################################################################################
#                              Functions explained                             #
################################################################################
#  menu_func:                                                                  #
#      In the menu (user interface), link the operator button to its text.     #
#  register:                                                                   #
#      Called when enabling the add-on. Register the class, add the operator   #
#      to a specified place in menu, and add a keyboard shortcut.              #
#  unregister:                                                                 #
#      Called when disabling the add-on. Unregister the class, remove it from  #
#      the menu and remove its keyboard shortcut.                              #
################################################################################

def menu_func(self, context):
    """Link the operator button to its text"""
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

    # This will run the invoke() method
    # run.dvr is just the bl_idname we have defined
    bpy.ops.run.dvr('INVOKE_DEFAULT') 
