from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.objects import mesh_select_face

from compas_pgs.rhino import rhino_volmesh_pull_halffaces


from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo
from compas_pgs.rhino import VolmeshHalffaceInspector


__commandname__ = "PGS_force_pull_halffaces"


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

    current_setting = force.settings['show.faces']
    if not current_setting:
        force.settings['show.faces'] = True
        scene.update()

    # select halfface ----------------------------------------------------------
    boundary_halffaces = force.diagram.halffaces_on_boundaries()

    hf_inspector = VolmeshHalffaceInspector(
        force.diagram,
        hfkeys=boundary_halffaces,
        dependents=True)
    hf_inspector.enable()
    halfface = mesh_select_face(force.diagram)
    hf_inspector.disable()
    del hf_inspector

    # pull faces ---------------------------------------------------------------
    rhino_volmesh_pull_halffaces(force.diagram, hfkey=halfface)

    force.settings['show.faces'] = current_setting

    # check if there is form diagram -------------------------------------------
    form = scene.get("form")[0]
    if not form:
        force.check_eq()
        scene.update()
        return

    # update -------------------------------------------------------------------
    form.diagram.update_angle_deviations()

    form.check_eq()
    force.check_eq()

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
