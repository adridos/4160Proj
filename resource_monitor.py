import requests
import time

# Function to fetch monitoring information from the Flask API
def fetch_monitoring_info(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            monitoring_data = response.json()
            return monitoring_data
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Main loop to continuously fetch monitoring information
if __name__ == "__main__":
    # URL of your Flask API endpoint
    api_url = "http://34.29.5.213/monitoring"

    while True:
        # Fetch monitoring information from the API
        monitoring_info = fetch_monitoring_info(api_url)
        if monitoring_info:
            print("Monitoring Information:")
            print(f"CPU Usage: {monitoring_info['cpu_usage']}%")
            print(f"Memory Usage: {monitoring_info['memory_usage']}%")
            print(f"Disk Usage: {monitoring_info['disk_usage']}%")
            # Add more print statements for additional monitoring data if needed
        else:
            print("Failed to fetch monitoring information")

        # Wait for some time before fetching again (e.g., every 5 seconds)
        time.sleep(5)
