import math
import numpy as np
np.set_printoptions(threshold=1000000000)

#initialize the output figure
figure = np.zeros((10, 150))
#defining constants to make the code more readable
X = 0
Y = 1
time_increment = 0.01
#position of the rocket [x, y] initialized at 0, 0
position = [0, 0]

def show_trajectory(last_position, cur_position, last_figure):
    #updating the undelying architecture
    value = 0
    if last_position[Y] > cur_position[Y]:
        value = -1
    elif last_position[Y] < cur_position[Y]:
        value = 1
    position_of_new_drawing = [int(cur_position[X]/150),int(cur_position[Y]/10)]
    last_figure[position_of_new_drawing[Y]][position_of_new_drawing[X]] = value
    print(last_figure)
    #printing the datamap
    for i in range(10):
        buffer = ""
        for j in range(149, 0, -1):
            if last_figure[i][j] == 0:
                buffer += " "
            elif last_figure[i][j] == 1:
                buffer += "/"
            elif last_figure[i][j] == -1:
                buffer += "\\"
        print(buffer)
    return last_figure

def calc_acceleration():
    return

def calc_trajectory():
    """Will have a loop that will continue unless the rocket touches the floor and will increment the time by time_increment seconds"""
    #defining global variables
    global position
    global figure
    for t in np.arange(0, 100, time_increment):
        #calc acceleration taking into account last acceleration
        #calc velocity taking into account last velocity
        #calc position compared to last position
        cur_position = [1,1]
        #if y of position is <= 0 end
        #show a figure of the trajectory of the rocket
        figure = show_trajectory(position, cur_position, figure)
        position = cur_position
        break
        if position[Y] <= 0:
            break

if __name__ == '__main__':
    calc_trajectory()
