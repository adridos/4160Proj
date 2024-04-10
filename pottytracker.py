import time
import requests
from datetime import datetime
from gpiozero import MotionSensor

pir = MotionSensor(4)
server_url = 'http://35.192.215.225/tracker'
motion_detected_count = 0
start_time = None
wait_time = 60 # in seconds

while True:
    pir.wait_for_motion()
    
	#Checks to see if there is an initial start time since the last motion detection.
    if start_time is None:
        start_time = datetime.now()
        print("Motion Detected: Potty Break!")
        timestamp = start_time.strftime('%Y-%m-%d %H:%M:%S')
        print(f'Motion Detected at {timestamp}')
    
    motion_detected_count += 1
    time.sleep(1)  #avoids multiple detections for the same motion
    pir.wait_for_no_motion()

    # If the wait time has passed since the first detection, send the data to the server
    if (datetime.now() - start_time).total_seconds() >= wait_time:
        data = {'motion_detected': motion_detected_count, 'timestamp': timestamp}
        try:
            response = requests.post(server_url, json=data)
            print('Data sent to server:', response.text)
        except Exception as e:
            print('Error sending data to server:', e)
        
        # Resets the variables for the next detection
        start_time = None
        motion_detected_count = 0