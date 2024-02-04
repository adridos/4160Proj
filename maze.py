from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()

#Variables
r = (255, 0, 0)
b = (0, 0, 0)
w = (255,255,255)
f = (255,255,0)
x = 0
y = 1

#loop condition
game_over = False

#Moves marbles based on gyroscope orientation taken during while loop
def move_marble(pitch, roll, x, y):
    new_x = x
    new_y = y

    
    if (1 < pitch < 179) and x != 0:
        new_x -= 1
    elif (181 < pitch < 359) and x != 7:
        new_x += 1

    if (1 < roll < 179) and y != 7:
        new_y += 1
    elif (359 > roll > 179) and y != 0:
        new_y -= 1

    new_x, new_y = check_wall(x,y,new_x,new_y)
    
    return new_x, new_y
    
 

#Define maze boundaries
maze = [
        [r,r,r,r,r,r,r,r],
        [b,b,r,b,b,b,r,r],
        [r,b,r,b,r,b,b,r],
        [r,b,b,b,r,r,r,r],
        [r,r,r,b,b,b,b,r],
        [r,b,r,b,r,r,b,r],
        [r,b,b,b,r,r,b,r],
        [r,r,r,r,r,r,f,r]
    ]

#Checks if a given pixel is an "r" labels pixeled
def check_wall(x, y, new_x, new_y):
    if maze[new_y][new_x] != r:
        return new_x, new_y
    elif maze[new_y][x] != r:
        return x, new_y
    elif maze[y][new_x] != r:
        return new_x,y
    else:
        return x,y

def check_game(y, x):
    if maze[y][x] is f:
        return True
    else:
        return False

while game_over == False:

    #Gyroscope Orientation
    o = sense.get_orientation()
    pitch = o["pitch"]
    roll = o["roll"]

    #Sends pitch/roll values to move_marble to determine if the new position of x/y
    x, y = move_marble(pitch,roll,x,y)
    
    game_over = check_game(y,x)

    maze[y][x] = w

    
    #Sets new pixels
    sense.set_pixels(sum(maze, []))

    #Slows maze ball movement
    sleep(0.15)
    
    #The newly placed LED is removed immediately to allow for the new position of LED to be lit
    maze[y][x] = b

sense.clear()
sense.show_message("Your did it", text_colour=f, back_colour=b, scroll_speed=0.05)
