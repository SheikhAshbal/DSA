import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.bar(['A', 'B'], [15, 42])
ax.set_title('Category Comparison')
ax.set_xlabel('Category')
ax.set_ylabel('Value')

plt.show()  # display the plot
fig.savefig('task2_bar.png', dpi=150, bbox_inches='tight')
print('bar chart rendered and saved as task2_bar.png')
