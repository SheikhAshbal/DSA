import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

x = [1, 2, 3, 4]
y = [10, 20, 25, 30]

ax.plot(x, y, marker='o')
ax.set_title('Trend Over Time')
ax.set_xlabel('x')
ax.set_ylabel('y')

fig.savefig('task1_line.png', dpi=150, bbox_inches='tight')
print('line plot saved as task1_line.png')
print('axes type:', type(ax).__name__)
