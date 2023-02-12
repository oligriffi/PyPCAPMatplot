import time
import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_network_traffic():
    # Define lists for storing the values
    x = []
    y = []
    udp = 0
    tcp = 0

    # Define the time interval
    time_interval = 15

    # Define the number of minutes to display
    num_minutes = 5

    # Get the starting values
    net_io_counters = psutil.net_io_counters(pernic=True)['ens33']
    prev_recv = net_io_counters.bytes_recv
    prev_sent = net_io_counters.bytes_sent

    # Function to be called every time interval
    def animate(i):
        nonlocal prev_recv, prev_sent, udp, tcp
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

        # Remove values older than 5 minutes
        if len(x) > num_minutes * 60 / time_interval:
            x.pop(0)
            y.pop(0)

        # Count the number of UDP and TCP packets
        if total_per_sec > 100000:
            udp += 1
        else:
            tcp += 1

        plt.clf()

        # Plot the line graph
        plt.subplot(1, 2, 1)
        plt.plot(x, y)
        plt.xlabel('Time (s)')
        plt.ylabel('Packet Count')
        plt.title('Live Network Traffic on ens33')
        plt.xlim(x[0], x[-1])

        # Plot the pie chart
        plt.subplot(1, 2, 2)
        labels = ['UDP', 'TCP']
        sizes = [udp, tcp]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True)
        plt.axis('equal')
        plt.title('Packet Types')

    # Call the animate function every time interval
    ani = FuncAnimation(plt.gcf(), animate, interval=time_interval * 1000)
    plt.tight_layout()
    plt.show()

# Call the function to start the


plot_network_traffic()
