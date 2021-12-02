from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_pgs.rhino import rhino_vertex_move

from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo


__commandname__ = "PGS_form_move_vertices"


@pgs_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    # get ForceVolMeshObject from scene
    form = scene.get("form")[0]
    if not form:
        print("There is no form diagram in the scene.")
        return

    # --------------------------------------------------------------------------

    current_setting = form.settings['show.nodes']
    if not current_setting:
        form.settings['show.nodes'] = True
        scene.update()

    vertices = form.select_vertices()

    rhino_vertex_move(form.diagram, vertices)

    form.settings['show.nodes'] = current_setting

    # --------------------------------------------------------------------------
    force = scene.get("force")[0]
    if not force:
        form.check_eq()
        scene.update()
        return

    # update -------------------------------------------------------------------
    form.diagram.update_angle_deviations()

    force.check_eq()
    form.check_eq()

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
