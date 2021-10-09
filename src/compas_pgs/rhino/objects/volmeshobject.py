from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.objects import VolMeshObject


__all__ = ['VolMeshObject']


class VolMeshObject(VolMeshObject):
    """A customised `VolMeshArtist` for 3GS `VolMesh`-based data structures."""

    @property
    def diagram(self):
        """The diagram associated with the object."""
        return self.volmesh

    @diagram.setter
    def diagram(self, diagram):
        self.volmesh = diagram
