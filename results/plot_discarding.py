import numpy as np
import matplotlib.pyplot as plt
import os


data_sets = []

for file in os.listdir('./results/Discarding/'):
    data_sets.append(np.load('./results/Discarding/' + file + '/rewards.npz'))

total_r = []
for data_set in data_sets:
    if data_set['total_r'][-1] > 10:
        total_r.append(data_set['total_r_changed'])
        plt.plot(np.concatenate(([1.0], data_set['lengths'])), data_set['total_r_changed'])

mean_var = np.mean(total_r, axis=0)
std_var = np.std(total_r, axis=0)

x = np.concatenate(([1.0], data_set['lengths']))

plt.xlabel('Pendulum Length [-]')
plt.xticks(x)
plt.ylabel('Total Reward [-]')
plt.savefig('discarding.png')
plt.show()



plt.plot(x, mean_var)
plt.fill_between(x, mean_var-2*std_var, mean_var+2*std_var, alpha=.1)

plt.xlabel('Pendulum Length [-]')
plt.xticks(x)
plt.ylabel('Total Reward [-]')
plt.savefig('discarding_conf.png')
plt.show()