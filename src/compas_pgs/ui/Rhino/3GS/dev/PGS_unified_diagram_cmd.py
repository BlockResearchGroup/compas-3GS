from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs

import compas_rhino

from compas_3gs.algorithms import volmesh_ud

from compas_3gs.utilities import get_force_colors_uv

from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo


__commandname__ = "PGS_unified_diagram"


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

    # get ForceVolMeshObject from scene
    form = scene.get("form")[0]
    if not force:
        print("There is no form diagram in the scene.")
        return

    # check global constraints -------------------------------------------------

    force.check_eq()
    form.check_eq()

    if not force.settings['_is.valid'] or not form.settings['_is.valid']:
        options = ["Yes", "No"]
        option = compas_rhino.rs.GetString("System is not in equilibrium... proceed?", strings=options, defaultString="No")
        if not option:
            return
        if option == "No":
            return

    show_loads = form.settings['show.externalforces']
    form.settings['show.externalforces'] = False

    # unified diagram ----------------------------------------------------------
    while True:

        rs.EnableRedraw(True)

        alpha = rs.GetReal('unified diagram scale', minimum=0.01, maximum=1.0)

        if alpha is None:
            break

        if not alpha:
            break

        compas_rhino.clear_layer(force.layer)
        compas_rhino.clear_layer(form.layer)

        # 1. get colors --------------------------------------------------------
        hf_color = (0, 0, 0)

        uv_c_dict = get_force_colors_uv(force.diagram, form.diagram, gradient=True)

        # 2. compute unified diagram geometries --------------------------------
        cells, prisms = volmesh_ud(force.diagram, form.diagram, scale=alpha)

        # 3. draw --------------------------------------------------------------
        for cell in cells:
            vertices = cells[cell]['vertices']
            faces = cells[cell]['faces']
            compas_rhino.draw_mesh(vertices, faces, layer=force.layer, name=str(cell), color=hf_color, redraw=False)

        for edge in prisms:
            vertices = prisms[edge]['vertices']
            faces = prisms[edge]['faces']
            compas_rhino.draw_mesh(vertices, faces, layer=force.layer, name=str(edge), color=uv_c_dict[edge], redraw=False)

        form.artist.draw_edges(color=uv_c_dict)

    # --------------------------------------------------------------------------

    form.settings['show.externalforces'] = show_loads

    scene.update()

# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    RunCommand(True)
