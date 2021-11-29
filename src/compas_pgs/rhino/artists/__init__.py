from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from compas_3gs.diagrams import ForceVolMesh
from compas_3gs.diagrams import FormNetwork

from .forcevolmeshartist import ForceVolMeshArtist
from .formnetworkartist import FormNetworkArtist
from .volmeshartist import VolMeshArtist
from .networkartist import NetworkArtist

VolMeshArtist.register(ForceVolMesh, ForceVolMeshArtist)
NetworkArtist.register(FormNetwork, FormNetworkArtist)


__all__ = [name for name in dir() if not name.startswith('_')]
