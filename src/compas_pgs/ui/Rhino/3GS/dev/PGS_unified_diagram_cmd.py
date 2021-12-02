from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs

import compas_rhino

from compas_3gs.algorithms import volmesh_ud

from compas_3gs.utilities import get_force_colors_uv

from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo

import Rhino


__commandname__ = "PGS_unified_diagram"


def _draw_ud(force, form, scale):

    compas_rhino.clear_layer(force.layer)

    # 1. get colors --------------------------------------------------------
    hf_color = (0, 0, 0)

    uv_c_dict = get_force_colors_uv(force.diagram, form.diagram, gradient=True)

    # 2. compute unified diagram geometries --------------------------------
    cells, prisms = volmesh_ud(force.diagram, form.diagram, scale=scale)

    # 3. draw --------------------------------------------------------------
    layer = force.settings["layer"]

    group_cells = "{}::cells".format(layer)
    group_prisms = "{}::prisms".format(layer)

    if not compas_rhino.rs.IsGroup(group_cells):
        compas_rhino.rs.AddGroup(group_cells)

    if not compas_rhino.rs.IsGroup(group_prisms):
        compas_rhino.rs.AddGroup(group_prisms)

    for cell in cells:
        vertices = cells[cell]['vertices']
        faces = cells[cell]['faces']
        guids = compas_rhino.draw_mesh(vertices, faces, layer=force.layer, name=str(cell), color=hf_color, redraw=False)
        compas_rhino.rs.AddObjectsToGroup(guids, group_cells)

    for edge in prisms:
        vertices = prisms[edge]['vertices']
        faces = prisms[edge]['faces']
        guids = compas_rhino.draw_mesh(vertices, faces, layer=force.layer, name=str(edge), color=uv_c_dict[edge], redraw=False)
        compas_rhino.rs.AddObjectsToGroup(guids, group_prisms)

    compas_rhino.rs.ShowGroup(group_cells)
    compas_rhino.rs.ShowGroup(group_prisms)

    form.artist.draw_edges(color=uv_c_dict)


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

    # get scale
    go = Rhino.Input.Custom.GetOption()
    go.SetCommandPrompt("Enter scale for unified diagram (press ESC to exit)")
    go.AcceptNothing(True)

    scale_opt = Rhino.Input.Custom.OptionDouble(0.50, 0.01, 0.99)

    go.AddOptionDouble("Alpha", scale_opt)

    show_loads = form.settings['show.externalforces']
    form.settings['show.externalforces'] = False
    scene.update()
    compas_rhino.clear_layer(form.layer)

    _draw_ud(force, form, 0.50)

    # unified diagram ----------------------------------------------------------
    while True:

        rs.EnableRedraw(True)

        opt = go.Get()
        scale = scale_opt.CurrentValue

        if not opt:
            print("The scale for unified diagram needs to be between 0.01 and 0.99!")

        if opt == Rhino.Input.GetResult.Cancel:  # esc
            keep = rs.GetString("Keep unified diagram? Press Enter to keep, or ESC to delete and exit.")
            form.settings['show.externalforces'] = show_loads
            if keep is None:
                scene.update()
                return
            else:
                _draw_ud(force, form, scale)
                rs.EnableRedraw(True)
                return

        _draw_ud(force, form, scale)


# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    RunCommand(True)
