import numpy as np

probs = np.array([0.1, 0.7, 0.1, 0.1])

predicted_class = probs.argmax()

print("probabilities  :", probs)
print("max value      :", probs.max())
print("predicted class:", predicted_class)
