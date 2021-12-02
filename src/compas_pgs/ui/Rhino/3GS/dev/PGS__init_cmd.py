from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import scriptcontext as sc

import compas
import compas_rhino

compas_rhino.unload_modules('compas_pgs')

from compas_pgs.scene import Scene  # noqa: E402
from compas_pgs.rhino import Browser  # noqa: E402
from compas_pgs.activate import check  # noqa: E402
from compas_pgs.activate import activate  # noqa: E402


__commandname__ = "PGS__init"


SETTINGS = {

    "3GS": {
        "show.angles": True,
        "show.forces": False,
        "tol.angles": 1.0,
        "tol.flatness": 0.1
    },

    "Solvers": {
        "reciprocation.alpha": 1.0,
        "reciprocation.l_min": 0.1,
        "reciprocation.l_max": 100000,
        "reciprocation.kmax": 500,
        "reciprocation.tol": 0.01,
        "reciprocation.refreshrate": 5,

        "planarization.kmax": 500,
        "planarization.tol": 0.01,
        "planarization.refreshrate": 10,

        "arearization.kmax": 500,
        "arearization.tol": 0.01,
        "arearization.refreshrate": 10,

    }
}


HERE = compas_rhino.get_document_dirname()
HOME = os.path.expanduser('~')
CWD = HERE or HOME

compas.PRECISION = '3f'


def RunCommand(is_interactive):

    if check():
        print("Current plugin is already activated")
    else:
        compas_rhino.rs.MessageBox("Detected environment change, re-activating plugin", 0, "Re-activating Needed")
        if activate():
            compas_rhino.rs.MessageBox("Restart Rhino for the change to take effect", 0, "Restart Rhino")
        else:
            compas_rhino.rs.MessageBox("Someting wrong during re-activation", 0, "Error")
        return

    Browser()

    sc.sticky["3GS.system"] = {
        "session.dirname": CWD,
        "session.filename": None,
        "session.extension": '3gs'
    }

    scene = Scene(SETTINGS)
    scene.clear()

    sc.sticky["3GS"] = {"scene": scene}

    sc.sticky["3GS.sessions"] = []

    print("3GS is successfully initiated!")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
