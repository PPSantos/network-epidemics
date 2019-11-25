import glob, os
import numpy as np
import matplotlib.pyplot as plt
# 0.1_graph_0_infected_ratios.csv

# TODO: average results for all networks...

# Plot infected ratio per time-step.
NUMBER_NETWORKS = 10


folder_name = 'output'

parameter = 0.0


fig = plt.figure()
fig.set_size_inches(10, 6.0)

os.chdir(folder_name)
i = 0;
for file in glob.glob("*.csv"):
    # check if file name match - if not, skip
    if not '_graph_' in file:
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
            print(average)

            X = np.arange(0, 15)
            Y = average[:15]

            plt.plot(X, Y)

            # get the average for matrix

        # data per network
        all_data = np.zeros((NUMBER_NETWORKS, num_timesteps))
        parameter = new_parameter
        i = 0

    all_data[i, :] = data
    i += 1

for net in range(NUMBER_NETWORKS):

    file_infected_ratio = "output/graph_" + str(net) + "_infected_ratios.csv"




plt.xlabel('Time step')
plt.ylabel('Infected percentage')
plt.show()
