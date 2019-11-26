import glob, os
import numpy as np
import matplotlib.pyplot as plt
# 0.1_graph_0_infected_ratios.csv

# TODO: average results for all networks...


'''
unicode symbols  
\u03C6 - phi
\u03B3 - gamma
\u03BC - mu 
\u03BB - alfa
'''


def plot_graph(num_networks, file_type, display_steps):

    # folder path
    folder_name = 'output'

    # initiate variables
    parameter = 0.0
    labels = []

    fig = plt.figure()
    fig.set_size_inches(10, 6.0)

    os.chdir(folder_name)
    # i - additional iterator, iterates over graph number for each parameter value
    i = 0
    # read every file name in 'folder name' directory
    for file in glob.glob("*.csv"):
        # check if file name match - if not, skip
        if not '_graph_' in file and file_type in file:
            continue

        # read parameter value
        new_parameter = float(file[:3])

        # read_data
        data = np.loadtxt(file, delimiter=',')
        num_timesteps = data.shape[0]

        if new_parameter != parameter:

            # if not initial iteration get average and plot
            if parameter != 0.0:
                average = np.mean(all_data, axis=0)

                X = np.arange(0, display_steps)
                Y = average[:display_steps]

                plt.plot(X, Y)

                # get the average for matrix

            # data per network
            all_data = np.zeros((num_networks, num_timesteps))
            parameter = new_parameter
            labels.append("\u03B2=" + str(parameter))
            # reset graph iterator
            i = 0

        # read
        all_data[i, :] = data
        # increase iterator
        i += 1

    plt.xlabel('Time step')
    plt.ylabel('Infected percentage')
    plt.title("SI model: \u03C6=0, \u03B3=10, \u03BC=0, \u03BB=0, NumSim=250, Networks(scale free)=10")
    plt.legend(labels)
    plt.grid()
    plt.show()
    return


if __name__ == '__main__':

    plot_graph(num_networks=10, file_type='_infected_ratios', display_steps=25)
