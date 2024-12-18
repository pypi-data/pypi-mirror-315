import numpy as np

from miniobj.loader import readlines, parse_lines
from miniobj.exporter import export_obj


class MiniObj:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.mtl_file_path = None

        self.v = []
        self.vn = []
        self.vt = []
        self.fv = []
        self.fvn = []
        self.fvt = []

        self.mtl = []
        self.mtl_f_map = {}

    def reset(self):
        self.v = []
        self.vn = []
        self.vt = []
        self.fv = []
        self.fvn = []
        self.fvt = []

        self.mtl = []
        self.mtl_f_map = {}

    def load(self, as_triangles=False):
        lines = readlines(self.file_path)
        parse_lines(self, lines)

        if as_triangles:
            self.quad_to_triangles()

        # post process
        if not self.has_fvn:
            self.fvn = []
        if not self.has_fvt:
            self.fvt = []

    @property
    def num_v(self):
        return len(self.v)

    @property
    def num_vt(self):
        return len(self.vt)

    @property
    def num_vn(self):
        return len(self.vn)

    @property
    def num_fv(self):
        return len(self.fv)

    @property
    def num_mtl(self):
        return len(self.mtl)

    @property
    def has_fvn(self):
        return len(self.fvn) > 0 and all(len(fvn) > 0 for fvn in self.fvn)

    @property
    def has_fvt(self):
        return len(self.fvt) > 0 and all(len(fvt) > 0 for fvt in self.fvt)

    def quad_to_triangles(self):
        fupdate_dict = {}
        current_face_index = 0

        has_fvn = self.has_fvn
        has_fvt = self.has_fvt

        new_fv = []
        if has_fvn:
            new_fvn = []
        if has_fvt:
            new_fvt = []

        for fi in range(self.num_fv):
            face = self.fv[fi]
            if has_fvn:
                fvn = self.fvn[fi]
            if has_fvt:
                fvt = self.fvt[fi]

            if len(face) == 4:
                new_fv1 = [face[0], face[1], face[2]]
                new_fv2 = [face[0], face[2], face[3]]
                if has_fvn:
                    new_fvn1 = [fvn[0], fvn[1], fvn[2]]
                    new_fvn2 = [fvn[0], fvn[2], fvn[3]]
                if has_fvt:
                    new_fvt1 = [fvt[0], fvt[1], fvt[2]]
                    new_fvt2 = [fvt[0], fvt[2], fvt[3]]

                fupdate_dict[fi] = [current_face_index, current_face_index + 1]
                new_fv.append(new_fv1)
                new_fv.append(new_fv2)
                current_face_index = len(new_fv)
                if has_fvn:
                    new_fvn.append(new_fvn1)
                    new_fvn.append(new_fvn2)
                if has_fvt:
                    new_fvt.append(new_fvt1)
                    new_fvt.append(new_fvt2)
            elif len(face) == 3:
                fupdate_dict[fi] = [current_face_index]
                new_fv.append(face)
                current_face_index = len(new_fv)
                if has_fvn:
                    new_fvn.append(fvn)
                if has_fvt:
                    new_fvt.append(fvt)
            else:
                raise ValueError(f"Invalid face length: {len(face)}")

        self.fv = new_fv
        if has_fvn:
            self.fvn = new_fvn
        if has_fvt:
            self.fvt = new_fvt

        if self.mtl_f_map:
            for k, faces in self.mtl_f_map.items():
                new_faces = []
                for face in faces:
                    new_faces.extend(fupdate_dict[face])
                self.mtl_f_map[k] = new_faces

    def export(self, file_path: str):
        export_obj(self, file_path)

    def scale_unit(self):
        min_v = np.min(self.v, axis=0)
        max_v = np.max(self.v, axis=0)
        scale = np.max(max_v - min_v)
        self.v = (self.v - min_v) / scale

    def quantize(self, bins=64):
        self.v = (self.v * bins).astype(int)
