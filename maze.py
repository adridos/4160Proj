from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()

#Variables
r = (255, 0, 0)
b = (0, 0, 0)
w = (255,255,255)
x = 1
y = 1


game_over = False

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
        [r,b,b,b,b,b,b,r],
        [r,r,r,b,r,b,b,r],
        [r,b,r,b,r,r,r,r],
        [r,b,b,b,b,b,b,r],
        [r,b,r,r,r,r,b,r],
        [r,b,b,r,b,b,b,r],
        [r,r,r,r,r,r,r,r]
    ]
def check_wall(x, y, new_x, new_y):
    if maze[new_y][new_x] != r:
        return new_x, new_y
    elif maze[new_y][x] != r:
        return x, new_y
    elif maze[y][new_x] != r:
        return new_x,y
    else:
        return x,y
#Code setup

maze[y][x] = w

while game_over == False:

    #Orientation
    o = sense.get_orientation()
    pitch = o["pitch"]
    roll = o["roll"]
    yaw = o["yaw"]
    print("pitch {0}, roll {1}, yaw{2}, y {3}, x {4}".format(pitch,roll,yaw,y,x))
    x, y = move_marble(pitch,roll,x,y)
    maze[y][x] = w
    sense.set_pixels(sum(maze, []))
    sleep(0.15)
    maze[y][x] = b

   
#pixel setup

