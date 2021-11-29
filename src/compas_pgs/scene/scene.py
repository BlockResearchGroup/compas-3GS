from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from uuid import uuid4

import compas_rhino

from compas_pgs.rhino import SettingsForm
from compas_pgs.rhino import NetworkObject
from compas_pgs.rhino import VolMeshObject


class Scene(object):
    """"""

    def __init__(self, settings={}):
        self.nodes = {}
        self.settings = settings

    def add(self, item, **kwargs):
        kwargs['scene'] = self
        node = NetworkObject.build(item, **kwargs)
        guid = uuid4()
        self.nodes[guid] = node
        return node

    def add_forcevolmesh(self, item, **kwargs):
        """Add an object to the scene matching the provided item.

        Parameters
        ----------
        item : :class:`compas_ags.diagrams.Diagram`
        name : str, optional
        layer : str, optional
        visible : bool, optional
        settings : dict, optional

        Returns
        -------
        GUID
        """
        kwargs['scene'] = self
        guid = uuid4()
        node = VolMeshObject.build(item, **kwargs)
        self.nodes[guid] = node
        return node

    def add_formnetwork(self, item, **kwargs):
        """Add an object to the scene matching the provided item.

        Parameters
        ----------
        item : :class:`compas_ags.diagrams.Diagram`
        name : str, optional
        layer : str, optional
        visible : bool, optional
        settings : dict, optional

        Returns
        -------
        GUID
        """
        kwargs['scene'] = self
        guid = uuid4()
        node = NetworkObject.build(item, **kwargs)
        self.nodes[guid] = node
        return node

    def get(self, name):
        selected = []
        for guid in self.nodes:
            if name == self.nodes[guid].name:
                selected.append(self.nodes[guid])
        if len(selected) == 0:
            return [None]
        else:
            return selected

    def update(self):
        compas_rhino.rs.EnableRedraw(False)
        for guid in self.nodes:
            node = self.nodes[guid]
            node.draw()
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def clear(self):
        compas_rhino.rs.EnableRedraw(False)
        for guid in list(self.nodes):
            node = self.nodes[guid]
            node.clear_conduits()
            node.clear()
            del self.nodes[guid]
        self.nodes = {}
        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def update_settings(self, settings=None):
        # should this not produce some kind of result we can react to?
        SettingsForm.from_settings(self.settings)

    def clear_selection(self):
        compas_rhino.rs.UnselectAllObjects()

    def update_selection(self, guids):
        compas_rhino.rs.SelectObjects(guids)

    @property
    def registered_object_types(self):
        return VolMeshObject.registered_object_types()
