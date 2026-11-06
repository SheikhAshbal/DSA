import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title('Report Chart')
ax.set_xlabel('X Axis Label')

fig.savefig('report_chart.png', dpi=300, bbox_inches='tight')

print('file saved:', os.path.exists('report_chart.png'))
print('file size:', os.path.getsize('report_chart.png'), 'bytes')
