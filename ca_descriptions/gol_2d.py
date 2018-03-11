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
import random
#def startGrid(newValue):
    #global startG = startG + newValue
    #return starG


def transition_func(grid, surrounding_fire, neighbourcounts):

    grid_dimensions = 200
    wind_direction = "w" #change direction here
    #initialGrid = np.zeros((grid_dimensions,grid_dimensions))
    #initialGrid[120:160,60:100] = 4                          # fill square with state 4
    #initialGrid[20:140,130:140] = 5                         # fill square with state 5
    if (wind_direction == "N" or wind_direction ==  "n"):
        wind_num = 0
        w_e = np.array([6,5,7,3,4,0,2,1])#wind effect array from left to right the values are neighbours directions ranked by which are most likely to catch fire due to wind direction
        print("n")
    elif (wind_direction == "E" or wind_direction == "e"):
        wind_num = 1
        w_e = np.array([3,0,5,1,6,2,7,4])#wind effect array
        print("e")
    elif (wind_direction == "S" or wind_direction == "s"):
        wind_num = 2
        w_e = np.array([1,2,0,3,4,5,7,6])#wind effect array
        print("s")
    else:
        wind_num = 3
        w_e = np.array([4,2,7,1,6,0,5,3])#wind effect array
        print("w")

    no_fire, on_fire, burned, lake, forest, canyon, fuel = neighbourcounts
    repr(on_fire)

    terrain_flammability = np.array([])
    fuel = (grid == 6) # cells that are currently in state 0
    grid[fuel] = 1
    no_fire = (grid == 0) # cells that are currently in state 0
    lake = (grid == 3)
    forest = (grid == 4) # cells that are currently in state 4
    canyon = (grid == 5) # cells that are currently in state 5
    #(nw=0,n=1,ne=2,w=3,e=4,sw=5,s=6,se=7)
    catching_fire = np.zeros((grid_dimensions, grid_dimensions), dtype=bool) #True table to see which will catch fire this transiton
    for i in range(0 , grid_dimensions):
        for j in range(0 , grid_dimensions):
            random_num = random.random()
            if((on_fire[i,j] == 1) & (surrounding_fire[w_e[0],i,j] == 1)): #uses the w_e(wind effect) array
                catching_fire[i,j] = True if ((grid[i,j] == 0) & (random_num <= 0.7)) else False
            elif((on_fire[i,j] == 1) & ((surrounding_fire[w_e[1],i,j] == 1) | (surrounding_fire[w_e[2],i,j] == 1))): #surrounding fire is a 3d array (8,200,200) with each of the 8 being a direction
                catching_fire[i,j] = True if (grid[i,j] == 0) & (random_num <= 0.4) else False
            elif((on_fire[i,j] == 1) & ((surrounding_fire[w_e[3],i,j] == 1) | (surrounding_fire[w_e[4],i,j] == 1))):
                catching_fire[i,j] = True if (grid[i,j] == 0) & (random_num <= 0.1) else False
            elif((on_fire[i,j] == 1) & ((surrounding_fire[w_e[5],i,j] == 1) | (surrounding_fire[w_e[6],i,j] == 1))):
                catching_fire[i,j] = True if (grid[i,j] == 0) & (random_num <= 0.05) else False
            elif((on_fire[i,j] == 1) & (surrounding_fire[w_e[7],i,j] == 1)):
                catching_fire[i,j] = True if (grid[i,j] == 0) & (random_num <= 0.01) else False

            if((on_fire[i,j] == 2) & (surrounding_fire[w_e[0],i,j] == 1)):
                catching_fire[i,j] = True if((grid[i,j] == 0)&(random_num <= 0.8))|((forest[i,j] == 1)&(random_num <= 0.1))else False #These use wind direction to see if the cell will catch fire
            elif((on_fire[i,j] == 2) & ((surrounding_fire[w_e[1],i,j] == 1) | (surrounding_fire[w_e[2],i,j] == 1))):                  #for either forest or grass (not needed for canyon as it
                catching_fire[i,j] = True if(grid[i,j] == 0)&(random_num <= 0.6)|((forest[i,j] == 1)&(random_num <= 0.08))else False # catches fire so easily)
            elif((on_fire[i,j] == 2) & ((surrounding_fire[w_e[3],i,j] == 1) | (surrounding_fire[w_e[4],i,j] == 1))):
                catching_fire[i,j] = True if(grid[i,j] == 0)&(random_num <= 0.2)|((forest[i,j] == 1)&(random_num <= 0.06))else False
            elif((on_fire[i,j] == 2) & ((surrounding_fire[w_e[5],i,j] == 1) | (surrounding_fire[w_e[6],i,j] == 1))):
                catching_fire[i,j] = True if(grid[i,j] == 0)&(random_num <= 0.10)|((forest[i,j] == 1)&(random_num <= 0.04))else False
            elif((on_fire[i,j] == 2) & (surrounding_fire[w_e[7],i,j] == 1)):
                catching_fire[i,j] = True if(grid[i,j] == 0)&(random_num <= 0.03)|((forest[i,j] == 1)&(random_num <= 0.02))else False

            if((on_fire[i,j] > 2) & (surrounding_fire[w_e[0],i,j] == 1)):
                catching_fire[i,j] = True if((grid[i,j] == 0)&(random_num <= 0.95))|((forest[i,j] == 1)&(random_num <= 0.2))else False
            elif((on_fire[i,j] > 2) & ((surrounding_fire[w_e[1],i,j] == 1) | (surrounding_fire[w_e[2],i,j] == 1))):
                catching_fire[i,j] = True if(grid[i,j] == 0)&(random_num <= 0.8)|((forest[i,j] == 1)&(random_num <= 0.16))else False
            elif((on_fire[i,j] > 2) & ((surrounding_fire[w_e[3],i,j] == 1) | (surrounding_fire[w_e[4],i,j] == 1))):
                catching_fire[i,j] = True if(grid[i,j] == 0)&(random_num <= 0.4)|((forest[i,j] == 1)&(random_num <= 0.12))else False
            elif((on_fire[i,j] > 2) & ((surrounding_fire[w_e[5],i,j] == 1) | (surrounding_fire[w_e[6],i,j] == 1))):
                catching_fire[i,j] = True if(grid[i,j] == 0)&(random_num <= 0.15)|((forest[i,j] == 1)&(random_num <= 0.08))else False
            elif((on_fire[i,j] > 2) & (surrounding_fire[w_e[7],i,j] == 1)):
                catching_fire[i,j] = True if(grid[i,j] == 0)&(random_num <= 0.05)|((forest[i,j] == 1)&(random_num <= 0.04))else False

            if(canyon[i,j] == 1) & (on_fire[i,j] >= 1):
                catching_fire[i,j] = True

    #survive = ((on_fire == 2) | (on_fire == 3)) & (grid == 1)
    #grid[:, :] = 0
    grid[catching_fire] = 1
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

    config.num_generations = 30 # 1 GENERATION = 2 HOURS
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
    config.wrap = False # Stops fire spreading over grid edges

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
