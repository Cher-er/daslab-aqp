import numpy as np
import matplotlib.pyplot as plt

x = np.array([1, 2, 3, 4, 5, 6])

with open('ground_truth.csv') as f:
    ground_truth = np.array([line.strip() for line in f.readlines()]).astype(float)

with open('random_sampling_0.1.csv') as f:
    random_sampling_0_1 = np.array([line.strip() for line in f.readlines()]).astype(float)
    random_sampling_0_1 = np.abs(random_sampling_0_1 - ground_truth) / ground_truth

with open('samples_10000_aqp.csv') as f:
    vae_10000_10 = np.array([line.strip() for line in f.readlines()]).astype(float)
    vae_10000_10 = np.abs(vae_10000_10 - ground_truth) / ground_truth

with open('samples_100000_aqp.csv') as f:
    vae_100000_20 = np.array([line.strip() for line in f.readlines()]).astype(float)
    vae_100000_20 = np.abs(vae_100000_20 - ground_truth) / ground_truth

bar_width = 0.3

plt.bar(x - bar_width, random_sampling_0_1, label='Random Sampling', alpha=0.7, width=bar_width)
plt.bar(x, vae_10000_10, label='VAE_10000_10', alpha=0.7, width=bar_width)
plt.bar(x + bar_width, vae_100000_20, label='VAE_100000_20', alpha=0.7, width=bar_width)

plt.legend()

plt.xlabel('SQL')
plt.ylabel('Relative Error')

plt.xticks(x, ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6'])

plt.show()
