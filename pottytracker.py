import time
from datetime import datetime
from gpiozero import MotionSensor

pir = MotionSensor(4)

while True:
	pir.wait_for_motion()
	print("Motion Detected: Potty Break!")
	timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
	print(f'Motion Detected at {timestamp}')
	time.sleep(1) #avoid mult detections in one moment
	pir.wait_for_no_motion()

