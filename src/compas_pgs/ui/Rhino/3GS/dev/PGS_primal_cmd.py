from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_3gs.diagrams import FormNetwork
from compas_3gs.algorithms import volmesh_dual_network

from compas_pgs.rhino import relocate_formdiagram

from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo

from compas.geometry import Translation


__commandname__ = "PGS_primal"


@pgs_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    # get ForceVolMeshObject from scene
    force = scene.get("force")[0]
    if not force:
        print("There is no force diagram in the scene.")
        return

    # --------------------------------------------------------------------------

    # make FormNetwork
    form = volmesh_dual_network(force.diagram, cls=FormNetwork)

    # set dual/primal
    form.dual = force.diagram
    force.diagram.primal = form

    # --------------------------------------------------------------------------

    # add FormNetworkObject
    translation = relocate_formdiagram(force.diagram, form)
    form.transform(Translation.from_vector(translation))
    form.update_angle_deviations()

    scene.add_formnetwork(form, name='form', layer='3GS::FormDiagram')

    form = scene.get("form")[0]

    # update -------------------------------------------------------------------
    form.check_eq()
    force.check_eq()

    scene.update()

    print('Primal diagram successfully created.')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
