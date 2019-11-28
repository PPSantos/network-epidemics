import glob, os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib.cm as cm

'''
unicode symbols  
\u03B3 - gamma
\u03C6 - phi
\u03B2 - beta
\u0394 - delta
\u03BC - mu 
\u03A9 - omega
\u03BB - lambda

\u03BB - alfa
'''

def plot_graph(num_networks, file_type, display_steps):
    """
        Timestep VS infected ratio.
    """
    # folder path
    folder_name = 'output'

    # initiate variables
    parameter = 0.0
    labels = []

    fig = plt.figure()
    fig.set_size_inches(6.5, 4.5)

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

    fig.savefig('img/SI/beta_infected_ratios.pdf')

    return


def plot_graph_hardcoded():
    """
        Timestep VS infected ratio.
    """
    fig = plt.figure()
    fig.set_size_inches(6.5, 4.5)

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

    fig.savefig('img/SI/beta_infected_ratios.pdf')


    return

def plot_threshold_timesteps():
    """
        Parameter VS timestep at which threshold was surpassed.
    """
    PARAMETERS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    NUMBER_OF_NETWORKS = 10

    THRESHOLD_1 = 0.8
    THRESHOLD_2 = 0.2

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
        fig.set_size_inches(6.5, 4.5)

        plt.plot(PARAMETERS, Y_1, label="80% infected threshold")
        plt.plot(PARAMETERS, Y_2, label="50% infected threshold")

        plt.xlabel('\u03B2')
        plt.ylabel('Average timesteps to surpass threshold')
        plt.title("SI model: \u03C6=0, \u03B3=10, \u03BC=0, \u03BB=0, NumSim=250, Networks(scale free)=10")
        plt.grid()
        plt.legend()
        plt.show()

    fig.savefig('img/SI/beta_thresholds.pdf')



def plot_dIdt():
    """
        Timestep VS dI/dt.
    """
    fig = plt.figure()
    fig.set_size_inches(6.5, 4.5)


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

    fig.savefig('img/SI/beta_dI_dt.pdf')

    return

def plot_dIdt_2():
    """
        Infected (I) VS dI/dt.
    """
    fig = plt.figure()
    fig.set_size_inches(6.5, 4.5)

    PARAMETERS = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    NUMBER_OF_NETWORKS = 5

    # DISPLAY_STEPS SHOULD BE AT LEAST 1 TIMESTEP SMALLER THAN NUM_TIMESTEPS.
    NUM_TIMESTEPS = 50

    NUM_SIM = 20

    LABELS = []

    scheme = cm.get_cmap("bwr", len(PARAMETERS))
    colors = scheme(np.linspace(0.0, 1.0, len(PARAMETERS)))

    for (parameter, p) in zip(PARAMETERS, range(len(PARAMETERS))):

        LABELS.append("\u03B2=" + str(parameter))

        for net in range(NUMBER_OF_NETWORKS):

            for i in range(NUM_SIM):

                file_name = "output/{0}_graph_{1}_{2}_infected_ratios.csv".format(parameter, net, i)

                I = np.loadtxt(file_name, delimiter=',')

                dI_dt = np.zeros((NUM_TIMESTEPS-1))
                # Caculate gradient.
                for t in range(NUM_TIMESTEPS-1):
                    dI_dt[t] = I[t+1] - I[t]

                if (net == 0 and i == 0):

                    all_data = np.zeros((2, NUM_TIMESTEPS-1))

                    all_data[0,:] = I[:-1]
                    all_data[1,:] = dI_dt

                else:
                    aux = np.zeros((2, NUM_TIMESTEPS-1))
                    aux[0,:] = I[:-1]
                    aux[1,:] = dI_dt

                    all_data = np.concatenate([all_data, aux], axis=1)

        plt.scatter(all_data[0,:], all_data[1,:], color=colors[p])

    plt.xlabel('Infected percentage')
    plt.ylabel('Infected gradient (dI/dt)')
    plt.title("SI model: \u03C6=0, \u03B3=10, \u03BC=0, \u03BB=0")
    plt.legend(LABELS)
    plt.grid()
    plt.show()

    fig.savefig('img/SI/beta_dI_dt_2.pdf')

    return

def SIS_plot_infected_ratios():
    """
        Timestep VS infected ratio.
    """

    NUM_TIMESTEPS = 50

    DISPLAY_STEPS = 50

    fig = plt.figure()
    fig.set_size_inches(6.5, 4.5)

    Y = np.loadtxt("output/0.2_0.3_graph_0_infected_ratios.csv", delimiter=',')

    X = np.arange(0, DISPLAY_STEPS)

    plt.plot(X, Y[:DISPLAY_STEPS])

    print(Y[-1])

    plt.xlabel('Time step')
    plt.ylabel('Infected percentage')
    plt.title("SI model \n [\u03C6=0, \u03B3=10, \u03BC=0, \u03BB=0]")
    plt.ylim([0,1])
    plt.grid()
    plt.show()

    fig.savefig('img/SIS/test.pdf')


def SIS_plot_disease_prevalence():
    """
        SIS_2d_grid_plot
    """
    NUM_TIMESTEPS = 40
    DISPLAY_STEPS = 40

    NUMBER_OF_NETWORKS = 5

    PARAMETERS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

    data = np.zeros((11,11))

    fig = plt.figure()
    fig.set_size_inches(5.5, 4.0)

    for (beta, i) in zip(PARAMETERS, range(len(PARAMETERS))):
        for (delta, j) in zip(PARAMETERS, range(len(PARAMETERS))):

            nets_data = np.zeros((NUMBER_OF_NETWORKS))

            for net in range(NUMBER_OF_NETWORKS):
                file_name = "output/SIS_2d_grid_plot/{0}_{1}_graph_{2}_infected_ratios.csv".format(beta, delta, net)
                nets_data[net] = np.loadtxt(file_name, delimiter=',')[-1]

            data[i, j] = np.average(nets_data)

    data = np.flip(data, axis=0) * 100

    plt.imshow(data, interpolation='bicubic')

    plt.xlabel('Recovery rate (\u0394)')
    plt.ylabel('Infection rate (\u03B2)')
    plt.title("SIS model disease prevalence at stationary distribution\n [\u03B3=10]")
    ticks = np.linspace(0,100,11)
    cbar = plt.colorbar()
    cbar.set_ticks(ticks)
    cbar.set_label('Infected percentage (%)')
    plt.clim(0,100)

    plt.xlim([0.0,1.0])
    plt.ylim([1.0,0.0])

    ticks_pos_x = np.arange(0,11)
    ticks_labels_x = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0']
    plt.xticks(ticks_pos_x, ticks_labels_x)

    ticks_pos_y = np.arange(0,11)
    ticks_labels_y = ['1.0', '0.9', '0.8', '0.7', '0.6', '0.5', '0.4', '0.3', '0.2', '0.1', '0.0']
    plt.yticks(ticks_pos_y, ticks_labels_y)

    fmt_func = lambda x,pos: "{:1.0f}%".format(x)
    fmt = matplotlib.ticker.FuncFormatter(fmt_func)

    #plt.clabel(contours, inline=True, fontsize=8, fmt=fmt)

    contour = plt.contour(data, levels = [1,50,80], colors='w', legend='sd')
    contour.clabel(inline=True, fmt=fmt)

    plt.grid()
    plt.show()

    fig.savefig('img/SIS/disease_stationary_prevalence.pdf')

def plot_SIS_1():
    """
        Naive SIS model. FIX beta and vary delta.
    """
    fig = plt.figure()
    fig.set_size_inches(6.5, 4.5)

    PARAMETERS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    NUMBER_OF_NETWORKS = 10
    NUM_TIMESTEPS = 25

    DISPLAY_STEPS = 25

    LABELS = []

    scheme = cm.get_cmap("bwr", len(PARAMETERS))
    colors = scheme(np.linspace(0.0, 1.0, len(PARAMETERS)))

    # Make a user-defined colormap.
    cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",["r","b"])

    # Make a normalizer that will map the time values from
    # [start_time,end_time+1] -> [0,1].
    cnorm = mcol.Normalize(vmin=min(PARAMETERS),vmax=max(PARAMETERS))

    for (parameter, p) in zip(PARAMETERS, range(len(PARAMETERS))):

        all_data = np.zeros((NUMBER_OF_NETWORKS, NUM_TIMESTEPS))

        LABELS.append("\u0394=" + str(parameter))

        for net in range(NUMBER_OF_NETWORKS):
            file_name = "output/naive_SIS_delta_variation/{0}_graph_{1}_infected_ratios.csv".format(parameter, net)
            all_data[net,:] = np.loadtxt(file_name, delimiter=',')

        average = np.mean(all_data, axis=0)
        X = np.arange(0, DISPLAY_STEPS)
        Y = average[:DISPLAY_STEPS] * 100

        plt.plot(X, Y, color=colors[p])

    plt.xlabel('Time step')
    plt.ylabel('Infected percentage (%)')
    plt.title("SIS model \n [\u03B3=10, \u03B2=0.4]")
    plt.legend(LABELS)
    plt.grid()
    plt.show()

    fig.savefig('img/SIS/naive_SIS_model_delta_variation.pdf')

    return

def plot_SIS_1_1():
    """
        naive sis: vary delta and show stationary distribution change.
    """
    NUMBER_OF_NETWORKS = 10

    PARAMETERS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    fig = plt.figure()
    fig.set_size_inches(6.5, 4.5)

    results = np.zeros((len(PARAMETERS)))

    for (delta, i) in zip(PARAMETERS, range(len(PARAMETERS))):

        nets_data = np.zeros((NUMBER_OF_NETWORKS))

        for net in range(NUMBER_OF_NETWORKS):
            file_name = "output/naive_SIS_delta_variation/{0}_graph_{1}_infected_ratios.csv".format(delta, net)
            nets_data[net] = np.loadtxt(file_name, delimiter=',')[-1]

        results[i] = np.average(nets_data)

    plt.plot(PARAMETERS, results*100)

    plt.xlabel('Recovery rate (\u0394)')
    plt.ylabel('Infected stationary distributon (%)')
    plt.title("SIS model \n [\u03B3=10, \u03B2=0.4]")
    plt.ylim([0,100])
    plt.grid()
    plt.show()

    fig.savefig('img/SIS/naive_SIS_model_delta_variation_stationary_dist.pdf')


if __name__ == '__main__':

    # plot_graph(num_networks=10, file_type='_infected_ratios', display_steps=25)

    #plot_graph_hardcoded()

    #plot_threshold_timesteps()

    #plot_dIdt()

    #plot_dIdt_2()

    #SIS_plot_infected_ratios()

    #SIS_plot_disease_prevalence()

    #plot_SIS_1()

    plot_SIS_1_1()
