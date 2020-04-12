import matplotlib.pyplot as plt
import csv
import numpy as np
import pickle

LOCAL_PATH = '.received_data.pickle'

def visualize(osc_params):
    """
    De-pickling and data adjusting.
    Creates a figure and plots data.
    """
    time = []
    data = []

    received_dict = {}
    with open(LOCAL_PATH, 'rb') as f:
        received_dict = pickle.load(f)

    data_1 = np.frombuffer(received_dict['rawdata_1'], 'B')
    data_2 = np.frombuffer(received_dict['rawdata_2'], 'B')
    voltoffset_1 = received_dict['voltoffset_1']
    voltoffset_2 = received_dict['voltoffset_2']
    voltscale = received_dict['voltscale']
    timeoffset = received_dict['timeoffset']
    timescale = received_dict['timescale']

    data_1 = data_1 *(-1) + 255
    data_1 = (data_1 - 130.0 - voltoffset_1 / voltscale * 25) / 25 * voltscale
    
    data_2 = data_2 *(-1) + 255
    data_2 = (data_2 - 130.0 - voltoffset_2 / voltscale * 25) / 25 * voltscale

    time = np.linspace(timeoffset - 6 * timescale, timeoffset + 6 * timescale, num=len(data_1))

    time = np.array(time)
    data_1 = np.array(data_1)
    data_2 = np.array(data_2)
    
    data_1 = data_1 + voltoffset_1
    data_2 = data_2 + voltoffset_2
    
    grid_x_pos = np.linspace(timeoffset, 5 * timescale + timeoffset, 6)
    grid_x_neg = np.linspace(-5 * timescale + timeoffset, timeoffset, 6)
    
    
    grid_y_pos = np.linspace(0, voltscale * 5, 6)
    grid_y_neg = np.linspace(-voltscale * 5, 0, 6)
    
    grid_x = np.concatenate([grid_x_neg, grid_x_pos])
    grid_y = np.concatenate([grid_y_neg, grid_y_pos])

            
    if (time[-1] < 1e-3):
        time = time * 1e6
        grid_x = grid_x * 1e6
        tUnit = 'µS'
    elif (time[-1] < 1):
        time = time * 1e3
        grid_x = grid_x * 1e3
        tUnit = 'mS'
    else:
        tUnit = "S"

        
    fig, ax = plt.subplots()
    ax.set_yticks(grid_y, minor=False)
    ax.set_yticks(grid_y, minor=True)
    ax.yaxis.grid(True, which='major')
    ax.yaxis.grid(True, which='minor')
    
    ax.set_xticks(grid_x, minor=False)
    ax.set_xticks(grid_x, minor=True)
    ax.xaxis.grid(True, which='major')
    ax.xaxis.grid(True, which='minor')

    ax.tick_params(direction='out', length=4, color='k', zorder=10)

    ax.set_ylabel('Voltage (V)')
    ax.set_xlabel('Time ({})'.format(tUnit))
    ax.set_xlim(time[0], time[-1])
    
    if osc_params['channel'] == '0':
        ax.plot(time, data_1, label='Prvi kanal')
        ax.plot(time, data_2, label='Drugi kanal')
    elif osc_params['channel'] == '1':
        ax.plot(time, data_1, label='Prvi kanal')
    elif osc_params['channel'] == '2':
        ax.plot(time, data_2, label='Drugi kanal')

    ax.legend()
    plt.show()
