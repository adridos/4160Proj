import psutil
import time

def monitor_resources(interval=1):
    while True:
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=None)

        # Get memory usage
        memory = psutil.virtual_memory()
        memory_total = memory.total
        memory_used = memory.used
        memory_percent = memory.percent

        # Get disk usage
        disk = psutil.disk_usage('/')
        disk_total = disk.total
        disk_used = disk.used
        disk_percent = disk.percent

        # Get network usage
        network = psutil.net_io_counters()
        network_bytes_sent = network.bytes_sent
        network_bytes_received = network.bytes_recv

        # Print resource usage
        print(f'CPU Usage: {cpu_percent}%')
        print(f'Memory Usage: {memory_used} / {memory_total} bytes ({memory_percent}%)')
        print(f'Disk Usage: {disk_used} / {disk_total} bytes ({disk_percent}%)')
        print(f'Network Usage: Sent: {network_bytes_sent} bytes, Received: {network_bytes_received} bytes')

        # Wait for the specified interval
        time.sleep(interval)

# Start monitoring resources
monitor_resources()
