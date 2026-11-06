import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

weeks = [1, 2, 3, 4, 5]
scores = [55, 62, 70, 75, 83]

fig, ax = plt.subplots()
ax.plot(weeks, scores, marker='o')
ax.set_title('Student scores improve steadily over 5 weeks')
ax.set_xlabel('Week (number)')
ax.set_ylabel('Score (out of 100)')

fig.savefig('task1_labelled.png', dpi=150, bbox_inches='tight')
print('chart saved: task1_labelled.png')
