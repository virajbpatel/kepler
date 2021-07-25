import pygame as pg
import time
from math import * 
import numpy as np #Matplotlib uses NumPy for arrays
import matplotlib.pyplot as plt
import random as rdm
import pickle #For file handling

#Kepler

pg.init()

#Define some constants using a DICTIONARY
constants = {"G": 6.673*(10**(-11)),
             "M": 1.989*(10**30),
             "px_scale": 1*(10**10),
             "o_scale": 10**(9),
             "planet capacity": 25,
             "one year": 31683912
            }

#Scale is 1 pixel for 15,000,000,000m for distance but planets have a radius of 5px and the Sun has radius of 10px


#Create a screen with parts of the display having a surface to themselves
canRun = True
screen = pg.display.set_mode((1080,720))
space = pg.Surface((720,720))
display_panel = pg.Surface((360,480))
display_panel.fill((66,84,107))

#Use exception handling to open image files
try:
    logo = pg.image.load("Kepler Logo Colour.png")
    logo_large = pg.transform.scale(logo, (480, 240))
    logo = pg.transform.scale(logo, (100, 50))
    pauseplay_icon = pg.image.load("pauseplay.png")
    pauseplay_icon = pg.transform.scale(pauseplay_icon, (30,30))
    plus_icon = pg.image.load("Plus Icon.png")
    plus_icon = pg.transform.scale(plus_icon, (30,30))
    minus_icon = pg.image.load("Minus Icon.png")
    minus_icon = pg.transform.scale(minus_icon, (30,30))
except:
    print("Unexpected Error. Goodbye.")
    quit()

#Initiate fonts that I will use in the program
pg.font.init()
normalFont = pg.font.SysFont("Segoe UI", 20)
pauseFont = pg.font.SysFont("Segoe UI", 50)

#Draw the welcome screen
screen.fill([66,84,107])
screen.blit(logo_large, (300, 100))
welcome = pauseFont.render("Welcome", True, [0,0,0])
screen.blit(welcome, (450, 340))
load_button = pg.Surface((200, 30))
load_button.fill([117,117,117])
load_text = normalFont.render("Load Previous Session", True, [0,0,0])
load_button.blit(load_text, (5,0))
new_button = pg.Surface((150, 30))
new_button.fill([117,117,117])
new_text = normalFont.render("New Simulation", True, [0,0,0])
new_button.blit(new_text, (5,0))
screen.blit(load_button, (450, 420))
screen.blit(new_button, (475, 470))
welcome = True
paused = True
selected = False

#Create LIST of colours

colours = [[0,0,0], [255,255,0]]

    

#Create Merge Sort algorithm to sort list of planets in order of increasing orbit radius - SORTING ALGORITHM

def mergesort(alist):
    #First check that the list is longer than 1 item
    if len(alist) > 1 :
        #Find midpoint of list to split into 2
        mid = len(alist) // 2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]
        #Merge sort each half by calling the function again - RECURSIVE ALGORITHM
        mergesort(lefthalf)
        mergesort(righthalf)
        #Define some counters
        m = 0 #Represents the left half counter
        n = 0 #Represents the right half counter
        o = 0 #Represents the counter for the reassembled list
        #First find which item goes first in the new sorted list
        while m < len(lefthalf) and n < len(righthalf):
            #Smallest first
            if lefthalf[m].distanceFromSun < righthalf[n].distanceFromSun:
                alist[o] = lefthalf[m]
                m += 1
            else:
                alist[o] = righthalf[n]
                n += 1
            o += 1 #Move on to the next item of the new list
        #Next add the rest of the items to the reassembled list
        while m < len(lefthalf):
            alist[o] = lefthalf[m]
            m += 1
            o += 1
        while n < len(righthalf):
            alist[o] = righthalf[n]
            n += 1
            o += 1
    #Function is only applied if the list has a length greater than 1

class Star():
    def __init__(self, name, mass, sun_list):
        #Define properties of the star
        self.name = name
        self.mass = mass
        sun_list.append(self)

    def draw(self):
        #Draws star on the orbit screen
        pg.draw.circle(space, [255,255,0], [360,360], 10, 0)

class Planet:
    def __init__(self, name, mass, radius, distanceFromSun, planets):
        #Define properties of the planet
        self.name = name
        self.mass = mass
        self.radius = radius
        self.r = distanceFromSun/constants["px_scale"]
        self.distanceFromSun = distanceFromSun
        self.force = (constants["G"] * constants["M"] * self.mass)/((distanceFromSun)**2) #Newton's law of universal gravitation
        self.angular_velocity = sqrt(self.force / (self.mass * distanceFromSun))
        self.omega = (sqrt(self.force / (self.mass * distanceFromSun))) * constants["o_scale"]
        self.period = sqrt((4*(pi**2)*((distanceFromSun)**3))/(constants["G"]*constants["M"])) #Kepler's third law
        self.acceleration = (constants["G"]*self.mass)/((self.radius)**2)
        self.x_position = (360 + self.r * cos(radians(self.omega * time.time()))) #Uses parametric equations to represent the position as a VECTOR 
        self.y_position = (360 + self.r * sin(radians(self.omega * time.time())))
        self.colour = [0,0,0]
        for i in range(len(colours)):
            while self.colour == colours[i]: #Colours are part of a LIST
                self.colour = [rdm.randint(0,255), rdm.randint(0,255), rdm.randint(0,255)] #Chooses a unique random colour for the planet that will stay the same throughout the program
        colours.append(self.colour)
        #Store planets in a LIST
        planets.append(self)
        mergesort(planets)
        
    def graph(self, quantity):
        t = np.arange(0, constants["one year"], 1) #Uses NumPy to create a range of values for time
        r = self.distanceFromSun / 1000 #Reduces the distance to km because smaller numbers are easier to handle
        w = self.angular_velocity
        name = self.name
        #Uses selection to check the quantity and then draws a graph with labelled axes, title and legend
        #Draws x and y component on the same set of axes
        if quantity == "displacement":
            title = "Displacement of " + name
            plt.plot(t, (r * np.sin(w * t)), label = "y-compoonent")
            plt.plot(t, (r * np.cos(w * t)), label = "x-component") 
            plt.title(title)
            plt.xlabel("Time (s)")
            plt.ylabel("Displacement (km)")
            plt.legend()
            plt.show()
        elif quantity == "velocity":
            title = "Velocity of " + name
            plt.plot(t, (r * w * np.cos(w * t)), label = "y-compoonent")
            plt.plot(t, (r * w * -1 * np.sin(w * t)), label = "x-component") 
            plt.title(title)
            plt.xlabel("Time (s)")
            plt.ylabel("Velocity (km/s)")
            plt.legend()
            plt.show()
        elif quantity == "acceleration":
            title = "Acceleration of " + name
            plt.plot(t, (r * (w**2) * -1 * np.sin(w * t)), label = "y-compoonent")
            plt.plot(t, (r * (w**2) * -1 * np.cos(w * t)), label = "x-component") 
            plt.title(title)
            plt.xlabel("Time (s)")
            plt.ylabel("Acceleration (km/s^2)")
            plt.legend()
            plt.show()

    def orbit(self):
        #Sets controlling variables
        paused = False
        runOrbit = True
        radius = self.r
        omega = self.omega
        colour = self.colour
        #Draws planet at current position
        pg.draw.circle(space, colour, 
                            [int(round(self.x_position)), int(round(self.y_position))], 5, 0)
        screen.blit(space, [0,0])
        pg.display.flip()
        #Makes the screen black so the planet appears to move
        space.fill([0,0,0])
        screen.blit(space, [0,0])
        pg.display.flip()
        #Changes coordinates of vector to new postion
        self.x_position = (360 + radius*cos(radians(omega*time.time())))
        self.y_position = (360 + radius*sin(radians(omega*time.time())))
        #Checks if the pause button has been clicked
        x, y = pg.mouse.get_pos()
        for e in pg.event.get():
            if e.type == pg.MOUSEBUTTONDOWN:
                if (885 < x < 915) and (50 < y < 80):
                    paused = True
                    runOrbit = False
        #Tells the remaining program if the pause button has been clicked
        return runOrbit, paused
    
    def display_info(self):
        #Displays information of the planet
        print("---------------------------------------------------------------")
        print("Displaying Planet Info for", self.name)
        print("---------------------------------------------------------------")
        print("")
        print("Name:  ", self.name)
        print("Mass:  ", self.mass)
        print("Radius: ", self.radius)
        print("Distance from the Sun:  ", self.distanceFromSun)
        print("Angular Velocity:  ", self.angular_velocity)
        print("Gravitational Force:  ", self.force)
        print("Acceleration due to Gravity:  ", self.acceleration)
        print("Orbital Period (in seconds):  ", self.period)
        print("")
        print("---------------------------------------------------------------")

#Save simulation

def save(planets, sun_list):
    try:
        with open("previousSession.list", "wb") as previous_session_list: #Write binary mode
            #Loads contents of planets list into file
            pickle.dump(planets, previous_session_list) 
            print("Planets Saved")
        previous_session_list.close() #Closes file
    except:
        #Exception handling used when opening files
        print("Something went wrong. Sorry, couldn't save planets.")
    try:
        with open("sun.list", "wb") as sun_file:
            #Load sun information into file
            pickle.dump(sun_list, sun_file)
            print("Sun Saved")
        sun_file.close()
    except:
        print("Something went wrong. Sorry, couldn't save the Sun.")

#Loads previous session

def load():
    try:
        with open("previousSession.list", "rb") as previous_session_list: #Read binary mode
            #Loads contents of file into planets list
            planet_list = pickle.load(previous_session_list)
            print("Planets Loaded")
        #Allows rest of program to use planets list
        #Closes file
        previous_session_list.close()
    except:
        #Exception handling used when opening files
        print("Something went wrong. Planets couldn't load.")
    try:
        with open("sun.list", "rb") as sun_file:
            sun_list = pickle.load(sun_file)
            print("Sun Loaded")
        sun_file.close()
    except:
        ("Something went wrong. Sun couldn't load.")
    return planet_list, sun_list


def display_default(planets, sun):
    #Constructs the default screen using surfaces and buttons to make it interactive
    screen.fill((0,0,0))
    #Sets starting position of list for planet names
    y = 90
    #Draws side panel
    pg.draw.rect(screen,(66,84,107), (720,0,360,720))
    sun_button = pg.Surface((360,30))
    sun_button.fill([117,117,117])
    sun_string = sun.name + "'s Settings"
    sun_text = normalFont.render(sun_string, True, [0,0,0])
    sun_button.blit(sun_text, (0,0))
    screen.blit(sun_button, (720, 660))
    #Draws button for displacement, velocity and accelereation graphs
    s_button = pg.Surface((120, 30))
    s_button.fill([117,117,117])
    s_text = normalFont.render("s", True, [0,0,0])
    s_button.blit(s_text, (50,0))
    screen.blit(s_button, (720, 690))
    v_button = pg.Surface((120, 30))
    v_button.fill([117,117,117])
    v_text = normalFont.render("v", True, [0,0,0])
    v_button.blit(v_text, (50,0))
    screen.blit(v_button, (840, 690))
    a_button = pg.Surface((120, 30))
    a_button.fill([117,117,117])
    a_text = normalFont.render("a", True, [0,0,0])
    a_button.blit(a_text, (50,0))
    screen.blit(a_button, (960, 690))
    paused = pg.Surface((720,720))
    #Draws the pause screen
    paused.fill([117,117,117])
    pause_text = pauseFont.render("Paused", True, [255,255,255])
    paused.blit(pause_text, (300,335))
    #Blits the paused screen, side panel and buttons onto the screen
    screen.blit(paused, (0,0))
    screen.blit(logo, (850,1))
    screen.blit(pauseplay_icon, (885,50))
    screen.blit(minus_icon, (795,50))
    screen.blit(plus_icon, (975,50))
    #Displays the planet names in order of increasing distance from the sun
    for t in range(len(planets)):
        name = planets[t].name
        text = normalFont.render(name, False, [0,0,0])
        screen.blit(text, (722, y))
        y += 20
    pg.display.update()


#Adds new planets using the init function in the Planet class
def add(planets):
    if len(planets) < constants["planet capacity"]: #Checks that the planet LIST isn't already full yet
        valid = False
        #Sets a limit on distance from the Sun so the planets can be displayed on the screen
        min = 1.5e11
        max = 3.0e12
        #Exception handling approach when user fills in new planet form
        while valid == False:
            try:
                name = input("Enter Planet Name:  ")
                #Floats are easier to use for standard notation to represent large numbers
                mass = float(input("Enter Planet's Mass in kg:  "))
                radius = float(input("Enter Radius of Planet in m:  "))
                distance_from_sun = float(input("Enter distance between Planet and the Sun in m:  "))
                while (min > distance_from_sun) or (distance_from_sun > max):
                    print("Distance must be between (1.5 x 10^11) and (3 x 10^12). If distance is in the form a x 10^b, write in the form aeb.")
                    distance_from_sun = float(input("Enter distance between Planet and the Sun in m:  "))
                valid = True
            except ValueError:
                valid = False
        #Uses a temporary variable to store the inputted name of the planet
        temp = name
        #Uses temporary variable and vars function to create new object with given credentials
        vars()[temp] = Planet(name, mass, radius, distance_from_sun, planets)
        print("Planet Added")
    else:
        #Outputs statement to say that the planets list is already full but allows user to continue using the program
        print("Not enough space for more planets. You must delete a planet before adding a new one.")         
            
def delete(n, valid, planets): #This subroutine deletes a planet if the user has given valid permissions
    #Stores name of planet to verify later
    name = planets[n].name
    check = ""
    #Uses exception handling to make sure user inputs a valid input
    while valid == False:
        if check.upper() == "Y":
            del planets[n] #Deletes planet if user allows
            print("Planet " + name + " has been deleted.") #Confirmation of deletion
            valid = True
        elif check.upper() == "N":
            print("Planet " + name + " has not been deleted.") #Confirmation in case user accidentally attempts to delete a planet
            valid = True
        else:
            print("Please enter Y for yes or N for no.")
            check = input("Would you like to delete planet " + name + "? Y for yes, N for no. ") #Only allows a Y or an N as an input

def change_sun(sun, min_mass, sun_list):
    del sun
    mass = 0
    valid = False
    while valid == False:
        try:
            name = input("Enter new name: ")
            while mass <= min_mass:
                print("Mass must be larger than ", min_mass)
                mass = float(input("Enter new mass: "))
            valid = True
        except ValueError:
            print("Please enter a valid name.")
            valid = False
    sun = Star(name, mass, sun_list)
    return sun


def main(): #This is the main subroutine that connects all of the above classes and subroutines

    #Sets some boolean variables that will control what screen the program switches to
    default = False
    welcome = True
    selected = False

    #Main loop that only runs if the rest of the program can run
    while canRun:
        #First locates and tracks position of mouse so it knows where the user as clicked
        mouse_x, mouse_y = pg.mouse.get_pos()
        #Iterates through the events of the user's behaviour until either the user exits the window or the user clicks on something
        for event in pg.event.get():
            if event.type == pg.QUIT:
                #Saves simulation
                save(planets, sun_list)
                #Exiting the window causes the program to quit
                pg.quit()
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                #If the user has clicked, the program decides the following action based on the current boolean variable that is active and the current position of the mouse
                if (475 < mouse_x < 625) and (470 < mouse_y < 500) and (welcome == True):
                    planets = []
                    sun_list = []
                    #Goes from the welcome screen to the default screen
                    earth = Planet("Earth", 6e24, 6e6, 150e9, planets)
                    uranus = Planet("Uranus", 9e25, 25362000, 3e12, planets)
                    sun = Star("Sun", 2e30, sun_list)
                    welcome = False
                    display_default(planets, sun)
                    default = True
                    #Phase has shifted to show that the default screen is now shown
                elif (450 < mouse_x < 650) and (420 < mouse_y < 450) and (welcome == True):
                    planets, sun_list = load()
                    sun = sun_list[0]
                    welcome = False
                    display_default(planets, sun)
                    default = True
                elif welcome == False:
                    if default == True:
                        if (885 < mouse_x < 915) and (50 < mouse_y < 80): #Checks if the play button has been clicked
                            #Runs the orbit function
                            default = False
                            runOrbit = True
                            paused = False
                            while runOrbit == True:
                                for i in range(len(planets)):
                                    if runOrbit == True:
                                        #Checks if the pause button has been pressed
                                        runOrbit, paused = planets[i].orbit()
                                        sun.draw()
                            default = True
                            #If the pause button hass been clicked, it switches back to the default screen
                            display_default(planets, sun)
                        elif (975 < mouse_x < 1005) and (50 < mouse_y < 80): #Checks if the plus button has been clicked
                            #Adds planet
                            add(planets)
                        elif (720 < mouse_x < 1080) and (90 < mouse_y < 460): #Checks if the user has clicked on a planet
                            #Calculates which planet the user has clicked on using an equation
                            n = (mouse_y - 90) // 20
                            #Checks to see if the user has actually clicked on a planet or an empty space on the window
                            if len(planets) >= n:
                                if selected == False:
                                    #Draws a red circle next to the planet name if the planet hass been clicked on
                                    pg.draw.circle(screen, [255,0,0], (1073, (105 + 20*n)), 5)
                                    selected = True
                                    #If planet is clicked on, the planet information is displayed
                                    planets[n].display_info()
                                else:
                                    display_default(planets, sun)
                                    #If a pllanet has already been selected, the screen refreshes so the new planet is now selected
                                    pg.draw.circle(screen, [255,0,0], (1073, (105 + 20*n)), 5)
                                    selected = True
                                    planets[n].display_info()
                        elif (720 < mouse_x < 1080) and (660 < mouse_y < 690):
                            sun = change_sun(sun, planets[len(planets)-1].mass, sun_list)
                        elif selected == True:
                            if (795 < mouse_x < 825) and (50 < mouse_y < 80): #Checks if te user has clicked the minus button
                                #Deletes the planet but uses False to tell program that the user needs to verify/confirm before deletion
                                delete(n, False, planets)
                            elif (720 < mouse_x < 840) and (690 < mouse_y < 720): #Checks if the user has clicked on the graph displacement button
                                #Graphs the displacement of the planet selected
                                planets[n].graph("displacement")
                            elif (840 < mouse_x < 960) and (690 < mouse_y < 720): #Checks if the user has clicked on the graph velocity button
                                #Graphs the velocity of the planet selected
                                planets[n].graph("velocity")
                            elif (960 < mouse_x < 1080) and (690 < mouse_y < 720): #Checks if the user has clicked on the graph acceleration button
                                #Graphs the acceleration of the planet selected
                                planets[n].graph("acceleration")
                    #Uses error handling if a boolean variable has been incorrectly set so the program quits to restart
                    else:
                        print("Something went wrong.")
                        quit()
                else:
                    print("Something went wrong.")
                    quit()
                        

        pg.display.flip()

#Uses exception handling because if the main function can't run, neither can the rest of the program so the program quits to restart
try:
    main()
except:
    print("Ssomething went wrong.")
