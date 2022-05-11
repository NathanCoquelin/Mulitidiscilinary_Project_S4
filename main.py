import math
import numpy as np
import sys
import pygame




#initialize the output figure
figure = np.zeros((10, 150))
#defining constants to make the code more readable
X = 0
Y = 1
time_increment = 0.001

#ramp for use in on_ramp
ramp_length = 1
#inputing the angle of the ramp

#friction coefficient of the rocket on the ramp
friction_coefficient = 0.1
#masses in kg
mass_of_rocket = 0.5
#mass of fuel also in kg

# g the constant force of gravity
g = 9.81
#the trust of the rocket due to the chemical reaction
thrust = 15
#rate of consumption of the fuel in kg/s
consumption = 0.4
#drag coefficient
drag_coefficient = 0.000624
#density of air in kg/m^3
density_of_air = 1.225
#area on the front of the rocket in m^2
profile_area = 0.2

def on_ramp(position):
    """This function will check if the rocket is on the ramp by using the distance of position to the start position"""
    if math.sqrt(position[X]**2 + position[Y]**2) <= ramp_length:
        return True
    else:
        return False

def calc_acceleration(position, velocity, angle_of_ramp, mass_of_fuel):
    """
        This function will calculate the acceleration of the rocket wether its on the ramp or not
        if the rocket is on the ramp the gravity is neglected and the main acceleration is the thrust in direction of the ramp
    """
    a = [0, 0]
    if mass_of_fuel >= 0:
        if on_ramp(position):
            a = [math.cos(angle_of_ramp) * thrust, math.sin(angle_of_ramp) * thrust]
        else:
            #if not on the ramp and has fuel need to adapt
            a = [math.atan(velocity[Y] / velocity[X]) * thrust, math.atan(velocity[Y] / velocity[X]) * thrust]
    if on_ramp(position):
        #apply friction force
        normal_force = (mass_of_rocket + mass_of_fuel) * g * math.cos(angle_of_ramp)
        friction_force = [math.cos(angle_of_ramp) * friction_coefficient * normal_force, math.sin(angle_of_ramp) * friction_coefficient * normal_force]
        #adapt the acceleration to stay on the ramp
        a = [a[X] - friction_force[X], a[Y] - friction_force[Y]]
    angle_of_velocity_vector = math.atan(velocity[Y]/ velocity[X])
    #this will turn the angle to the same angle of the drag force
    angle_drag_force = angle_of_velocity_vector + math.pi
    magnitude_of_velocity = math.sqrt(velocity[X]**2 + velocity[Y]**2)
    drag_force = profile_area * drag_coefficient * (density_of_air * magnitude_of_velocity ** 2) / 2
    a = [a[X] + math.cos(angle_drag_force) * drag_force , a[Y] + math.sin(angle_drag_force) * drag_force]

    # calc gravity force
    if not on_ramp(position):
        a = [a[X], a[Y] - g * (mass_of_rocket + mass_of_fuel)]
    else:
        # here we calcuate and take into account the difference of the gravity force on the acceleration which will be paralel to the thrust and the ramp so that we don't have  
        # problem of keeping the rocket on the ramp or not
        # 180 = 90 + angle1 + angle2
        # 90 - angle1 = angle2
        magnitude_of_the_gravity_force = math.cos(math.pi/2 - angle_of_ramp) * g
        a = [a[X] - magnitude_of_the_gravity_force * math.cos(angle_of_ramp), a[Y] - magnitude_of_the_gravity_force * math.sin(angle_of_ramp)]
    return a

def consume_fuel(t, mass_of_fuel):
    if not(-0.5 <= mass_of_fuel and mass_of_fuel <= 0.0001):
        mass_of_fuel -= consumption * t
    else: 
        return

def calc_trajectory(angle_of_ramp, mass_of_fuel, disp):
    """Will have a loop that will continue unless the rocket touches the floor and will increment the time by time_increment seconds"""
    if disp == True:
        screenWidth = 1550 #~15.5m
        screenHeight = 700 #~7m

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((screenWidth,screenHeight))
        screen.fill([255,255,255])
        positions=[]
    #position of the rocket [x, y] initialized at 0, 0
    position = [0, 0]
    #velocity list of the rocket
    velocity = [0.000000001, 0.00000001]
    #acceleration list of the rocket
    acceleration = [0, 0]
    #converting it to radians
    angle_of_ramp = math.radians(angle_of_ramp)
    for t in np.arange(0, 10000, time_increment):
        consume_fuel(time_increment, mass_of_fuel)
        #calc acceleration taking into account last acceleration
        acceleration = calc_acceleration(position, velocity, angle_of_ramp, mass_of_fuel)
        #calc velocity taking into account last velocity
        # velocity = at + v0
        velocity = [acceleration[X] * time_increment + velocity[X], acceleration[Y] * time_increment + velocity[Y]]
        print(math.sqrt(velocity[X]**2 + velocity[Y]**2))
        #calc position compared to last position
        # position = at^2/2 + vt+ x0
        position = [acceleration[X] * time_increment **2 / 2 + velocity[X] * time_increment + position[X], acceleration[Y] * time_increment **2 / 2 + velocity[Y] * time_increment + position[Y]]
        #if y of position is <= 0 end
        if position[Y] <= 0:
            return position[X]


        #for the pygame window
        if disp == True:
            positions.append(position)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.fill([255,255,255])
            font = pygame.font.SysFont("calibri",20)
            for i in range(16):
                text = pygame.font.Font.render(font,str(i), True, (0, 0, 0))
                screen.blit(text,((100*i)+50, screenHeight - 35))
            #pygame.draw.line(screen, (0, 0, 0), (0, screenHeight), (ramp_length*math.cos(angle_of_ramp)*100, screenHeight - ramp_length*math.sin(angle_of_ramp)*100), 4)
            for i in range(len(positions)):
                if mass_of_fuel >= 0:
                    color_of_line = (255,0,0)
                else :
                    color_of_line = (0,0,255)
                pygame.draw.rect(screen,color_of_line,[positions[i][0]*100 + 50,screenHeight-(positions[i][1]*100) - 50,2,2])
            pygame.display.flip()

if __name__ == '__main__':
    calc_trajectory(45, 0.3, disp=True)
    # res_values = []
    # for angle_of_ramp in np.arange(30,  60, 1):
    #     for mass_of_fuel in np.arange(0,2,0.001):
    #         res = calc_trajectory(angle_of_ramp, mass_of_fuel, disp=False)
    #         print("******************************************************\n"+
    #             "angle of ramp\t" + str(angle_of_ramp) +
    #             "\tmass of fuel\t" + str(mass_of_fuel))
    #         print("Distance: \t\t\t\t" + str(res) + "\n")
    #         if 14.5 <= res and res <= 15.5:
    #             res_values.append([angle_of_ramp, mass_of_fuel])
    # print(res_values)

# print(position)
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#     screen.fill([255,255,255])
#     font = pygame.font.SysFont("calibri",20)
#     for i in range(16):
#         text = pygame.font.Font.render(font,str(i), True, (0, 0, 0))
#         screen.blit(text,((100*i)+50, screenHeight - 35))
#     #pygame.draw.line(screen, (0, 0, 0), (0, screenHeight), (ramp_length*math.cos(angle_of_ramp)*100, ramp_length*math.sin(angle_of_ramp)*100), 4)
#     for i in range(len(positions)):
#         pygame.draw.rect(screen,(255,0, 0),[(positions[i][0]*100) + 50,screenHeight-(positions[i][1]*100)-50,2,2])
#     pygame.display.flip()