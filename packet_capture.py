import time
import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_network_traffic():
    # Define lists for storing the values
    x = []
    y = []

    # Define the time interval
    time_interval = 15

    # Get the starting values
    net_io_counters = psutil.net_io_counters(pernic=True)['ens33']
    prev_recv = net_io_counters.bytes_recv
    prev_sent = net_io_counters.bytes_sent

    # Function to be called every time interval
    def animate(i):
        nonlocal prev_recv, prev_sent
        net_io_counters = psutil.net_io_counters(pernic=True)['ens33']
        bytes_recv = net_io_counters.bytes_recv
        bytes_sent = net_io_counters.bytes_sent
        received_per_sec = (bytes_recv - prev_recv) / time_interval
        sent_per_sec = (bytes_sent - prev_sent) / time_interval
        total_per_sec = received_per_sec + sent_per_sec
        x.append(i * time_interval)
        y.append(total_per_sec)
        prev_recv = bytes_recv
        prev_sent = bytes_sent

        plt.clf()
        plt.plot(x, y)
        plt.xlabel('Time (s)')
        plt.ylabel('Packet Count')
        plt.title('Live Network Traffic on ens33')

    # Call the animate function every time interval
    ani = FuncAnimation(plt.gcf(), animate, interval=time_interval * 1000)
    plt.tight_layout()
    plt.show()

# Call the function to start the graph
plot_network_traffic()

