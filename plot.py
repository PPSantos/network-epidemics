import numpy as np
import matplotlib.pyplot as plt

# TODO: average results for all networks...

# Plot infected ratio per time-step.
NETWORKS = ['test_network']

for net in NETWORKS:

    file_infected_ratio = "output/" + net + "_infected_ratios.csv" 
    data = np.loadtxt(file_infected_ratio, delimiter=',')

    print(data.shape)

    fig = plt.figure()
    fig.set_size_inches(10, 6.0)

    X = np.arange(0, data.shape[0])
    Y = data

    plt.plot(X, Y)

    plt.xlabel('Time step')
    plt.ylabel('Infected percentage')
    plt.show()
