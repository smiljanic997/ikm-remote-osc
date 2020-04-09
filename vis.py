import matplotlib.pyplot as plt
import csv
import numpy as np
import pickle
from matplotlib import gridspec

LOCAL_PATH = '.received_data.pickle'

def visualize():
    time = []
    data = []

    received_dict = {}
    with open(LOCAL_PATH, 'rb') as f:
        received_dict = pickle.load(f)

    data = np.frombuffer(received_dict['rawdata'], 'B')
    voltoffset = received_dict['voltoffset']
    voltscale = received_dict['voltscale']
    timeoffset = received_dict['timeoffset']
    timescale = received_dict['timescale']

    data = data *(-1) + 255
    data = (data - 130.0 - voltoffset / voltscale * 25) / 25 * voltscale

    time = np.linspace(timeoffset - 6 * timescale, timeoffset + 6 * timescale, num=len(data))

    time = np.array(time)
    data = np.array(data)
            
    if (time[-1] < 1e-3):
        time = time * 1e6
        tUnit = 'µS'
    elif (time[-1] < 1):
        time = time * 1e3
        tUnit = 'mS'
    else:
        tUnit = "S"
        
            
    plt.plot(time, data)
    plt.title('Oscilloscope Channel 1')
    plt.ylabel('Voltage (V)')
    plt.xlabel('Time ({})'.format(tUnit))
    plt.xlim(time[0], time[-1])
    
    plt.grid()
    plt.show()

# $ python3 read_rpi.py proxy51.rt3.io 39429