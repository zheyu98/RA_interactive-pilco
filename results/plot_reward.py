import numpy as np
import matplotlib.pyplot as plt

def plt_rwrd(time_str):
    rewards = np.load('./logs/' + time_str + '/rewards.npz')

    plt.plot(rewards['total_r'])

    print(rewards['predicted_r'])
    print(rewards['total_r'])

    return len(rewards['total_r'])

def plt_rwrd_fld(time_str):
    rewards = np.load('./logs/' + time_str + '/rewards.npz')

    plt.plot(rewards['lengths'], rewards['total_r_lengths'])

    print(rewards['predicted_r'])
    print(rewards['total_r_lengths'])
    print(rewards['lengths'])

    return len(rewards['total_r'])

def plt_rwrd_fld2(time_str):
    rewards = np.load('./examples/WithVarianceRuns/' + time_str + '/rewards.npz')

    plt.plot(rewards['total_r'])

    return len(rewards['total_r'])

#time_str1 = '23-03-2021-14:48:29'
#time_str2 = '23-03-2021-15:08:01'
time_str3 = '25-03-2021-11-33-32'
time_str4 = '25-03-2021-12.01.23'
time_str5 = '25-03-2021-03.48.19'
time_str6 = '25-03-2021-12.58.16'
time_str7 = '27-03-2021-15-05-33'

l = plt_rwrd_fld(time_str7)

#plt.xticks(range(l))
plt.xlabel('Trail [-]')
plt.ylabel('Reward [-]')
plt.show()