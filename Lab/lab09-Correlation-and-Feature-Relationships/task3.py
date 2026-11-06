import matplotlib; matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5, 5, 100)
y = x**2  # perfect U-shape, fully determined by x

r = np.corrcoef(x, y)[0, 1]

plt.figure(figsize=(6,4))
plt.scatter(x, y, alpha=0.6)
plt.title('y = x^2 (non-linear relationship)')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('ushape.png', dpi=120, bbox_inches='tight')

print('correlation of x and x^2:', round(r, 4))
