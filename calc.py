import math
import numpy as np
import pygame
import sys

screenWidth = 1550 #~15.5m
screenHeight = 700 #~7m

pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((screenWidth,screenHeight))
screen.fill([255,255,255])
positions=[]

density_of_air = 1.225 #kg/m^3
drag_coefficient = 0.0001 #no unit / should be 0.00062
friction_coefficient = 0.1 #no unit
area_of_cap = 0.5
angle_of_ramp = 40 #in degrees
angle_of_ramp = math.radians(angle_of_ramp) #in radiants
g = 9.81
mass_of_rocket = 0.5
mass_of_fuel = 0.25
a = 12

time_increment = 0.001# in seconds

fuel_consumption_rate = 0.1# per seconds
ramp_length = 1
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
    #print("drag force = "+str(drag_coefficient * A * (density_of_air * v**2) / 2))
    return (drag_coefficient * A * (density_of_air * v**2) / 2)

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
        angle = math.atan(( pos_y - prev_pos_y )/( pos_x - prev_pos_x ))
        friction_force = [0,0]
    acceleration_x = a * math.cos(angle)
    acceleration_y = a * math.sin(angle)
    return [previous_velocity[0] + t * ( acceleration_x - (calc_drag_force(area_of_cap, previous_velocity[0]) + friction_force[0] * ( total_weight ))), previous_velocity[1] + t * ( acceleration_y - (calc_drag_force(area_of_cap, previous_velocity[1]) + friction_force[1] + ( total_weight  ) * g ))]
    #verify the x-velocity, if it's friction_force * weight

def consume_fuel():
    global mass_of_fuel
    global fuel_consumption_rate
    mass_of_fuel = mass_of_fuel - time_increment * fuel_consumption_rate
    if mass_of_fuel <= 0:
        mass_of_fuel = 0



def calc_v_at_ramp_end():
    global v_current_x
    global v_current_y
    global a
    global pos_x, pos_y, prev_pos_x, prev_pos_y
    #increment by time from t0 to t1
    for t in np.arange(0, 100, time_increment):
        
        #for the pygame window
        positions.append([pos_x,pos_y])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill([255,255,255])
        #pygame.draw.line(screen, (0, 0, 0), (0, screenHeight), (ramp_length*math.cos(angle_of_ramp)*100, screenHeight - ramp_length*math.sin(angle_of_ramp)*100), 4)
        for i in range(len(positions)):
            pygame.draw.rect(screen,(255,0, 0),[positions[i][0]*100,-positions[i][1]*100,2,2])
        pygame.display.flip()


        if (mass_of_fuel <= 0.0):
            a = 0
        acceleration = get_x_y_accelerations()
        v_next_x, v_next_y = calc_velocity(time_increment, acceleration[0], [v_current_x, v_current_y])

        v_current_x = v_next_x
        v_current_y = v_next_y
        prev_pos_x = pos_x
        prev_pos_y = pos_y
        pos_x = prev_pos_x + v_current_x* time_increment + ((time_increment**2)/2) * acceleration[0]
        pos_y = prev_pos_y + v_current_y* time_increment + ((time_increment**2)/2) * acceleration[1]

        print("posX: "+ str(pos_x))
        print("posY: "+ str(pos_y))
        consume_fuel()
        print("Mass of fuel: " + str(mass_of_fuel))
        print("Current speed: " + str( v_current_x))

calc_v_at_ramp_end()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill([255,255,255])
    pygame.draw.line(screen, (0, 0, 0), (0, screenHeight), (ramp_length*math.cos(angle_of_ramp)*100, ramp_length*math.sin(angle_of_ramp)*100), 4)
    for i in range(len(positions)):
        pygame.draw.rect(screen,(255,0, 0),[positions[i][0]*1000, screenHeight - positions[i][1],2,2]*1000)
    pygame.display.flip()