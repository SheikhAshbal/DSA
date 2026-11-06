from sklearn.metrics import classification_report

y_true = [0, 0, 0, 0, 1, 1, 1, 1]
y_pred = [0, 0, 0, 1, 0, 1, 1, 1]

print(classification_report(y_true, y_pred, digits=2))
