from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs

import compas_rhino

from compas_3gs.diagrams.polyhedral import ForceVolMesh

from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo

from compas_rhino.utilities import volmesh_from_polysurfaces


__commandname__ = "PGS_force_from_polysurfaces"


@pgs_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    # get ForceVolMeshObject from scene
    force = scene.get("force")[0]
    if force:
        compas_rhino.display_message("Force diagram already exists in the scene!")
        return

    guids = rs.GetObjects("select polysurfaces", filter=rs.filter.polysurface)
    if not guids:
        return

    compas_rhino.rs.HideObjects(guids)

    force = volmesh_from_polysurfaces(ForceVolMesh, guids)
    scene.add_forcevolmesh(force, name='force', layer='3GS::ForceDiagram')

    force = scene.get("force")[0]
    force.check_eq()

    scene.update()

    print('Polyhedral force diagram successfully created.')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
