# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Steven Garcia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

import bpy
import bmesh

from mathutils import Vector
from ..global_functions import global_functions

def unhide_object(mesh):
    mesh.hide_set(False)
    mesh.hide_viewport = False

def set_ignore(mesh):
    collection_list = mesh.users_collection
    ignore = False
    if mesh.hide_viewport or mesh.hide_get():
        ignore = True

    for collection in collection_list:
        if not collection.name == 'Master Collection':
            access_collection = bpy.data.collections[collection.name]
            if access_collection.hide_viewport:
                ignore = True

    return ignore

def count_steps(name, start, val):
    real_pos = start
    steps = 0
    while real_pos < len(name) and real_pos > 0 and name[real_pos] != " ":
        real_pos += val
        steps += val

    return steps

def gather_symbols(used_symbols_list, processed_symbol_name):
    symbol_name = "".join(processed_symbol_name)
    symbol_list = ("%", "#", "?", "!", "@", "*", "$", "^", "-", "&", "=", ".", ";", ")", ">", "<", "|", "~", "(", "{", "}", "[")
    for idx, char in enumerate(symbol_name): # loop through the characters in the name
        if char in symbol_list: # Check if the character exists in the symbols list
            symbol_name = symbol_name[:idx] + " " + symbol_name[idx + 1:]
            if not char in used_symbols_list: # Check if it's already been appended
                used_symbols_list += char

        else:
            if not char == " ": # If it isn't a whitespace then break cause we've hit the material name
                break

    return (used_symbols_list, symbol_name)

def gather_parameters(name):
    processed_name = name
    processed_parameters = []
    for lm_idx, char in enumerate(name): # loop through the characters in the name
        parameter = ""
        if char == ":":
            value_length = count_steps(name, lm_idx, 1)
            parameter_length = count_steps(name, lm_idx, -1) * -1
            if parameter_length == 3:
                for num in range(parameter_length + value_length):
                    parameter += processed_name[lm_idx - parameter_length + num]
                    index = lm_idx - parameter_length + num
                    processed_name = processed_name[:index] + " " + processed_name[index + 1:]

                processed_parameters.append(parameter)

    return (processed_name, processed_parameters)

def append_material_symbols(material, game_version):
    material_name = material.name
    if not global_functions.string_empty_check(material.ass_jms.name_override):
        material_name = material.ass_jms.name_override

    processed_symbol_name = material_name
    if material.ass_jms.is_bm and not game_version == 'halo3':
        processed_lightmap_properties = gather_parameters(material_name)
        processed_lightmap_name = processed_lightmap_properties[0]
        processed_parameters = processed_lightmap_properties[1]

        symbol_properties = gather_symbols("", processed_lightmap_name)
        symbol_properties = gather_symbols(symbol_properties[0], reversed(symbol_properties[1]))
        used_symbol_list = symbol_properties[0]
        processed_symbol_name = "".join(reversed(symbol_properties[1])).strip()
        if game_version == 'haloce':
            if material.ass_jms.two_sided or "%" in used_symbol_list:
                processed_symbol_name += "%"
            if material.ass_jms.transparent_1_sided or "#" in used_symbol_list:
                processed_symbol_name += "#"
            if material.ass_jms.render_only or "!" in used_symbol_list:
                processed_symbol_name += "!"
            if material.ass_jms.sphere_collision_only or "*" in used_symbol_list:
                processed_symbol_name += "*"
            if material.ass_jms.fog_plane or "$" in used_symbol_list:
                processed_symbol_name += "$"
            if material.ass_jms.ladder or "^" in used_symbol_list:
                processed_symbol_name += "^"
            if material.ass_jms.breakable or "-" in used_symbol_list:
                processed_symbol_name += "-"
            if material.ass_jms.ai_deafening or "&" in used_symbol_list:
                processed_symbol_name += "&"
            if material.ass_jms.collision_only or "@" in used_symbol_list:
                processed_symbol_name += "@"
            if material.ass_jms.portal_exact or "." in used_symbol_list:
                processed_symbol_name += "."

        elif game_version == 'halo2':
            if material.ass_jms.two_sided or "%" in used_symbol_list:
                processed_symbol_name += "%"
            if material.ass_jms.transparent_1_sided or "#" in used_symbol_list:
                processed_symbol_name += "#"
            if material.ass_jms.transparent_2_sided or "?" in used_symbol_list:
                processed_symbol_name += "?"
            if material.ass_jms.render_only or "!" in used_symbol_list:
                processed_symbol_name += "!"
            if material.ass_jms.collision_only or "@" in used_symbol_list:
                processed_symbol_name += "@"
            if material.ass_jms.sphere_collision_only or "*" in used_symbol_list:
                processed_symbol_name += "*"
            if material.ass_jms.fog_plane or "$" in used_symbol_list:
                processed_symbol_name += "$"
            if material.ass_jms.ladder or "^" in used_symbol_list:
                processed_symbol_name += "^"
            if material.ass_jms.breakable or "-" in used_symbol_list:
                processed_symbol_name += "-"
            if material.ass_jms.ai_deafening or "&" in used_symbol_list:
                processed_symbol_name += "&"
            if material.ass_jms.no_shadow or "=" in used_symbol_list:
                processed_symbol_name += "="
            if material.ass_jms.shadow_only or "." in used_symbol_list:
                processed_symbol_name += "."
            if material.ass_jms.lightmap_only or ";" in used_symbol_list:
                processed_symbol_name += ";"
            if material.ass_jms.precise or ")" in used_symbol_list:
                processed_symbol_name += ")"
            if material.ass_jms.conveyor or ">" in used_symbol_list:
                processed_symbol_name += ">"
            if material.ass_jms.portal_1_way or "<" in used_symbol_list:
                processed_symbol_name += "<"
            if material.ass_jms.portal_door or "|" in used_symbol_list:
                processed_symbol_name += "|"
            if material.ass_jms.portal_vis_blocker or "~" in used_symbol_list:
                processed_symbol_name += "~"
            if material.ass_jms.dislike_photons or "(" in used_symbol_list:
                processed_symbol_name += "("
            if material.ass_jms.ignored_by_lightmaps or "{" in used_symbol_list:
                processed_symbol_name += "{"
            if material.ass_jms.blocks_sound or "}" in used_symbol_list:
                processed_symbol_name += "}"
            if material.ass_jms.decal_offset or "[" in used_symbol_list:
                processed_symbol_name += "["
            if material.ass_jms.lightmap_resolution_scale > 0.0:
                processed_symbol_name += " lm:%s" % material.ass_jms.lightmap_resolution_scale
            if material.ass_jms.lightmap_power_scale > 0.0:
                processed_symbol_name += " lp:%s" % material.ass_jms.lightmap_power_scale
            if material.ass_jms.lightmap_half_life > 0.0:
                processed_symbol_name += " hl:%s" % material.ass_jms.lightmap_half_life
            if material.ass_jms.lightmap_diffuse_scale > 0.0:
                processed_symbol_name += " ds:%s" % material.ass_jms.lightmap_diffuse_scale

            for parameter in processed_parameters:
                split_parameter = parameter.split(':', 1)
                if split_parameter[0].strip() == "lm" and not "lm" in processed_symbol_name:
                    processed_symbol_name += " lm:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "lp" and not "lp" in processed_symbol_name:
                    processed_symbol_name += " lp:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "hl" and not "hl" in processed_symbol_name:
                    processed_symbol_name += " hl:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "ds" and not "ds" in processed_symbol_name:
                    processed_symbol_name += " ds:%s" % split_parameter[1]

    return processed_symbol_name

def deselect_objects(context):
    active_obj = context.view_layer.objects.active
    if not active_obj == None:
        if not active_obj.hide_get() and not active_obj.hide_viewport:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

        context.view_layer.objects.active = None

def select_object(context, obj):
    obj.select_set(True)
    context.view_layer.objects.active = obj

def vertex_group_clean_normalize(context, obj, limit_value):
    if len(obj.vertex_groups) > 0:
        select_object(context, obj)
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
        bpy.ops.object.vertex_group_clean(group_select_mode='ALL', limit=limit_value)
        bpy.ops.object.vertex_group_normalize_all(group_select_mode='ALL')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        context.view_layer.update()

def gather_modifers(obj):
    modifier_list = []
    for modifier in obj.modifiers:
        modifier.show_render = True
        modifier.show_viewport = True
        modifier.show_in_editmode = True
        modifier_list.append(modifier.type)

    return modifier_list

def add_modifier(context, obj, triangulate_faces, edge_split_class, armature):
    modifier_list = gather_modifers(obj)
    if triangulate_faces:
        if not 'TRIANGULATE' in modifier_list:
            obj.modifiers.new("Triangulate", type='TRIANGULATE')

    if edge_split_class and edge_split_class.is_enabled:
        if not 'EDGE_SPLIT' in modifier_list:
            edge_split = obj.modifiers.new("EdgeSplit", type='EDGE_SPLIT')
            edge_split.use_edge_angle = edge_split_class.use_edge_angle
            edge_split.split_angle = edge_split_class.split_angle
            edge_split.use_edge_sharp = edge_split_class.use_edge_sharp

        else:
            modifier_idx = modifier_list.index('EDGE_SPLIT')
            obj.modifiers[modifier_idx].use_edge_angle = edge_split_class.use_edge_angle
            obj.modifiers[modifier_idx].split_angle = edge_split_class.split_angle
            obj.modifiers[modifier_idx].use_edge_sharp = edge_split_class.use_edge_sharp

    if armature:
        if not 'ARMATURE' in modifier_list:
            armature_modifier = obj.modifiers.new("Armature", type='ARMATURE')
            armature_modifier.object = armature

        else:
            modifier_idx = modifier_list.index('ARMATURE')
            obj.modifiers[modifier_idx].object = armature

    context.view_layer.update()

def get_color_version_check(file_type):
    version = 8211
    if file_type == 'ASS':
        version = 6

    return version

def process_mesh_import_data(game_version, import_file, object_element, object_mesh, random_color_gen, file_type):
    vert_normal_list = []
    vertex_groups = []
    active_region_permutations = []
    bm = bmesh.new()
    if file_type == 'JMS':
        object_data = import_file

    else:
        object_data = object_element

    for idx, triangle in enumerate(object_data.triangles):
        triangle_material_index = triangle.material_index
        mat = None
        if not triangle_material_index == -1:
            mat = import_file.materials[triangle_material_index]

        if game_version == 'haloce':
            if import_file.version >= 8198:
                region = triangle.region

                current_region_permutation = import_file.regions[region].name

            else:
                region = import_file.vertices[triangle.v0].region
                current_region_permutation = import_file.regions[region].name

        elif game_version == 'halo2' or game_version == 'halo3':
            current_region_permutation = global_functions.material_definition_helper(triangle_material_index, mat)

        if not current_region_permutation in active_region_permutations:
            active_region_permutations.append(current_region_permutation)
            object_mesh.face_maps.new(name=current_region_permutation)

        p1 = object_data.vertices[triangle.v0].translation
        p2 = object_data.vertices[triangle.v1].translation
        p3 = object_data.vertices[triangle.v2].translation
        v1 = bm.verts.new((p1[0], p1[1], p1[2]))
        v2 = bm.verts.new((p2[0], p2[1], p2[2]))
        v3 = bm.verts.new((p3[0], p3[1], p3[2]))
        bm.faces.new((v1, v2, v3))
        vert_list = [triangle.v0, triangle.v1, triangle.v2]
        for vert in vert_list:
            vert_normals = []
            file_vert = object_data.vertices[vert]
            for normal in file_vert.normal:
                vert_normals.append(normal)

            vert_normal_list.append(vert_normals)
            for node_values in file_vert.node_set:
                node_index = node_values[0]
                if not node_index == -1 and not node_index in vertex_groups:
                    vertex_groups.append(node_index)
                    object_mesh.vertex_groups.new(name = import_file.nodes[node_index].name)

    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    if file_type == 'JMS':
        vertex_groups_names = object_mesh.vertex_groups.keys()

    for idx, triangle in enumerate(object_data.triangles):
        triangle_material_index = triangle.material_index
        if not triangle_material_index == -1:
            mat = import_file.materials[triangle_material_index]

        if game_version == 'haloce':
            if import_file.version >= 8198:
                region = triangle.region

                current_region_permutation = import_file.regions[region].name

            else:
                region = import_file.vertices[triangle.v0].region
                current_region_permutation = import_file.regions[region].name

        elif game_version == 'halo2' or game_version == 'halo3':
            current_region_permutation = global_functions.material_definition_helper(triangle_material_index, mat)

        if not current_region_permutation in active_region_permutations:
            active_region_permutations.append(current_region_permutation)
            object_mesh.face_maps.new(name=current_region_permutation)

        if not triangle_material_index == -1:
            material_list = []
            material_name = mat.scene_name
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            for slot in object_mesh.material_slots:
                material_list.append(slot.material)

            if not mat in material_list:
                material_list.append(mat)
                object_mesh.data.materials.append(mat)

            mat.diffuse_color = random_color_gen.next()
            material_index = material_list.index(mat)
            bm.faces[idx].material_index = material_index

        fm = bm.faces.layers.face_map.verify()
        face_idx = bm.faces[idx]
        face_idx[fm] = active_region_permutations.index(current_region_permutation)
        vert_list = [triangle.v0, triangle.v1, triangle.v2]
        for vert_idx, vert in enumerate(vert_list):
            vertex_index = (3 * idx) + vert_idx
            file_vert = object_data.vertices[vert]
            bm.verts[vertex_index].normal = file_vert.normal
            if not file_vert.color == None and game_version == 'halo3' and import_file.version >= get_color_version_check(file_type):
                color_r = file_vert.color[0]
                color_g = file_vert.color[1]
                color_b = file_vert.color[2]
                color_a = 1

                layer_color = bm.loops.layers.color.get("color")
                if layer_color is None:
                    layer_color = bm.loops.layers.color.new("color")

                loop = bm.faces[idx].loops[vert_idx]
                loop[layer_color] = (color_r, color_g, color_b, color_a)

            for uv_idx, uv in enumerate(file_vert.uv_set):
                uv_name = 'UVMap_%s' % uv_idx
                layer_uv = bm.loops.layers.uv.get(uv_name)
                if layer_uv is None:
                    layer_uv = bm.loops.layers.uv.new(uv_name)

                loop = bm.faces[idx].loops[vert_idx]
                loop[layer_uv].uv = (uv[0], uv[1])

            for node_values in file_vert.node_set:
                layer_deform = bm.verts.layers.deform.verify()

                node_index = node_values[0]
                node_weight = node_values[1]
                if not node_index == -1:
                    group_name = import_file.nodes[node_index].name
                    group_index = vertex_groups_names.index(group_name)
                    vert_idx = bm.verts[vertex_index]
                    vert_idx[layer_deform][group_index] = node_weight

    return bm, vert_normal_list

def process_mesh_export_weights(vert, armature, original_geo, vertex_groups, joined_list, file_type):
    node_index_list = []
    if len(vert.groups) != 0 and len(vert.groups) <= len(vertex_groups):
        object_vert_group_list = []
        vertex_vert_group_list = []
        for group_index in range(len(vert.groups)):
            vert_group = vert.groups[group_index].group
            object_vertex_group = vertex_groups[vert_group]
            if armature:
                if object_vertex_group in armature.data.bones:
                    vertex_vert_group_list.append(group_index)
                    if armature.data.bones[object_vertex_group] in joined_list:
                        object_vert_group_list.append(vert_group)

            else:
                if object_vertex_group in bpy.data.objects:
                    vertex_vert_group_list.append(group_index)
                    if bpy.data.objects[object_vertex_group] in joined_list:
                        object_vert_group_list.append(vert_group)

        value = len(object_vert_group_list)
        if value > 4:
            value = 4

        node_influence_count = int(value)
        node_set = []
        if len(object_vert_group_list) != 0:
            for idx, group_index in enumerate(object_vert_group_list):
                vert_index = int(vertex_vert_group_list[idx])
                vert_group = vert.groups[vert_index].group
                object_vertex_group = vertex_groups[vert_group]
                if armature:
                    node_obj = armature.data.bones[object_vertex_group]

                else:
                    node_obj = bpy.data.objects[object_vertex_group]

                node_index = int(joined_list.index(node_obj))
                if not node_index in node_index_list:
                    node_index_list.append(node_index)

                node_weight = float(vert.groups[vert_index].weight)
                node_set.append([node_index, node_weight])

        else:
            node_set = []
            node_influence_count = int(0)
            if file_type == 'JMS':
                parent_index = global_functions.get_parent(armature, original_geo, joined_list, 0)
                node_influence_count = int(1)
                node_index = int(parent_index[0])
                node_weight = float(1.0000000000)
                node_set.append([node_index, node_weight])

    else:
        node_set = []
        node_influence_count = int(0)
        if file_type == 'JMS':
            parent_index = global_functions.get_parent(armature, original_geo, joined_list, 0)
            node_influence_count = int(1)
            node_index = int(parent_index[0])
            node_weight = float(1.0000000000)
            node_set.append([node_index, node_weight])

    return node_influence_count, node_set, node_index_list

def process_mesh_export_color(evaluated_geo, loop_index):
    color = (0.0, 0.0, 0.0)
    if evaluated_geo.vertex_colors:
        color_rgb = evaluated_geo.vertex_colors.active.data[loop_index].color
        color = color_rgb

    return color

def process_mesh_export_uv(evaluated_geo, file_type, loop_index, version):
    uv_set = []
    for uv_index in range(len(evaluated_geo.uv_layers)):
        evaluated_geo.uv_layers.active = evaluated_geo.uv_layers[uv_index]
        uv = evaluated_geo.uv_layers.active.data[evaluated_geo.loops[loop_index].index].uv
        uv_set.append(uv)

    if file_type == 'JMS':
        if not uv_set and version <= 8204:
            uv_set = [(0.0, 0.0)]

    return uv_set

def process_mesh_export_vert(vert, file_type, original_geo_matrix, version, custom_scale):
    if file_type == 'JMS':
        translation = original_geo_matrix @ vert.co

    else:
        translation = custom_scale * vert.co

    mesh_dimensions = global_functions.get_dimensions(None, None, version, translation, True, False, file_type, custom_scale)
    scaled_translation = (mesh_dimensions.position[0], mesh_dimensions.position[1], mesh_dimensions.position[2])

    if file_type == 'JMS':
        normal = (original_geo_matrix @ (vert.co + vert.normal) - translation).normalized()

    else:
        normal = (vert.normal).normalized()

    if original_geo_matrix.determinant() < 0.0 and file_type == 'JMS':
        invert_translation_x = scaled_translation[0] * -1
        invert_translation_y = scaled_translation[1] * -1
        invert_translation_z = scaled_translation[2] * -1
        invert_normal_x = normal[0] * -1
        invert_normal_y = normal[1] * -1
        invert_normal_z = normal[2] * -1
        scaled_translation = (invert_translation_x, invert_translation_y, invert_translation_z)
        normal = (invert_normal_x, invert_normal_y, invert_normal_z)

    return scaled_translation, normal

def process_mesh_export_face_set(default_permutation, default_region, game_version, original_geo, face_map_idx):
    if game_version == 'haloce':
        if not face_map_idx == -1:
            region = original_geo.face_maps[face_map_idx].name
            face_set = (None, None, region)

    else:
        if not face_map_idx == -1:
            face_set = original_geo.face_maps[face_map_idx].name.split()

        lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)
        face_set = (lod, permutation, region)

    return face_set

def get_default_region_permutation_name(game_version):
    default_name = None
    if game_version == 'haloce':
        default_name = 'unnamed'

    else:
        default_name = 'Default'

    return default_name

def get_lod(lod_setting, game_version):
    LOD_name = None
    if game_version == 'haloce':
        if lod_setting == '1':
            LOD_name = 'superlow'

        elif lod_setting == '2':
            LOD_name = 'low'

        elif lod_setting == '3':
            LOD_name = 'medium'

        elif lod_setting == '4':
            LOD_name = 'high'

        elif lod_setting == '5':
            LOD_name = 'superhigh'

    else:
        LOD_name = lod_setting

    return LOD_name

def get_child_nodes(import_file_main, import_file_a, import_file_b, parent_idx, file_type):
    file_version = import_file_main.version
    first_frame = import_file_main.transforms[0]
    child_list = []
    for child_idx, node in enumerate(import_file_main.nodes):
        if node.parent == parent_idx:
            child_distance = (Vector((0, 0, 0)) - first_frame[child_idx].vector).length
            if file_version >= global_functions.get_version_matrix_check(file_type):
                child_distance = (first_frame[parent_idx].vector - first_frame[child_idx].vector).length

            child_list.append(child_distance)

    return child_list

def get_bone_distance(import_file_main, import_file_a, import_file_b, current_idx, file_type):
    bone_distance = 0
    file_version = import_file_main.version
    first_frame = import_file_main.transforms[0]
    child_list = get_child_nodes(import_file_main, import_file_a, import_file_b, current_idx, file_type)
    import_file_main_nodes = import_file_main.nodes

    if len(child_list) == 0 and import_file_main_nodes[current_idx].parent and not import_file_main_nodes[current_idx].parent == -1:
        bone_distance = (Vector((0, 0, 0)) - first_frame[current_idx].vector).length
        if file_version >= global_functions.get_version_matrix_check(file_type):
            bone_distance = (first_frame[import_file_main_nodes[current_idx].parent].vector - first_frame[current_idx].vector).length

    elif len(child_list) == 1:
        bone_distance = child_list[0]

    elif len(child_list) > 1:
        bone_distance = sum(child_list) / len(child_list)

    print(bone_distance)
    if bone_distance < 1.0:
        bone_distance = 1

    return bone_distance
