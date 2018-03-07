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
    unburnt, burning, burnt, lake, forest, canyon, fuel= neighbourcounts

    fuel = (grid == 6) # cells that are currently in state 0
    grid[fuel] = 1

    unburnt = (grid == 0) # cells that are currently in state 0
    three_one_neighbours = (neighbourcounts[1] == 2) # cells that have 2 neighbours in state 0
    unburn_to_burning = unburnt & three_one_neighbours
    # cells that are currently in state 0 and have exactly 2 neighbours in state 1
    grid[unburn_to_burning] = 1

    forest = (grid == 4) # cells that are currently in state 4
    four_one_neighbours = (neighbourcounts[1] == 4) # cells that have 4 neighbours in state 0
    forest_to_burning = forest & four_one_neighbours
    # cells that are currently in state 4 and have exactly 4 neighbours in state 1
    grid[forest_to_burning] = 1

    canyon = (grid == 5) # cells that are currently in state 5
    two_one_neighbours = (neighbourcounts[1] == 1) # cells that have 1 neighbours in state 0
    canyon_to_burning = canyon & two_one_neighbours
    # cells that are currently in state 5 and have exactly 1 neighbours in state 1
    grid[canyon_to_burning] = 1

    burning = (grid == 1) # cells that are currently in state 2
    three_one_neighbours = (neighbourcounts[1] == 6) # cells that have 3 neighbours in state 0
    burning_to_burnt = burning & three_one_neighbours
    # cells that are currently in state 2 and have exactly 3 neighbours in state 1
    grid[burning_to_burnt] = 2

    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "fire"
    config.dimensions = 2
    config.states = (0, 1, 2, 3, 4, 5, 6)
    # 0 no fire (yellow)
    # 1 on fire (red)
    # 2 burned  (black)
    # 3 lake    (blue)
    # 4 forest  (green)
    # 5 canyon  (grey)
    # 6 fuel    (brown)
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.num_generations = 700
    config.grid_dims = (200,200)
    config.state_colors = [(0.9,0.7,0.1),(1,0,0),(0,0,0),(0,0.5,1),(0,0.3,0),(0.6,0.6,0.6),(0.4,0.1,0.1)]

    config.initial_grid = np.zeros(config.grid_dims)                # zero grid
    halfr, halfc = config.grid_dims[0]//2, config.grid_dims[1]//2   # calc central square indices
    config.initial_grid[halfr:halfr+5, halfc:halfc+5] = 0           # fill square with state 0
    config.initial_grid[40:60,20:60] = 3                            # fill square with state 3
    config.initial_grid[120:160,60:100] =4                          # fill square with state 4
    config.initial_grid[20:140,130:140] = 5                         # fill square with state 5
    #config.initial_grid[0:3,0:3] = 6                                    # fill square with state 6
    config.initial_grid[0:3,197:200] = 6                                  # fill square with state 6
    config.wrap = False

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
