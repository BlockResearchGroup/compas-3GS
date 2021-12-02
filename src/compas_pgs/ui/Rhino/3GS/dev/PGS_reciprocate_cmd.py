from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_3gs.algorithms import volmesh_reciprocate

from compas_pgs.rhino import ReciprocationConduit
from compas_pgs.rhino import get_scene
from compas_pgs.rhino import pgs_undo


__commandname__ = "PGS_reciprocate"


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

    # --------------------------------------------------------------------------

    current_setting = form.settings['show.nodes']
    if not current_setting:
        form.settings['show.nodes'] = True
        scene.update()

    # --------------------------------------------------------------------------

    # get global settings
    kmax = scene.settings['Solvers']['reciprocation.kmax']
    weight = scene.settings['Solvers']['reciprocation.alpha']
    refresh = scene.settings['Solvers']['reciprocation.refreshrate']

    options = ['Alpha', 'Iterations', 'Fix_vertices', 'Refreshrate']

    # --------------------------------------------------------------------------
    fix_vertices = []

    while True:
        option = compas_rhino.rs.GetString('Press Enter to run or ESC to exit.', strings=options)

        if option is None:
            print("Reciprocation aborted!")
            return

        if not option:
            break

        if option == 'Alpha':
            weight = compas_rhino.rs.GetReal(
                "Enter weight factor : 1  = form only... 0 = force only...", 1.0, minimum=0, maximum=1.0)

        if option == 'Iterations':
            new_kmax = compas_rhino.rs.GetInteger('Enter number of iterations', kmax, 1, 10000)
            if new_kmax or new_kmax is not None:
                kmax = new_kmax

        elif option == 'Fix_vertices':
            fix_vertices += form.select_vertices()

        elif option == 'Refreshrate':
            new_refresh = compas_rhino.rs.GetInteger('Refresh rate for dynamic visualisation', refresh, 0, 1000)
            if new_refresh or new_refresh is not None:
                refresh = new_refresh

    if refresh > kmax:
        refresh = 0

    scene.settings['Solvers']['reciprocation.kmax'] = kmax
    scene.settings['Solvers']['reciprocation.refreshrate'] = refresh

    # --------------------------------------------------------------------------

    form.artist.clear()

    # --------------------------------------------------------------------------

    if refresh > 0:

        conduit = ReciprocationConduit(force.diagram, form.diagram)

        def callback(forcediagram, formdiagram, k, args, refreshrate=refresh):
            if k % refreshrate:
                return
            conduit.redraw()

        with conduit.enabled():
            volmesh_reciprocate(force.diagram,
                                form.diagram,
                                weight=weight,
                                edge_min=scene.settings['Solvers']['reciprocation.l_min'],
                                edge_max=scene.settings['Solvers']['reciprocation.l_max'],
                                fix_vkeys=fix_vertices,
                                kmax=kmax,
                                tolerance=scene.settings['3GS']['tol.angles'],
                                callback=callback,
                                print_result_info=True)

    else:
        volmesh_reciprocate(force.diagram,
                            form.diagram,
                            kmax=kmax,
                            weight=weight,
                            edge_min=scene.settings['Solvers']['reciprocation.l_min'],
                            edge_max=scene.settings['Solvers']['reciprocation.l_max'],
                            fix_vkeys=fix_vertices,
                            tolerance=scene.settings['3GS']['tol.angles'],
                            callback=callback,
                            print_result_info=True)

    form.diagram.update_angle_deviations()

    # update -------------------------------------------------------------------
    form.settings['show.nodes'] = current_setting

    force.check_eq()
    form.check_eq()

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
