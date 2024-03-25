import time
import requests
from datetime import datetime
from gpiozero import MotionSensor


pir = MotionSensor(4)
server_url = 'http://35.192.215.225'  # Change the IP address and port to your GCP server's address

while True:
	#pir.wait_for_motion()
	
	print("Motion Detected: Potty Break!")
	timestamp = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
	print(f'Motion Detected at {timestamp}')
	
	# Send data to the server
	data = {'motion_detected': True, 'timestamp': timestamp}
	try:
		response = requests.post(server_url, json=data)
		print('Data sent to server:', response.text)

	except Exception as e:
		print('Error sending data to server:', e)
	


	time.sleep(1) #avoid mult detections in one moment
	pir.wait_for_no_motion()

