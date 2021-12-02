from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs

import compas_rhino

from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo


__commandname__ = "PGS__scene_clear"


@pgs_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    options = ["Yes", "No"]
    option = compas_rhino.rs.GetString("Clear all 3GS objects?", strings=options, defaultString="No")
    if not option:
        return

    if option == "Yes":
        scene.clear()

    rs.Command('Show')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
