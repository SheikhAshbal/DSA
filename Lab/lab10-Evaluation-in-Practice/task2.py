from sklearn.metrics import confusion_matrix

y_true = [0, 0, 0, 0, 1, 1, 1, 1]
y_pred = [0, 0, 0, 1, 0, 1, 1, 1]

matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])

print("Confusion matrix:")
print(matrix)

tn, fp, fn, tp = matrix.ravel()

print("True negatives:", tn)
print("False positives:", fp)
print("False negatives:", fn)
print("True positives:", tp)
