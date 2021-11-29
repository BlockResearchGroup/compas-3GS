from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json

import compas_rhino

from compas.utilities import DataEncoder

from compas_pgs.rhino import get_system
from compas_pgs.rhino import get_scene
from compas_pgs.rhino import select_filepath_save


__commandname__ = "PGS__session_save"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    system = get_system()
    if not system:
        return

    scene = get_scene()
    if not scene:
        return

    dirname = system['session.dirname']
    filename = system['session.filename']
    extension = system['session.extension']

    filepath = select_filepath_save(dirname, extension)
    if not filepath:
        return
    dirname, basename = os.path.split(filepath)
    filename, _ = os.path.splitext(basename)

    filepath = os.path.join(dirname, filename + '.' + extension)

    session = {
        "data": {"form": None, "force": None},
        "settings": scene.settings,
    }

    form = scene.get('form')[0]
    if form:
        session['data']['form'] = form.datastructure.to_data()

    force = scene.get('force')[0]
    if force:
        session['data']['force'] = force.datastructure.to_data()

    with open(filepath, 'w+') as f:
        json.dump(session, f, cls=DataEncoder)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
