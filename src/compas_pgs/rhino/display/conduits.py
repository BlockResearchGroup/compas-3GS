from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import length_vector
from compas.geometry import length_vector_sqrd

from compas_rhino.conduits import BaseConduit

from System.Drawing.Color import FromArgb

import Rhino
import scriptcontext as sc

from Rhino.Geometry import Line
from Rhino.Geometry import Point3d

find_object = sc.doc.Objects.Find
feedback_color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor

arrow_color = FromArgb(255, 0, 79)
jl_blue = FromArgb(0, 113, 188)
black = FromArgb(0, 0, 0)
gray = FromArgb(200, 200, 200)
green = FromArgb(0, 255, 0)
white = FromArgb(255, 255, 255)
form_color = FromArgb(255, 255, 255)
force_color = FromArgb(0, 0, 0)


__all__ = ['MeshConduit',
           'VolmeshConduit',
           'ExternalForcesConduit',
           'ReciprocationConduit']


# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
#
#   mesh conduit
#
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************


class MeshConduit(BaseConduit):
    """Conduit for mesh algorithms.

    """

    def __init__(self, mesh, face_colordict={}, **kwargs):
        super(MeshConduit, self).__init__(**kwargs)
        self.mesh = mesh
        self.face_colordict = face_colordict

    def DrawForeground(self, e):
        _conduit_mesh_edges(self.mesh, e)

        if self.face_colordict:
            for fkey in self.face_colordict:
                color = FromArgb(*self.face_colordict[fkey])
                points = self.mesh.face_coordinates(fkey)
                points.append(points[0])
                points = [Point3d(*pt) for pt in points]
                e.Display.DrawPolygon(points, color, filled=True)


# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
#
#   volmesh conduit
#
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************


class VolmeshConduit(BaseConduit):
    """Conduit for volmesh algorithms.

    """

    def __init__(self, volmesh, face_colordict={}, **kwargs):
        super(VolmeshConduit, self).__init__(**kwargs)
        self.volmesh = volmesh
        self.face_colordict = face_colordict

    def DrawForeground(self, e):
        _conduit_volmesh_edges(self.volmesh, e)

        if self.face_colordict:
            for fkey in self.face_colordict:
                color = FromArgb(*self.face_colordict[fkey])
                f_vkeys = self.volmesh.halfface_vertices(fkey)
                points = [self.volmesh.vertex_coordinates(vkey) for vkey in f_vkeys]
                points.append(points[0])
                points = [Point3d(*pt) for pt in points]
                e.Display.DrawPolygon(points, color, filled=True)


class ExternalForcesConduit(BaseConduit):

    def __init__(self, network, color, scale, tol, **kwargs):
        super(ExternalForcesConduit, self).__init__(**kwargs)
        self.network = network
        self.color = color
        self.scale = scale
        self.tol = tol
        self.arrow_size = 0.1

    def DrawForeground(self, e):

        load_vectors = {}
        load_mags = {}

        for cell in self.network.dual.cells_on_boundaries():
            vectors = []
            for face in self.network.dual.cell_faces(cell):
                if self.network.dual.is_halfface_on_boundary(face):
                    vectors.append(self.network.dual.halfface_normal(face, unitized=False))

            vectors = zip(*vectors)
            resultant = [sum(vector) for vector in vectors]
            load_vectors[cell] = resultant
            load_mags[cell] = length_vector(resultant)

        for node in self.network.nodes():
            r = scale_vector(load_vectors[node], self.scale)
            sp = self.network.node_coordinates(node)
            ep = add_vectors(sp, r)
            if length_vector_sqrd(r) < self.tol ** 2:
                continue
            if self.network.dual.attributes['convention'] == -1:
                sp, ep = ep, sp
            line = Line(Point3d(*sp), Point3d(*ep))
            e.Display.DrawArrow(line,
                                FromArgb(*self.color),
                                0,
                                self.arrow_size)


# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
#
#   reciprocation conduit
#
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************


class ReciprocationConduit(BaseConduit):
    """Conduit for the reciprocation algorithm.

    """

    def __init__(self, volmesh, network, **kwargs):
        super(ReciprocationConduit, self).__init__(**kwargs)
        self.volmesh = volmesh
        self.network = network

    def DrawForeground(self, e):
        _conduit_volmesh_edges(self.volmesh, e)
        _conduit_network_edges(self.network, e)


# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
#
#   conduit helpers
#
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************


def _conduit_network_edges(network, e):
    for u, v in network.edges():
        sp = network.node_coordinates(u)
        ep = network.node_coordinates(v)
        # e.Display.DrawPoint(Point3d(*sp), 0, 4, white)
        # e.Display.DrawPoint(Point3d(*ep), 0, 4, white)
        e.Display.DrawLine(Line(Point3d(*sp), Point3d(*ep)), white, 1)


def _conduit_mesh_edges(mesh, e):
    for u, v in mesh.edges():
        sp = mesh.vertex_coordinates(u)
        ep = mesh.vertex_coordinates(v)
        # e.Display.DrawPoint(Point3d(*sp), 0, 4, white)
        # e.Display.DrawPoint(Point3d(*ep), 0, 4, white)
        e.Display.DrawLine(Line(Point3d(*sp), Point3d(*ep)), white, 1)


def _conduit_volmesh_edges(volmesh, e):
    for u, v in volmesh.edges():
        sp = volmesh.vertex_coordinates(u)
        ep = volmesh.vertex_coordinates(v)
        # e.Display.DrawPoint(Point3d(*sp), 0, 4, white)
        # e.Display.DrawPoint(Point3d(*ep), 0, 4, white)
        e.Display.DrawLine(Line(Point3d(*sp), Point3d(*ep)), white, 1)


# ******************************************************************************
# ******************************************************************************
# ******************************************************************************
#
#   main
#
# ******************************************************************************
# ******************************************************************************
# ******************************************************************************


if __name__ == "__main__":
    pass
