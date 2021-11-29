from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import is_color_rgb

from compas_rhino.artists import VolMeshArtist


__all__ = ['VolMeshArtist']


class VolMeshArtist(VolMeshArtist):
    """A customised `VolMeshArtist` for 3GS `VolMesh`-based data structures."""

    def __init__(self, **kwargs):
        super(VolMeshArtist, self).__init__(**kwargs)

        self.color_vertices = self.vertex_color
        self.color_edges = self.edge_color
        self.color_faces = self.face_color
        self.color_cells = self.cell_color

    @property
    def diagram(self):
        """The diagram assigned to the artist."""
        return self.volmesh

    @diagram.setter
    def diagram(self, diagram):
        self.volmesh = diagram

