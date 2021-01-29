import bpy
import time

bl_info = {
    "name": "Sponge Creator",
    "blender": (2, 80, 0),
    "category": "Object",
}

def deselect():
    for i in bpy.context.scene.objects:
        i.select_set(False)

def fractalPart(mainPart):
    deselect()
    parts=[]
    
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0))
    parts.append(bpy.context.active_object)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(1,0,0))
    parts.append(bpy.context.active_object)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-1,0,0))
    parts.append(bpy.context.active_object)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,1,0))
    parts.append(bpy.context.active_object)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,-1,0))
    parts.append(bpy.context.active_object)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,1))
    parts.append(bpy.context.active_object)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,-1))
    parts.append(bpy.context.active_object)
    #print(parts)
    for i in range(1,len(parts)):
        #print(parts[i])
        bool = parts[0].modifiers.new(type="BOOLEAN", name="bool")
        bool.object = parts[i]
        bool.operation = 'UNION'
        #parts[i].hide_viewport = True
        bpy.context.view_layer.objects.active = parts[0]
        bpy.ops.object.modifier_apply(modifier="bool")
    deselect()
    while len(parts)>1:
        bpy.context.view_layer.objects.active = parts[1]
        parts[1].select_set(True)
        bpy.ops.object.delete()
        parts.pop(1)
    bool = mainPart.modifiers.new(type="BOOLEAN", name="bool")
    bool.object = parts[0]
    bool.operation = 'DIFFERENCE'
    #parts[i].hide_viewport = True
    bpy.context.view_layer.objects.active = mainPart
    bpy.ops.object.modifier_apply(modifier="bool")
    bpy.context.view_layer.objects.active = parts[0]
    deselect()
    parts[0].select_set(True)
    bpy.ops.object.delete()
    deselect()
    

def replicate(mainPart):
    deselect()
    mainPart.scale[0]=1/3
    mainPart.scale[1]=1/3
    mainPart.scale[2]=1/3
    bpy.context.view_layer.objects.active = mainPart
    mainPart.select_set(True)
    bpy.ops.object.transform_apply(scale=True)
    parts=[]
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                if abs(x)+abs(y)+abs(z)>1:
                    print(str(x)+' '+str(y)+' '+str(z))
                    deselect()
                    bpy.context.view_layer.objects.active = mainPart
                    mainPart.select_set(True)
                    bpy.ops.object.duplicate()
                    parts.append(bpy.context.active_object)
                    bpy.context.active_object.location[0]=x
                    bpy.context.active_object.location[1]=y
                    bpy.context.active_object.location[2]=z
                    
    print(parts)
    deselect()
    bpy.context.view_layer.objects.active = mainPart
    mainPart.select_set(True)
    bpy.ops.object.delete()
    for i in range(1,len(parts)):
        #print(parts[i])
        bool = parts[0].modifiers.new(type="BOOLEAN", name="bool")
        bool.object = parts[i]
        bool.operation = 'UNION'
        #parts[i].hide_viewport = True
        bpy.context.view_layer.objects.active = parts[0]
        bpy.ops.object.modifier_apply(modifier="bool")
    deselect()
    while len(parts)>1:
        bpy.context.view_layer.objects.active = parts[1]
        parts[1].select_set(True)
        bpy.ops.object.delete()
        parts.pop(1)
    deselect()
    bpy.context.view_layer.objects.active = parts[0]
    parts[0].select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    return parts[0]

class runSponge(bpy.types.Operator):
    """Runs the fractal."""
    bl_idname = "object.make_sponge_fractal"
    bl_label = "Create layer of sponge fractal."
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        replicate(bpy.context.active_object)
        return {'FINISHED'}

#bpy.ops.mesh.primitive_cube_add(size=3, location=(0,0,0))
#main=bpy.context.active_object
#fractalPart(main)
#for i in range(2):
    #main=replicate(main)
def menu_func(self, context):
    self.layout.operator(runSponge.bl_idname)

def register():
    bpy.utils.register_class(runSponge)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(runSponge)

if __name__ == "__main__":
    register()
    print("Registered!")
