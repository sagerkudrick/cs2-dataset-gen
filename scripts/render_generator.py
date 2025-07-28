import bpy
import time

# Global variables to track the state
current_rotation_z = 0
current_rotation_y = 0
increment = 18  # Rotation increment in degrees
max_rotation = 180  # Stop Y rotation at 180 instead of 360
timestamp = time.strftime("%Y%m%d-%H%M%S")

# Get all collections in the scene
collections = bpy.context.scene.collection.children
current_collection_index = 0

def setup_collection_visibility():
    """Hide all collections except the current one."""
    global current_collection_index, collections

    for i, coll in enumerate(collections):
        coll.hide_viewport = i != current_collection_index
        coll.hide_render = i != current_collection_index

def rotate_and_render():
    global current_rotation_z, current_rotation_y, current_collection_index, timestamp

    if current_collection_index < len(collections):
        # Set up visibility for the current collection
        setup_collection_visibility()

        if current_rotation_y < max_rotation:  # Stop Y at 180
            # Rotate around Z-axis completely
            if current_rotation_z < 360:
                # Rotate the object around Z
                bpy.ops.transform.rotate(value=(increment * 3.14159) / 180, orient_axis='Z', orient_type='GLOBAL')
                current_rotation_z += increment

                # Render the scene
                bpy.context.scene.render.filepath = f"//render_{timestamp}_Coll{collections[current_collection_index].name}_Y{current_rotation_y}_Z{current_rotation_z}.png"
                bpy.ops.render.render(write_still=True)

                return 1.0  # 1 second delay
            else:
                # Reset Z rotation and increment Y rotation
                current_rotation_z = 0
                current_rotation_y += increment

                # Rotate the object around Y
                bpy.ops.transform.rotate(value=(increment * 3.14159) / 180, orient_axis='Y', orient_type='GLOBAL')

                # Render the scene
                bpy.context.scene.render.filepath = f"//render_{timestamp}_Coll{collections[current_collection_index].name}_Y{current_rotation_y}_Z{current_rotation_z}.png"
                bpy.ops.render.render(write_still=True)

                return 1.0  # 1 second delay
        else:
            # Reset rotations and move to the next collection
            current_rotation_z = 0
            current_rotation_y = 0
            current_collection_index += 1

            return 1.0  # 1 second delay
    else:
        # Stop the timer when all collections are done
        return None

# Register the timer
bpy.app.timers.register(rotate_and_render)
