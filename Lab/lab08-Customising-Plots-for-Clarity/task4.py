import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

months = list(range(1, 13))
sales = [30, 35, 32, 40, 38, 42, 45, 90, 50, 48, 44, 40]

fig, ax = plt.subplots()
ax.plot(months, sales, marker='o')

peak_idx = sales.index(max(sales))
ax.annotate('Flash sale spike',
            xy=(months[peak_idx], sales[peak_idx]),
            xytext=(months[peak_idx] - 3, 75),
            arrowprops=dict(arrowstyle='->'))

ax.set_title('Monthly sales peak during flash sale event')
ax.set_xlabel('Month (number)')
ax.set_ylabel('Sales (units)')

fig.savefig('task4_annotated.png', dpi=150, bbox_inches='tight')
print('chart saved: task4_annotated.png')
print('annotation text: Flash sale spike at month', months[peak_idx],
      'value:', sales[peak_idx])
