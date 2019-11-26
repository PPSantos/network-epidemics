import glob, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib.cm as cm
# 0.1_graph_0_infected_ratios.csv

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
    for file in sorted(glob.glob("*.csv")):
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


def plot_graph_hardcoded():
    """
        HARDCODED VERSION.
    """
    fig = plt.figure()
    fig.set_size_inches(10, 6.0)

    PARAMETERS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    NUMBER_OF_NETWORKS = 10
    NUM_TIMESTEPS = 50

    DISPLAY_STEPS = 25

    LABELS = []

    scheme = cm.get_cmap("bwr", len(PARAMETERS))
    colors = scheme(np.linspace(0.0, 1.0, len(PARAMETERS)))

    # Make a user-defined colormap.
    cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",["r","b"])

    # Make a normalizer that will map the time values from
    # [start_time,end_time+1] -> [0,1].
    cnorm = mcol.Normalize(vmin=min(PARAMETERS),vmax=max(PARAMETERS))

    # Turn these into an object that can be used to map time values to colors and
    # can be passed to plt.colorbar().
    #cpick = cm.ScalarMappable(norm=cnorm,cmap=cm1)
    #cpick.set_array([])

    for (parameter, p) in zip(PARAMETERS, range(len(PARAMETERS))):

        all_data = np.zeros((NUMBER_OF_NETWORKS, NUM_TIMESTEPS))

        LABELS.append("\u03B2=" + str(parameter))

        for net in range(NUMBER_OF_NETWORKS):
            file_name = "output/{0}_graph_{1}_infected_ratios.csv".format(parameter, net)
            all_data[net,:] = np.loadtxt(file_name, delimiter=',')

        average = np.mean(all_data, axis=0)
        X = np.arange(0, DISPLAY_STEPS)
        Y = average[:DISPLAY_STEPS]

        #plt.plot(X, Y, color=cpick.to_rgba(parameter))
        plt.plot(X, Y, color=colors[p])

    plt.xlabel('Time step')
    plt.ylabel('Infected percentage')
    plt.title("SI model: \u03C6=0, \u03B3=10, \u03BC=0, \u03BB=0, NumSim=250, Networks(scale free)=10")
    plt.legend(LABELS)
    plt.grid()
    plt.show()

    return

def plot_threshold_timesteps():

    PARAMETERS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    NUMBER_OF_NETWORKS = 10

    THRESHOLD_1 = 0.8
    THRESHOLD_2 = 0.5

    Y_1 = np.zeros((len(PARAMETERS)))
    Y_2 = np.zeros((len(PARAMETERS)))

    for (parameter, p) in zip(PARAMETERS, range(len(PARAMETERS))):

        timesteps_1 = np.zeros((NUMBER_OF_NETWORKS))
        timesteps_2 = np.zeros((NUMBER_OF_NETWORKS))

        for net in range(NUMBER_OF_NETWORKS):
            file_name = "output/{0}_graph_{1}_infected_ratios.csv".format(parameter, net)
            data = np.loadtxt(file_name, delimiter=',')

            # Find the timestep at which the threshold was surpassed.
            timesteps_1[net] = np.argmax(data > THRESHOLD_1)
            timesteps_2[net] = np.argmax(data > THRESHOLD_2)

        Y_1[p] = np.average(timesteps_1)
        Y_2[p] = np.average(timesteps_2)

    if 0.0 in Y_1 or 0.0 in Y_2:
        print("ERROR")
    else:
        fig = plt.figure()
        fig.set_size_inches(10, 6.0)

        plt.plot(PARAMETERS, Y_1, label="80% infected threshold")
        plt.plot(PARAMETERS, Y_2, label="50% infected threshold")

        plt.xlabel('\u03B2')
        plt.ylabel('Average timesteps to surpass threshold')
        plt.title("SI model: \u03C6=0, \u03B3=10, \u03BC=0, \u03BB=0, NumSim=250, Networks(scale free)=10")
        plt.grid()
        plt.legend()
        plt.show()


def plot_dIdt():

    fig = plt.figure()
    fig.set_size_inches(10, 6.0)

    PARAMETERS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    NUMBER_OF_NETWORKS = 10

    # DISPLAY_STEPS SHOULD BE AT LEAST 1 TIMESTEP SMALLER THAN NUM_TIMESTEPS.
    NUM_TIMESTEPS = 50
    DISPLAY_STEPS = 25

    LABELS = []

    scheme = cm.get_cmap("bwr", len(PARAMETERS))
    colors = scheme(np.linspace(0.0, 1.0, len(PARAMETERS)))

    for (parameter, p) in zip(PARAMETERS, range(len(PARAMETERS))):

        all_data = np.zeros((NUMBER_OF_NETWORKS, NUM_TIMESTEPS))

        LABELS.append("\u03B2=" + str(parameter))

        for net in range(NUMBER_OF_NETWORKS):
            file_name = "output/{0}_graph_{1}_infected_ratios.csv".format(parameter, net)
            all_data[net,:] = np.loadtxt(file_name, delimiter=',')

        average = np.mean(all_data, axis=0)

        X = np.arange(0,NUM_TIMESTEPS)

        dI_dt = np.zeros((NUM_TIMESTEPS))
        # Caculate gradient.
        for t in range(NUM_TIMESTEPS-1):
            dI_dt[t] = average[t+1] - average[t]

        #plt.plot(X, Y, color=cpick.to_rgba(parameter))
        plt.plot(X[:DISPLAY_STEPS], dI_dt[:DISPLAY_STEPS], color=colors[p])

    plt.xlabel('Time step')
    plt.ylabel('Infected gradient (dI/dt)')
    plt.title("SI model: \u03C6=0, \u03B3=10, \u03BC=0, \u03BB=0, NumSim=250, Networks(scale free)=10")
    plt.legend(LABELS)
    plt.grid()
    plt.show()

    return

if __name__ == '__main__':

    # plot_graph(num_networks=10, file_type='_infected_ratios', display_steps=25)

    plot_graph_hardcoded()

    # plot_threshold_timesteps()

    plot_dIdt()