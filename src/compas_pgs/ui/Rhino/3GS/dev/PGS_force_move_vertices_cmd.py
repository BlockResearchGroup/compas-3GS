from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_pgs.rhino import rhino_vertex_move

from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo


__commandname__ = "PGS_force_move_vertices"


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

    current_setting = force.settings['show.vertices']
    if not current_setting:
        force.settings['show.vertices'] = True
        scene.update()

    vertices = force.select_vertices()

    rhino_vertex_move(force.diagram, vertices)

    force.settings['show.vertices'] = current_setting

    # --------------------------------------------------------------------------
    form = scene.get("form")[0]
    if not form:
        force.check_eq()
        scene.update()
        return

    form.diagram.update_angle_deviations()

    # update -------------------------------------------------------------------
    force.check_eq()
    form.check_eq()

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
