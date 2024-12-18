def export_obj(obj_mesh, file_path: str):
    with open(file_path, "w") as f:
        for v in obj_mesh.v:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for vt in obj_mesh.vt:
            f.write(f"vt {vt[0]} {vt[1]}\n")
        for vn in obj_mesh.vn:
            f.write(f"vn {vn[0]} {vn[1]} {vn[2]}\n")

        for k, faces in obj_mesh.mtl_f_map.items():
            f.write(f"usemtl {k}\n")
            for face in faces:
                fv = obj_mesh.fv[face]
                if obj_mesh.has_fvt:
                    fvt = obj_mesh.fvt[face]
                if obj_mesh.has_fvn:
                    fvn = obj_mesh.fvn[face]

                if obj_mesh.has_fvn and obj_mesh.has_fvt:
                    components = ["f"]
                    for i in range(len(fv)):
                        components.append(f"{fv[i]}/{fvt[i]}/{fvn[i]}")
                    f.write(" ".join(components) + "\n")
                elif obj_mesh.has_fvn:
                    components = ["f"]
                    for i in range(len(fv)):
                        components.append(f"{fv[i]}//{fvn[i]}")
                    f.write(" ".join(components) + "\n")
                elif obj_mesh.has_fvt:
                    components = ["f"]
                    for i in range(len(fv)):
                        components.append(f"{fv[i]}/{fvt[i]}")
                    f.write(" ".join(components) + "\n")
                else:
                    components = ["f"]
                    for i in range(len(fv)):
                        components.append(f"{fv[i]}")
                    f.write(" ".join(components) + "\n")

    print(f"Exported obj to {file_path}")
