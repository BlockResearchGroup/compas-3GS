from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo


__commandname__ = "PGS__scene_redraw"


@pgs_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
