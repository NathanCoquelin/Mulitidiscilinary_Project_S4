import math
import numpy as np

density_of_air = 1.225
drag_coefficient = 0.1
friction_coefficient = 0.1
area_of_cap = 0.5
angle_of_ramp = 40
angle_of_ramp = math.radians(angle_of_ramp)
g = 9.81
mass_of_rocket = 0.5
mass_of_fuel = 0.25
a = 12
# in seconds
time_increment = 0.01
# per seconds
fuel_consumption_rate = 0.1
on_ramp = True
v_current_x = 0
v_current_y = 0
pos_x = 0 
pos_y = 0
prev_pos_x = 0
prev_pos_y = 0

def get_x_y_accelerations():
    global angle_of_ramp
    global a
    return [a * math.cos(angle_of_ramp), a * math.sin(angle_of_ramp)]

def calc_drag_force(A, v):
    return drag_coefficient * A * (density_of_air * v**2) / 2

def calc_friction_force():
    if on_ramp:
        return [friction_coefficient * (mass_of_rocket + mass_of_fuel) * g * math.cos(angle_of_ramp) * math.sin(angle_of_ramp), friction_coefficient * ( mass_of_rocket + mass_of_fuel ) * g * math.sin(angle_of_ramp) * math.cos(angle_of_ramp)]
    else: 
        return 0

def calc_velocity(t, a, previous_velocity):
    global pos_x
    global pos_y
    total_weight = mass_of_fuel + mass_of_rocket
    if on_ramp:
        angle = angle_of_ramp
        friction_force = calc_friction_force()
    else :
        # toa
        angle = math.tan(( pos_y - prev_pos_x )/( pos_x - prev_pos_y ))
        friction_force = [0,0]
    acceleration_x = a * math.cos(angle)
    acceleration_y = a * math.sin(angle)
    return [previous_velocity[0] + t * ( acceleration_x - (calc_drag_force(area_of_cap, previous_velocity[0]) + friction_force[0] + ( total_weight ))), previous_velocity[1] + t * ( acceleration_y - (calc_drag_force(area_of_cap, previous_velocity[1]) + friction_force[1] + ( total_weight  ) * g ))]

def consume_fuel():
    global mass_of_fuel
    global fuel_consumption_rate
    mass_of_fuel = mass_of_fuel - time_increment / fuel_consumption_rate
    if mass_of_fuel <= 0:
        mass_of_fuel = 0



def calc_v_at_ramp_end():
    global v_current_x
    global v_current_y
    global a
    #increment by time from t0 to t1
    for t in np.arange(0, 100, time_increment):
        if (mass_of_fuel <= 0.0):
            a = 0
        acceleration = get_x_y_accelerations()
        v_next_x, v_next_y = calc_velocity(time_increment, acceleration[0], [v_current_x, v_current_y])

        v_current_x = v_next_x
        v_current_y = v_next_y

        consume_fuel()
        print("Mass of fuel: " + str(mass_of_fuel))
        print("Current speed: " + str( v_current_x))

calc_v_at_ramp_end()