import numpy as np
import matplotlib.pyplot as plt

FILE = "output/states.csv"

data = np.loadtxt(FILE, delimiter=',')

print(data)

print(data.shape)

fig = plt.figure()
fig.set_size_inches(10, 6.0)

X = np.arange(0, data.shape[0])
Y = np.sum(data, axis=1) / data.shape[1]

plt.plot(X, Y)

plt.xlabel('Time step')
plt.ylabel('Infected percentage')
plt.show()
