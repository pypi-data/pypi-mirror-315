def readlines(file_path):
    # read all lines
    with open(file_path, "r") as file:
        lines = file.readlines()
    # strip start and end whitespace
    lines = [line.strip() for line in lines]
    return lines


def parse_each_face(face: str):
    components = face.split("/")
    vertex_index = int(components[0])
    if len(components) == 2:
        texture_index = int(components[1]) if components[1] != "" else -1
        normal_index = -1
    elif len(components) == 3:
        texture_index = int(components[1]) if components[1] != "" else -1
        normal_index = int(components[2]) if components[2] != "" else -1
    return vertex_index, texture_index, normal_index


def parse_lines(obj, lines: list[str]):
    current_mtl = None
    # parse lines
    for line in lines:
        if line.startswith("v "):
            # parse vertex
            vertex = line.split(" ")[1:]
            # map string to float
            vertex = [float(v) for v in vertex]
            obj.v.append(vertex)
        elif line.startswith("vn "):
            # parse vertex normal
            vertex_normal = line.split(" ")[1:]
            vertex_normal = [float(vn) for vn in vertex_normal]
            obj.vn.append(vertex_normal)
        elif line.startswith("vt "):
            # parse vertex texture
            vertex_texture = line.split(" ")[1:]
            vertex_texture = [float(vt) for vt in vertex_texture]
            obj.vt.append(vertex_texture)
        elif line.startswith("usemtl "):
            # parse material
            material = line.split(" ")[1]
            current_mtl = material
            obj.mtl.append(material)
            if material not in obj.mtl_f_map:
                obj.mtl_f_map[material] = []
        elif line.startswith("f "):
            # parse face
            points = line.split(" ")[1:]
            fv = []
            fvt = []
            fvn = []
            for point in points:
                vertex_index, texture_index, normal_index = parse_each_face(point)
                fv.append(vertex_index)
                if texture_index != -1:
                    fvt.append(texture_index)
                if normal_index != -1:
                    fvn.append(normal_index)

            current_face_index = len(obj.fv)
            if current_mtl is not None:
                obj.mtl_f_map[current_mtl].append(current_face_index)

            obj.fv.append(fv)
            obj.fvt.append(fvt)
            obj.fvn.append(fvn)
