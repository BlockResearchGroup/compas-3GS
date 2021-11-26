from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino


__commandname__ = "PGS__redo"


def RunCommand(is_interactive):

    if 'PGS' not in sc.sticky:
        compas_rhino.display_message('PGS has not been initialised yet.')
        return

    scene = sc.sticky['PGS']['scene']
    if not scene:
        return

    if not scene.redo():
        compas_rhino.display_message("Nothing left to redo.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
