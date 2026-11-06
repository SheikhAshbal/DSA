import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
series_a = [10, 20, 25, 30, 40]
series_b = [5, 15, 18, 22, 28]

fig, ax = plt.subplots()
ax.plot(x, series_a, color='tab:blue', linestyle='-',
        marker='o', label='Series A')
ax.plot(x, series_b, color='tab:red', linestyle='--',
        marker='s', label='Series B')

ax.set_title('Two series distinguished by colour and style')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()

fig.savefig('task2_accessible.png', dpi=150, bbox_inches='tight')
print('chart saved: task2_accessible.png')
print('legend entries: Series A (blue, solid, circle), Series B (red, dashed, square)')
