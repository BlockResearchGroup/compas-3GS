from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_pgs.rhino import SettingsForm

from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo


__commandname__ = "PGS_settings"


@pgs_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    SettingsForm.from_scene(scene, object_types=["ForceVolMeshObject", "FormNetworkObject"], global_settings=['3GS', 'Solvers'])

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
