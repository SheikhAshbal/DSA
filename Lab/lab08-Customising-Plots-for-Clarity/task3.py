import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

categories = ['Karachi', 'Lahore', 'Islamabad']
values = [120, 95, 80]

fig, ax = plt.subplots()
ax.bar(categories, values)
ax.set_ylim(bottom=0)
ax.set_title('Student enrollment by city')
ax.set_xlabel('City')
ax.set_ylabel('Students (count)')

print('y-axis limits:', ax.get_ylim())

fig.savefig('task3_honest_bar.png', dpi=150, bbox_inches='tight')
print('chart saved: task3_honest_bar.png')
