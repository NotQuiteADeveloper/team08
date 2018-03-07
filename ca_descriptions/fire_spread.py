# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np


def transition_func(grid, neighbourstates, neighbourcounts):
    wind_direction = "N"
    if (wind_direction == "N" or "n"):
        wind_num = 0
    elif (wind_direction == "E" or "e"):
        wind_num = 1
    elif (wind_direction == "S" or "s"):
        wind_num = 2
    else:
        wind_num = 3
    # dead = state == 0(green), live = state == 1(fire)
    # unpack state counts for state 0 and state 1
    neighbourstatesI = neighbourstates
    dead_neighbours, live_neighbours = neighbourcounts
    #neighbourstatesI()
    print(neighbourstatesI[6,1,:])
    print(neighbourstatesI[6,:,0])
    print(neighbourstatesI[:,1,0])
    print(neighbourstatesI[6,1,0])
    #loops for each generation
    print("hi")
    print(grid[0,:])
    print(grid[:,0])
    print(live_neighbours[0,:])
    print(live_neighbours.shape)
    repr(live_neighbours)
    # create boolean arrays for the birth & survival rules
    # if 3 live neighbours and is dead -> cell born

    #if (wind_num == 0):
    #    for i, cell in enumerate(grid)
    #    birth = (live_neighbours >= 1) & ((neighbourstatesI[6,]
    for i in range(0,49):
        for j in range(0,49):
            if (wind_num == 0 & (neighbourstatesI[6,i-1,j] == 1)):
                birth = True
            else:
                birth = False


    # if 2 or 3 live neighbours and is alive -> survives
    survive = (grid == 1)
    # Set all cells to 0 (dead)
    grid[:, :] = 0
    # Set cells to 1 where either cell is born or survives
    grid[birth] = 1
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "FIRE SPREAD"
    config.dimensions = 2
    config.states = (0, 1)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [(0.196, 0.804, 0.196),(1.000, 0.000, 0.000)]
    config.num_generations = 10
    config.grid_dims = (50,50)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()
