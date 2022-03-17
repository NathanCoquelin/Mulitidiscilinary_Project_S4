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
#velocity list of the rocket
velocity = [0, 0]
#acceleration list of the rocket
acceleration = [0, 0]
#ramp for use in on_ramp
ramp_length = 1
#inputing the angle of the ramp
angle_of_ramp = 45
#converting it to radians
angle_of_ramp = math.radians(angle_of_ramp)
#friction coefficient of the rocket on the ramp
friction_coefficient = 0.1
#masses in kg
mass_of_rocket = 0.5
#mass of fuel also in kg
mass_of_fuel = 0.25
# g the constant force of gravity
g = 9.81
#the trust of the rocket due to the chemical reaction
thrust = 10
#rate of consumption of the fuel in kg/s
consumption = 0.1
#drag coefficient
drag_coefficient = 0.000624
#density of air in kg/m^3
density_of_air = 1.225
#area on the front of the rocket in m^2
profile_area = 0.2

def on_ramp():
    """This function will check if the rocket is on the ramp by using the distance of position to the start position"""
    global position
    if math.sqrt(position[X]**2 + position[Y]**2) <= ramp_length:
        return True
    else:
        return False

def calc_acceleration():
    """
        This function will calculate the acceleration of the rocket wether its on the ramp or not
        if the rocket is on the ramp the gravity is neglected and the main acceleration is the thrust in direction of the ramp
    """
    global velocity
    a = [0, 0]
    if mass_of_fuel >= 0:
        if on_ramp:
            a = [math.cos(angle_of_ramp) * thrust, math.sin(angle_of_ramp) * thrust]
        else:
            #if not on the ramp and has fuel need to adapt
            a = [math.atan(velocity[Y] / velocity[X]) * thrust, math.atan(velocity[Y] / velocity[X]) * thrust]
    if on_ramp:
        #apply friction force
        normal_force = (mass_of_rocket + mass_of_fuel) * g * math.cos(angle_of_ramp)
        friction_force = [math.cos(angle_of_ramp) * friction_coefficient * normal_force, math.sin(angle_of_ramp) * friction_coefficient * normal_force]
        #adapt the acceleration to stay on the ramp
        a = [a[X] - friction_force[X], a[Y] - friction_force[Y]]
    angle_of_velocity_vector = math.atan(velocity[Y], velocity[X])
    #this will turn the angle to the same angle of the drag force
    angle_drag_force = angle_of_velocity_vector + math.pi
    magnitude_of_velocity = math.sqrt(velocity[X]**2 + velocity[Y]**2)
    drag_force = profile_area * drag_coefficient * (density_of_air * magnitude_of_velocity ** 2) / 2
    a = [a[X] + math.cos(angle_drag_force) * drag_force , a[Y] + math.sin(angle_drag_force) * drag_force]
    if not on_ramp:
        a = [a[X], a[Y] - g * (mass_of_rocket + mass_of_fuel)]
    else:
        # here we calcuate and take into account the difference of the gravity force on the acceleration which will be paralel to the thrust and the ramp so that we don't have  
        # problem of keeping the rocket on the ramp or not
        # 180 = 90 + angle1 + angle2
        # 90 - angle1 = angle2
        magnitude_of_the_gravity_force = math.cos(math.pi/2 - angle_of_ramp) * g
        a = [a[X] - magnitude_of_the_gravity_force * math.cos(angle_of_ramp), a[Y] - magnitude_of_the_gravity_force * math.sin(angle_of_ramp)]
    return a

def calc_trajectory():
    """Will have a loop that will continue unless the rocket touches the floor and will increment the time by time_increment seconds"""
    #defining global variables
    global position
    global velocity
    global acceleration
    for t in np.arange(0, 100, time_increment):
        #calc acceleration taking into account last acceleration
        acceleration = calc_acceleration()
        #calc velocity taking into account last velocity
        # velocity = at + v0
        velocity = [acceleration[X] * time_increment + velocity[X], acceleration[Y] * time_increment + velocity[Y]]
        #calc position compared to last position
        # position = at^2/2 + vt+ x0
        position = [acceleration[X] * time_increment **2 / 2 + velocity[X] * time_increment + position[Y]]
        #if y of position is <= 0 end
        if position[Y] <= 0:
            break

if __name__ == '__main__':
    calc_trajectory()
