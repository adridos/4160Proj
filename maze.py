import requests
from sense_hat import SenseHat
from time import sleep

from resource_monitor import fetch_monitoring_info


sense = SenseHat()
sense.clear()

#Initial prompt for user

print("Welcome to the Sense HAT Controller")
print("Press the joystick to interact with the Sense HAT")
print("Press the up arrow to send sensor data to the server")
print("Press the right arrow to start the maze game")
print("Press the down arrow to fetch monitoring information")
print("Press the left arrow to exit the program")

# Variables for maze game
r = (255, 0, 0)
b = (0, 0, 0)
w = (255, 255, 255)
f = (255, 255, 0)
x = 0
y = 1
maze = [
    [r, r, r, r, r, r, r, r],
    [b, b, r, b, b, b, r, r],
    [r, b, r, b, r, b, b, r],
    [r, b, b, b, r, r, r, r],
    [r, r, r, b, b, b, b, r],
    [r, b, r, b, r, r, b, r],
    [r, b, b, b, r, r, b, r],
    [r, r, r, r, r, r, f, r]
]
game_over = False

# Variables for sensor data
sensor_url = 'http://34.29.5.213/update-sensor-data'  # Update with your server details

# Function to read sensor data
def read_sensor_data():
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    return temperature, humidity

# Function to send sensor data to server
def send_sensor_data_to_server():
    temperature, humidity = read_sensor_data()
    if temperature is not None and humidity is not None:
        data = {'temperature': temperature, 'humidity': humidity}
        response = requests.post(sensor_url, json=data)
        if response.status_code == 200:
            print('Sensor data sent successfully')
        else:
            print('Failed to send sensor data')
    else:
        print('Failed to read sensor data')

# Function to move marble in the maze game
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

    new_x, new_y = check_wall(x, y, new_x, new_y)

    return new_x, new_y

def define_maze():
    # Define maze boundaries
    maze = [
        [r, r, r, r, r, r, r, r],
        [b, b, r, b, b, b, r, r],
        [r, b, r, b, r, b, b, r],
        [r, b, b, b, r, r, r, r],
        [r, r, r, b, b, b, b, r],
        [r, b, r, b, r, r, b, r],
        [r, b, b, b, r, r, b, r],
        [r, r, r, r, r, r, f, r]
    ]
    return maze

# Checks if a given pixel is an "r" labeled pixel
def check_wall(x, y, new_x, new_y):
    if maze[new_y][new_x] != r:
        return new_x, new_y
    elif maze[new_y][x] != r:
        return x, new_y
    elif maze[y][new_x] != r:
        return new_x, y
    else:
        return x, y

# Check if the game is over
def check_game(y, x):
    if maze[y][x] is f:
        return True
    else:
        return False

# Main loop for joystick control
while True:
    
    sense.set_pixels([
        b,b,b,r,r,b,b,b,
        b,b,b,r,r,b,b,b,
        b,b,b,b,b,b,b,b,
        r,r,b,b,b,b,r,r,
        r,r,b,b,b,b,r,r,
        b,b,b,b,b,b,b,b,
        b,b,b,r,r,b,b,b,
        b,b,b,r,r,b,b,b
    ])

    for event in sense.stick.get_events():
        if event.action == 'pressed':
            if event.direction == 'up':
                # Send sensor data when the up arrow is pressed
                send_sensor_data_to_server()
                                     
            elif event.direction == 'right':
                x = 0
                y = 1
                maze[y][x] = w
                maze = define_maze()
                # Start the maze game when the right arrow is pressed
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

                    for event in sense.stick.get_events():
                        if event.action == 'pressed' and event.direction == 'left':
                            game_over=True
                            break
                    
                # Clear the Sense HAT display after the game is over
                sense.clear()
                game_over = False
            
            elif event.direction == 'down':
                # Fetch monitoring information when the down arrow is pressed
                monitoring_info = fetch_monitoring_info("http://34.29.5.213/monitoring")
                if monitoring_info:
                    print("Monitoring Information:")
                    print(f"CPU Usage: {monitoring_info['cpu_usage']}%")
                    print(f"Memory Usage: {monitoring_info['memory_usage']}%")
                    print(f"Disk Usage: {monitoring_info['disk_usage']}%")
                    # Add more processing for additional monitoring data if needed
                else:
                    print("Failed to fetch monitoring information")

            elif event.direction == 'left':
                sense.clear()
                exit()
                
