"""Run with Blender 4.3 in background mode to export the interactive instrument.
The separate EarthRotor child can turn within its inclined axle.
"""
from pathlib import Path
from math import sin, cos, pi, radians
import bpy
import os
from mathutils import Vector
src=Path(__file__).resolve().parent
dst=src.parents[1]/'dist'/'assets'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
TAU=2*pi
C=Vector((0,0,.30))
def metal(name,color,rough=.23,metal=1):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    return m
silver=metal('Satin titanium',(.57,.66,.65),.235,.93)
edge=metal('Polished edges',(.83,.88,.84),.13,.98)
dark=metal('Smoked graphite',(.055,.07,.067),.25,.83)
green=metal('Pine enamel',(.024,.07,.055),.3,.5)
ink=metal('Etched graphite',(.045,.054,.050),.36,.39)
mark=metal('Pale index',(.69,.78,.67),.32,.54)
def mesh(name,verts,faces,mat,smooth=True):
    m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.update()
    ob=bpy.data.objects.new(name,m);bpy.context.collection.objects.link(ob);m.materials.append(mat)
    if smooth:
        for f in m.polygons:f.use_smooth=True
    return ob
def align(ob,n):
    ob.rotation_mode='QUATERNION';ob.rotation_quaternion=Vector((0,0,1)).rotation_difference(Vector(n).normalized())
    return ob
def lathe(name,section,mat,at=(0,0,0),normal=(0,0,1),steps=112):
    verts=[];faces=[];m=len(section)
    for i in range(steps):
        t=TAU*i/steps
        for r,z in section:verts.append((r*cos(t),r*sin(t),z))
    for i in range(steps):
        for j in range(m):
            jj=(j+1)%m
            faces.append((i*m+j,(i+1)%steps*m+j,(i+1)%steps*m+jj,i*m+jj))
    ob=mesh(name,verts,faces,mat);ob.location=at;align(ob,normal)
    return ob
def ring(name,r,thick,height,mat,at,normal=(0,0,1),bevel=.005):
    ri=r-thick;hh=height/2;b=min(bevel,thick/3,height/3)
    return lathe(name,[(ri+b,-hh),(r-b,-hh),(r,-hh+b),(r,hh-b),(r-b,hh),(ri+b,hh),(ri,hh-b),(ri,-hh+b)],mat,at,normal)
def cyl(name,r,height,mat,at,normal=(0,0,1),bevel=.008):
    return ring(name,r,r-.0001,height,mat,at,normal,bevel)
def ticks(name,r,extent,n,width,height,mat,center,normal,major=True):
    vv=[];ff=[]
    for i in range(n):
        t=TAU*i/n;l=extent if not major or i%6==0 else extent*.65 if i%3==0 else extent*.36
        w=width*(1.3 if i%6==0 else 1)
        start=len(vv)
        for rr,off in [(r-l,-w),(r,-w),(r,w),(r-l,w)]:vv.append((rr*cos(t+off),rr*sin(t+off),height))
        ff.append(tuple(start+j for j in range(4)))
    o=mesh(name,vv,ff,mat,False);o.location=center;align(o,normal)
    return o
def sphere(name,mat,r,at,seg=96,rings=56):
    verts=[];faces=[];uvfaces=[]
    for j in range(rings+1):
        lat=pi*(j/rings-.5)
        for k in range(seg+1):
            lon=TAU*(k/seg-.5)
            verts.append((r*cos(lat)*sin(lon),-r*cos(lat)*cos(lon),r*sin(lat)))
    for j in range(rings):
        for k in range(seg):
            i=j*(seg+1)+k
            f=(i,i+1,i+seg+2,i+seg+1)
            uvf=((k/seg,j/rings),((k+1)/seg,j/rings),((k+1)/seg,(j+1)/rings),(k/seg,(j+1)/rings))
            if j==0:f=(f[0],f[2],f[3]);uvf=(uvf[0],uvf[2],uvf[3])
            if j==rings-1:f=(f[0],f[1],f[2]);uvf=(uvf[0],uvf[1],uvf[2])
            faces.append(f);uvfaces.append(uvf)
    ob=mesh(name,verts,faces,mat)
    uv=ob.data.uv_layers.new(name='Map')
    for face,coords in zip(ob.data.polygons,uvfaces):
        for loop,coord in zip(face.loop_indices,coords):uv.data[loop].uv=coord
    ob.location=at
    return ob
# The turned parts stack into a stable, low weighted plinth.
lathe('Foot machined lower bevel',[(.002,-1.36),(.442,-1.36),(.493,-1.349),(.522,-1.326),(.532,-1.31),(.532,-1.289),(.525,-1.281),(.002,-1.281)],edge)
lathe('Foot deep enamel collar',[(.002,-1.285),(.516,-1.285),(.53,-1.277),(.53,-1.219),(.524,-1.206),(.49,-1.196),(.002,-1.196)],green)
lathe('Plinth satin crown',[(.002,-1.199),(.496,-1.199),(.504,-1.19),(.5,-1.174),(.46,-1.152),(.336,-1.142),(.003,-1.142)],silver)
ring('Plinth concentric incise',.402,.008,.004,ink,(0,0,-1.143))
lathe('Stem flared mounting',[(.002,-1.144),(.214,-1.144),(.217,-1.13),(.19,-1.11),(.113,-1.088),(.092,-1.052),(.084,-.988),(.091,-.949),(.135,-.924),(.141,-.901),(.139,-.887),(.003,-.887)],edge)
cyl('Stand upper clamp',.11,.19,dark,(0,0,-.838))
# Near-vertical graduated band with polished retainers on either side.
meridian=(0,-1,0)
ring('Meridian brushed instrument band',1.204,.081,.074,silver,C,meridian)
ring('Meridian graphite inlay',1.192,.055,.003,green,C+Vector(meridian)*.038,meridian,bevel=.0005)
ring('Meridian exterior bright lip',1.206,.012,.084,edge,C,meridian,bevel=.003)
ring('Meridian interior bright lip',1.136,.009,.083,edge,C,meridian,bevel=.002)
ticks('Meridian engraved coordinates',1.186,.045,144,.002,.041,mark,C,meridian)
# Inclined earth spindle.
axis=Vector((-.33,0,.944)).normalized()
for sign,name in [(1,'North'),(-1,'South')]:
    for dist,r,th,mat,part in [(1.041,.038,.11,edge,'axle'),(1.084,.068,.049,dark,'bushing'),(1.101,.062,.037,edge,'inner ferrule'),(1.214,.079,.050,silver,'crown'),(1.243,.052,.02,edge,'polished cap')]:
        pos=C+sign*dist*axis
        cyl(name+' '+part,r,th,mat,pos,axis,bevel=.008)
# Zodiac ring broad enough for machined coordinate indices and parallel polished lips.
orbit=Vector((-.286,-.087,.954)).normalized()
ring('Orbit graduated face',1.288,.066,.044,silver,C,orbit)
ring('Orbit outer bright rail',1.291,.012,.051,edge,C,orbit,bevel=.0025)
ring('Orbit inner bright rail',1.234,.009,.047,edge,C,orbit,bevel=.002)
ticks('Orbit minute graduation',1.281,.047,180,.0019,.0233,ink,C,orbit)
# Continuous warm-grey ink and enamel, with actual coastlines and understated graticule.
globe=metal('Cartographic evergreen enamel',(.2,.3,.25),.31,.36)
gp=globe.node_tree.nodes['Principled BSDF'];gp.inputs['Coat Weight'].default_value=.28;gp.inputs['Coat Roughness'].default_value=.21
tex=globe.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(src/'globe-enamel.jpg'));tex.image.colorspace_settings.name='sRGB';tex.image.pack()
globe.node_tree.links.new(tex.outputs['Color'],gp.inputs['Base Color'])
mount=bpy.data.objects.new('AxisMount',None);bpy.context.collection.objects.link(mount);mount.location=C;align(mount,axis)
earth=sphere('EarthRotor',globe,1.0,(0,0,0));earth.parent=mount;earth.rotation_euler.z=radians(-28)
# Export the physical instrument alone.
bpy.ops.object.select_all(action='SELECT')
turntable_dir=os.environ.get('MERIDIAN_TURNTABLE_DIR')
if not turntable_dir:
    bpy.ops.export_scene.gltf(filepath=str(dst/'meridian.glb'),export_format='GLB',use_selection=True,export_yup=True,export_materials='EXPORT',export_cameras=False,export_lights=False,export_animations=False,export_image_format='AUTO',export_extras=False)
# Calibrated transparent product poster. Object center in glTF world ~= (0,.072,0).
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=160;scene.cycles.use_denoising=False;scene.cycles.use_adaptive_sampling=True
scene.render.resolution_x=816;scene.render.resolution_y=912;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.file_format='PNG';scene.render.filepath=os.environ.get('MERIDIAN_POSTER_PATH',str(dst/'meridian-render.png'))
world=bpy.data.worlds.new('Soft highland studio');scene.world=world;world.use_nodes=True;bg=world.node_tree.nodes['Background'];bg.inputs['Strength'].default_value=.8
worldtex=world.node_tree.nodes.new('ShaderNodeTexEnvironment');worldtex.image=bpy.data.images.load('/usr/share/blender/datafiles/studiolights/world/courtyard.exr');world.node_tree.links.new(worldtex.outputs['Color'],bg.inputs[0])
def area(name,loc,power,size,color):
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(C-Vector(loc)).to_track_quat('-Z','Y').to_euler()
area('Large west window',(-3.4,-4.5,5.2),390,4.8,(1,.98,.94))
area('North skylight',(0,1.7,4.5),440,3.0,(.86,.95,1))
area('East reflector',(3.9,-2.1,1.7),180,4,(.90,.99,.95))
bpy.ops.object.camera_add(location=(2.5,-8.3,2.2));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,.073))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=3.27;scene.camera=cam
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
if turntable_dir:
    output=Path(turntable_dir)
    output.mkdir(parents=True,exist_ok=True)
    scene.render.resolution_x,scene.render.resolution_y=476,532
    scene.cycles.samples=28
    start=earth.rotation_euler.z
    for frame in range(36):
        earth.rotation_euler.z=start+TAU*frame/36
        scene.render.filepath=str(output/f'{frame:02}.png')
        bpy.ops.render.render(write_still=True)
else:
    bpy.ops.render.render(write_still=True)
