import numpy as np
import matplotlib.pyplot as plt

# TODO: average results for all networks...

# Plot infected ratio per time-step.
NUMBER_NETWORKS = 10

file_infected_ratio = "output/graph_0_infected_ratios.csv" 
data = np.loadtxt(file_infected_ratio, delimiter=',')
num_timesteps = data.shape[0]

all_data = np.zeros((NUMBER_NETWORKS,num_timesteps))

for net in range(NUMBER_NETWORKS):

    file_infected_ratio = "output/graph_" + str(net) + "_infected_ratios.csv" 
    all_data[net,:] = np.loadtxt(file_infected_ratio, delimiter=',')


all_data = np.mean(all_data, axis=0)

print(all_data)

fig = plt.figure()
fig.set_size_inches(10, 6.0)

X = np.arange(0, 15)
Y = data[:15]

plt.plot(X, Y)

plt.xlabel('Time step')
plt.ylabel('Infected percentage')
plt.show()
