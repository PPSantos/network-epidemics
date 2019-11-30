import glob, os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib.cm as cm
import matplotlib
import seaborn as sns
import pandas as pd
#from statsmodels.nonparametric.kernel_regression import KernelReg

'''
unicode symbols  
\u03C6 - phi
\u03B3 - gamma
\u03BC - mu 
\u03BB - lambda
\u03B2 - beta
'''

def plot_graph(num_networks, file_type, display_steps, plot_baseline):
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

    if plot_baseline:
        baseline_all_data = np.load('./output/baseline_alldata_0.7.npy')
        average_new = np.mean(baseline_all_data, axis=0)
        X = np.arange(0, display_steps)
        Y = average_new[:display_steps]
        plt.plot(X, Y * 100, '--', color='#ff0000')
        labels.append("baseline")



    os.chdir(folder_name)
    # i - additional iterator, iterates over graph number for each parameter value
    i = 0
    # read every file name in 'folder name' directory

    scheme = cm.get_cmap("Blues", 10)
    colors = scheme(np.linspace(0.0, 1.0, 10))

    # auxiliary iterators
    tmp = 0
    k = 0
    for file in sorted(glob.glob("*.csv")):
        # check if file name match - if not, skip
        if not '_graph_':
            continue

        # read parameter value
        new_parameter = float(file[:3])

        # read_data
        data = np.loadtxt(file, delimiter=',')
        num_timesteps = data.shape[0]


        # additional tmp to plot param ==1
        if new_parameter == 1:
            tmp += 1

        if tmp ==10:
            all_data[i, :] = data

        if new_parameter != parameter or tmp==10:


            # if not initial iteration get average and plot
            if parameter != 0.0:
                average = np.mean(all_data, axis=0)
                X = np.arange(0, display_steps)
                Y = average[:display_steps]

                plt.plot(X, Y*100, color=colors[k])
                k += 1

                # get the average for matrix

            # data per network
            all_data = np.zeros((num_networks, num_timesteps))
            parameter = new_parameter
            labels.append("\u03BB=" + str(parameter))
            # reset graph iterator
            i = 0


        # read
        all_data[i, :] = data
        # increase iterator
        i += 1


    plt.xlabel('Time step')
    plt.ylabel('Infected percentage (%)')
    plt.title("SI model\n[\u03C6 = 5, \u03B3 = 10, \u03B2 = 0.7, \u03BC = 0.7]")
    #plt.title("SI model, \n [\u03C6 = 0, \u03B3 = 10, \u03BC = 0, \u03BB = 0]")
    print("NumSim=200, Networks(scale free)=10")
    plt.legend(labels)
    plt.grid()

    plt.show()

    fig.savefig("../img/SI/lambda_mu07_beta07_numsim200_N10.pdf", format='pdf')


    return


def plot_graph_hardcoded():
    """
        Timestep VS infected ratio.
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

    fig.savefig('img/SI/beta_infected_ratios.pdf')


    return

def plot_threshold_timesteps(plot_baseline):
    """
        Parameter VS timestep at which threshold was surpassed.
    """
    PARAMETERS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    NUMBER_OF_NETWORKS = 10

    THRESHOLD_1 = 0.2
    THRESHOLD_2 = 0.4
    THRESHOLD_3 = 0.5

    if plot_baseline:
        baseline_all_data = np.load('./output/baseline_alldata_0.7.npy')

    Y_1 = np.zeros((len(PARAMETERS)))
    Y_2 = np.zeros((len(PARAMETERS)))
    Y_3 = np.zeros((len(PARAMETERS)))
    B_1 = np.zeros((len(PARAMETERS)))
    B_2 = np.zeros((len(PARAMETERS)))
    B_3 = np.zeros((len(PARAMETERS)))

    for (parameter, p) in zip(PARAMETERS, range(len(PARAMETERS))):

        timesteps_1 = np.zeros((NUMBER_OF_NETWORKS))
        timesteps_2 = np.zeros((NUMBER_OF_NETWORKS))
        timesteps_3 = np.zeros((NUMBER_OF_NETWORKS))

        timesteps_b_1 = np.zeros((NUMBER_OF_NETWORKS))
        timesteps_b_2 = np.zeros((NUMBER_OF_NETWORKS))
        timesteps_b_3 = np.zeros((NUMBER_OF_NETWORKS))


        for net in range(NUMBER_OF_NETWORKS):
            file_name = "output/{0}_graph_{1}_infected_ratios.csv".format(parameter, net)
            data = np.loadtxt(file_name, delimiter=',')

            # Find the timestep at which the threshold was surpassed.
            timesteps_1[net] = np.argmax(data > THRESHOLD_1)
            timesteps_2[net] = np.argmax(data > THRESHOLD_2)
            timesteps_3[net] = np.argmax(data > THRESHOLD_3)

            timesteps_b_1[net] = np.argmax(baseline_all_data[net,:] > THRESHOLD_1)
            timesteps_b_2[net] = np.argmax(baseline_all_data[net,:] > THRESHOLD_2)
            timesteps_b_3[net] = np.argmax(baseline_all_data[net,:] > THRESHOLD_3)


        Y_1[p] = np.average(timesteps_1)
        Y_2[p] = np.average(timesteps_2)
        Y_3[p] = np.average(timesteps_3)


        B_1[p] = np.average(timesteps_b_1)
        B_2[p] = np.average(timesteps_b_2)
        B_3[p] = np.average(timesteps_b_3)

    if 0.0 in Y_1 or 0.0 in Y_2 or 0.0 in Y_3:
        print("ERROR")
    else:
        fig = plt.figure()
        fig.set_size_inches(6.5, 4.5)

        plt.plot(PARAMETERS, Y_2, label="40% infected threshold", color='#0066ff')
        plt.plot(PARAMETERS, Y_1, label="20% infected threshold", color='#dd3333')
        plt.plot(PARAMETERS, Y_3, label="50% infected threshold", color='#ff3333')

        if plot_baseline:
            plt.plot(PARAMETERS, B_2, '--', label="40% infected, baseline", color='#660033')
            plt.plot(PARAMETERS, B_1, '--', label="20% infected, baseline", color='#440033')
            plt.plot(PARAMETERS, B_3, '--', label="50% infected, baseline", color='black')


        plt.xlabel('Awarness spread (\u03BB)')
        plt.ylabel('Average timesteps to surpass threshold')
        plt.title("SI model\n[\u03C6 = 5, \u03B3 = 10, \u03B2 = 0.7, \u03BC = 0.7]")
        plt.grid()
        plt.legend()
        plt.show()

        fig.savefig('./img/SI/lambda_mu07_beta0_7_thresholds_200_N10.pdf')


def plot_dIdt(plot_baseline):
    """
        Timestep VS dI/dt.
    """
    fig = plt.figure()
    fig.set_size_inches(6.5, 4.5)

    PARAMETERS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    NUMBER_OF_NETWORKS = 10

    if plot_baseline:
        baseline_all_data = np.load('./output/baseline_alldata_0.7.npy')

    # DISPLAY_STEPS SHOULD BE AT LEAST 1 TIMESTEP SMALLER THAN NUM_TIMESTEPS.
    NUM_TIMESTEPS = 50
    DISPLAY_STEPS = 25

    LABELS = []

    scheme = cm.get_cmap("Blues", len(PARAMETERS))
    colors = scheme(np.linspace(0.0, 1.0, len(PARAMETERS)))

    for (parameter, p) in zip(PARAMETERS, range(len(PARAMETERS))):

        all_data = np.zeros((NUMBER_OF_NETWORKS, NUM_TIMESTEPS))

        LABELS.append("\u03BB=" + str(parameter))

        for net in range(NUMBER_OF_NETWORKS):
            file_name = "output/{0}_graph_{1}_infected_ratios.csv".format(parameter, net)
            all_data[net,:] = np.loadtxt(file_name, delimiter=',')

        average = np.mean(all_data, axis=0)
        average_baseline = np.mean(baseline_all_data, axis=0)

        X = np.arange(0,NUM_TIMESTEPS)

        dI_dt = np.zeros((NUM_TIMESTEPS))
        dI_dt_baseline = np.zeros((NUM_TIMESTEPS))
        # Caculate gradient.
        for t in range(NUM_TIMESTEPS-1):
            dI_dt[t] = average[t+1] - average[t]
            dI_dt_baseline[t] = average_baseline[t+1] - average_baseline[t]

        #plt.plot(X, Y, color=cpick.to_rgba(parameter))
        plt.plot(X[:DISPLAY_STEPS], dI_dt[:DISPLAY_STEPS], color=colors[p])
        if plot_baseline and parameter == 1.0:
            plt.plot(X[:DISPLAY_STEPS], dI_dt_baseline[:DISPLAY_STEPS], '--', color='red')
            LABELS.append('baseline')

    plt.xlabel('Time step')
    plt.ylabel('Infected gradient (dI/dt)')
    plt.title("SI model\n[\u03C6 = 5, \u03B3 = 10, \u03B2 = 0.7, \u03BC = 0.7]")
    plt.legend(LABELS)
    plt.grid()
    plt.show()


    fig.savefig('./img/SI/lambda_mu07_beta_0_7_dI_dt_numsim200_N10.pdf', format='pdf')
    #fig.savefig("../img/SI/beta_infected_ratios_numsim200_N10.pdf", format='pdf')

    return

def plot_dIdt_2():
    """
        Infected (I) VS dI/dt.
    """
    fig = plt.figure()
    fig.set_size_inches(10, 6.0)

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
    plt.title("SI model: \u03C6 = 0, \u03B3=10, \u03BC=0, \u03BB=0")
    plt.legend(LABELS)
    plt.grid()
    plt.show()

    fig.savefig('img/SI/beta_dI_dt_2.pdf')
    #fig.savefig("../img/SI/beta_infected_ratios_numsim200_N10.pdf", format='pdf')

    return


def plot_barchart():

    PARAMETERS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    NUMBER_OF_NETWORKS = 10

    TRESHOLDS = [0.5, 0.7, 0.90]
    # TRESHOLDS = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]

    baseline_all_data = np.load('./output/baseline_alldata_0.7.npy')

    extensions = np.zeros((len(TRESHOLDS),len(PARAMETERS)))

    for (treshold, t) in zip(TRESHOLDS, range(len(TRESHOLDS))):
        Y_1 = np.zeros((len(PARAMETERS)))
        B_1 = np.zeros((len(PARAMETERS)))

        timesteps_1 = np.zeros((NUMBER_OF_NETWORKS))
        timesteps_b_1 = np.zeros((NUMBER_OF_NETWORKS))

        for (parameter, p) in zip(PARAMETERS, range(len(PARAMETERS))):

            for net in range(NUMBER_OF_NETWORKS):
                file_name = "output/{0}_graph_{1}_infected_ratios.csv".format(parameter, net)
                data = np.loadtxt(file_name, delimiter=',')

                # Find the timestep at which the threshold was surpassed.
                timesteps_1[net] = np.argmax(data > treshold)

                timesteps_b_1[net] = np.argmax(baseline_all_data[net,:] > treshold)

            Y_1[p] = np.average(timesteps_1)

            B_1[p] = np.average(timesteps_b_1)

            extensions[t,p] = 1+((Y_1[p]-B_1[p])/B_1[p])

    extensions_avg = np.mean(extensions, axis=0)
    print(extensions_avg.shape)
    fig = plt.figure()
    fig.set_size_inches(6.5, 4.5)

    #plt.bar(x=PARAMETERS,height=extensions_avg)
    df = pd.DataFrame(columns=['parameters', 'extensions', 'tresholds'])
    df['parameters'] = PARAMETERS
    df['extensions'] = extensions[0,:]
    df['tresholds'] = str(TRESHOLDS[0])
    df1 = pd.DataFrame(columns=['parameters', 'extensions', 'tresholds'])
    df1['parameters'] = PARAMETERS
    df1['extensions'] = extensions[1,:]
    df1['tresholds'] = str(TRESHOLDS[1])
    df2 = pd.DataFrame(columns=['parameters', 'extensions', 'tresholds'])
    df2['parameters'] = PARAMETERS
    df2['extensions'] = extensions[2,:]
    df2['tresholds'] = str(TRESHOLDS[2])



    df_total = pd.concat([df, df1, df2], axis=0)
    sns.set(style="whitegrid")
    ax = sns.barplot(x='parameters', y='extensions', hue='tresholds', data=df_total,  palette="Blues")


    # df = pd.DataFrame(columns=['parameters', 'extensions', 'treshold'])
    # df['parameters'] = PARAMETERS
    # df['extensions'] = extensions_avg
    # sns.barplot(x='parameters', y='extensions', data=df, palette="Blues_d")
    plt.xlabel('Disease decay while aware (\u03BB)')
    plt.ylabel('Expansion time for given treshold')
    plt.title("SI model\n[\u03C6 = 5, \u03B3 = 10, \u03B2 = 0.7, \u03BC = 0.7]")
    plt.grid()
    plt.show()

    fig.savefig('img/SI/SI_lambda_mu07_tresholds_percent_speed.pdf')

    return

def SIS_plot_disease_prevalence():
    """
        SIS_2d_grid_plot
    """
    NUM_TIMESTEPS = 40
    DISPLAY_STEPS = 40

    NUMBER_OF_NETWORKS = 5

    PARAMETERS = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    TRESHOLDS = 0.4

    baseline = './output/0.0_0.0_graph_0_infected_ratios.csv'
    baseline_all_data = np.loadtxt(baseline, delimiter=',')

    # data = np.zeros((11,11))
    data = np.full(shape=(11,11), fill_value=10000)

    fig = plt.figure()
    fig.set_size_inches(5.5, 4.0)

    # Y_1 = np.zeros((len(PARAMETERS)))
    Y_1 = np.full(shape=len(PARAMETERS), fill_value=10000)
    # B_1 = np.zeros((len(PARAMETERS)))
    B_1 = np.full(len(PARAMETERS), fill_value=10000)

    # timesteps_1 = np.zeros((NUMBER_OF_NETWORKS))
    timesteps_1 = np.full((NUMBER_OF_NETWORKS), fill_value=100)
    # timesteps_b_1 = np.zeros((NUMBER_OF_NETWORKS))
    timesteps_b_1 = np.full((NUMBER_OF_NETWORKS), fill_value=100)


    for (mu, i) in zip(PARAMETERS, range(len(PARAMETERS))):
        for (lambdaa, j) in zip(PARAMETERS, range(len(PARAMETERS))):

            # nets_data = np.zeros((NUMBER_OF_NETWORKS))

            for net in range(NUMBER_OF_NETWORKS):
                file_name = "output/{0}_{1}_graph_{2}_infected_ratios.csv".format(mu, lambdaa, net)
                # nets_data[net] = np.loadtxt(file_name, delimiter=',')
                data_net = np.loadtxt(file_name, delimiter=',')

                # Find the timestep at which the threshold was surpassed.
                argmax = np.argmax(data_net > TRESHOLDS)
                # if  argmax == 0 :
                #     timesteps_1[net] = 1000
                # else:
                #     timesteps_1[net] = argmax
                timesteps_1[net] = argmax
                timesteps_b_1[net] = np.argmax(baseline_all_data > TRESHOLDS)


            Y_1[j] = np.average(timesteps_1)

            B_1[j] = np.average(timesteps_b_1)


            # data[i, j] = 1+((Y_1[j]-B_1[j])/B_1[j])
            data[i, j] = Y_1[j]

    data = np.flip(data, axis=0)

    plt.imshow(data, interpolation='bicubic')

    # \u03BC - mu
    # \u03BB -lambda

    plt.xlabel('Infection decay while aware (\u03BB)')
    plt.ylabel('Awareness spread rate (\u03BC)')
    plt.title("Awarness impact on time of reaching the treshould of "+str(TRESHOLDS)+"\n[ \u03B2 = 0.7, \u03BC = 0.7 \u03B3=10]")
    ticks = np.linspace(0,100,11)
    cbar = plt.colorbar()
    # cbar.set_ticks(ticks)
    cbar.set_label('Timestepts to reach the treshold')
    # plt.clim(0,100)
    #
    plt.ylim([1.0,0.0])
    plt.xlim([0.0,1.0])

    ticks_pos_x = np.arange(0,11)
    ticks_labels_x = ['0.0', '0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.99']
    plt.xticks(ticks_pos_x, ticks_labels_x)

    ticks_pos_y = np.arange(0,11)
    ticks_labels_y = ['1.0', '0.9', '0.8', '0.7', '0.6', '0.5', '0.4', '0.3', '0.2', '0.1', '0.0']
    plt.yticks(ticks_pos_y, ticks_labels_y)
    #
    fmt_func = lambda x,pos: "{:1.0f}".format(x)
    fmt = matplotlib.ticker.FuncFormatter(fmt_func)

    # plt.clabel(contours, inline=True, fontsize=8, fmt=fmt)

    contour = plt.contour(data, levels = [6,7,8,10, 14, 20 ,35, 200], colors='w', legend='sd')
    contour.clabel(inline=True, fmt=fmt)

    plt.grid()
    plt.show()

    fig.savefig('img/SI/mu_lambda_prevelance_treshold'+str(TRESHOLDS)+'.pdf')


if __name__ == '__main__':

    #plot_graph(num_networks=10, file_type='_infected_ratios', display_steps=45, plot_baseline=True)

    #plot_graph_hardcoded()

    #plot_threshold_timesteps(plot_baseline=True)

    #plot_dIdt(plot_baseline=True)

    #plot_dIdt_2()

    #plot_barchart()

    #plot_dIdt_2()

    SIS_plot_disease_prevalence()
