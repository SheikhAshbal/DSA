import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

data = [1, 2, 2, 3, 3, 3, 4, 4, 5]

fig, ax = plt.subplots()

ax.hist(data, bins=3)
ax.set_title('Distribution of Values')
ax.set_xlabel('Value')
ax.set_ylabel('Frequency')

fig.savefig('task3_hist.png', dpi=150, bbox_inches='tight')
print('histogram saved as task3_hist.png')
