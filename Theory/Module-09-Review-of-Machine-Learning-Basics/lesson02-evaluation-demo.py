"""Evaluate fixed binary predictions and scores; no model is trained here."""
import argparse
import math
from pathlib import Path

import numpy as np
from sklearn.metrics import (
    accuracy_score, confusion_matrix, precision_score,
    recall_score, f1_score, roc_auc_score, roc_curve,
)

Y_TRUE = np.array([1,1,1,1,0,0,0,0,0,0])
Y_PRED = np.array([1,1,0,0,1,0,0,0,0,0])
ROC_Y = np.array([0,0,0,0,1,1,1,1])
SCORES_A = np.array([0.1,0.2,0.3,0.6,0.4,0.7,0.8,0.9])
SCORES_B = np.full(8,0.5)


def from_counts(tp,fn,fp,tn):
    counts = (tp,fn,fp,tn)
    if not all(isinstance(value,(int,np.integer)) and value >= 0 for value in counts):
        raise ValueError("Counts must be nonnegative integers.")
    total = sum(counts)
    if total == 0:
        raise ValueError("At least one observation is required.")
    return {
        "accuracy": (tp+tn)/total,
        "precision": tp/(tp+fp) if tp+fp else None,
        "recall": tp/(tp+fn) if tp+fn else None,
        "f1": 2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None,
        "fpr": fp/(fp+tn) if fp+tn else None,
    }


def threshold_metrics(threshold):
    if not math.isfinite(threshold):
        raise ValueError("Use a finite threshold.")
    prediction = (SCORES_A >= threshold).astype(int)
    tn,fp,fn,tp = confusion_matrix(ROC_Y,prediction,labels=[0,1]).ravel()
    return from_counts(tp,fn,fp,tn)


def make_plots(output):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"svg.fonttype":"none","font.size":10})
    fig,axes = plt.subplots(2,2,figsize=(12,8),layout="constrained")
    fig.suptitle("Classification evaluation: counts, imbalance, and thresholds",fontsize=16)
    matrix = confusion_matrix(Y_TRUE,Y_PRED,labels=[0,1])
    ax = axes[0,0]
    ax.imshow(matrix,cmap="Blues",vmin=0,vmax=5)
    for i in range(2):
        for j in range(2):
            label = [["TN","FP"],["FN","TP"]][i][j]
            ax.text(j,i,f"{label} = {matrix[i,j]}",ha="center",va="center",
                    color="white" if matrix[i,j] >= 4 else "#111111")
    ax.set(xticks=[0,1],xticklabels=["Negative (0)","Positive (1)"],
           yticks=[0,1],yticklabels=["Negative (0)","Positive (1)"],
           xlabel="Predicted label",ylabel="Actual label",title="Ten-row fixture: matrix orientation matters")

    ax = axes[0,1]
    bars = ax.bar(["Accuracy","Fraud recall"],[99,0],color=["#2166ac","#c85b16"])
    ax.bar_label(bars,labels=["99%","0%"],padding=4)
    ax.set(ylim=(0,110),ylabel="Percent",title="Never-fraud baseline: misses all 100 frauds")

    ax = axes[1,0]
    for scores,name,colour in [(SCORES_A,"A","#2166ac"),(SCORES_B,"B","#c85b16")]:
        fpr,tpr,_ = roc_curve(ROC_Y,scores,drop_intermediate=False)
        area = roc_auc_score(ROC_Y,scores)
        ax.plot(fpr,tpr,marker="o",color=colour,label=f"Model {name}: AUC {area:.4f}")
    ax.set(xlim=(-0.03,1.03),ylim=(-0.03,1.03),xlabel="False-positive rate",ylabel="True-positive rate (recall)",title="ROC uses scores across thresholds")
    ax.legend(frameon=False,fontsize=9,loc="lower right")

    ax = axes[1,1]
    thresholds = [0.1,0.4,0.5,0.7,0.9]
    results = [threshold_metrics(value) for value in thresholds]
    ax.plot(thresholds,[row["precision"] for row in results],marker="o",label="Precision",color="#2166ac")
    ax.plot(thresholds,[row["recall"] for row in results],marker="s",label="Recall",color="#c85b16")
    ax.set(ylim=(0,1.08),xlabel="Threshold (positive if score >= threshold)",ylabel="Metric",title="Precision is not necessarily monotonic")
    ax.legend(frameon=False,fontsize=9,loc="lower left")
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,format="svg")
    fig.savefig(output.with_suffix(".png"),dpi=130)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot",action="store_true",help="Requires Matplotlib")
    args = parser.parse_args()
    print("Confusion matrix, rows actual [0,1], columns predicted [0,1]:")
    print(confusion_matrix(Y_TRUE,Y_PRED,labels=[0,1]))
    print(f"Accuracy: {accuracy_score(Y_TRUE,Y_PRED):.6f}")
    print(f"Precision: {precision_score(Y_TRUE,Y_PRED,zero_division=np.nan):.6f}")
    print(f"Recall: {recall_score(Y_TRUE,Y_PRED,zero_division=np.nan):.6f}")
    print(f"F1: {f1_score(Y_TRUE,Y_PRED,zero_division=np.nan):.6f}")
    print("Never-fraud baseline:",from_counts(0,100,0,9900))
    print(f"Task 2 precision: {80/100:.4%}; recall: {80/90:.4%}")
    print(f"AUC model A: {roc_auc_score(ROC_Y,SCORES_A):.4f}")
    print(f"AUC model B: {roc_auc_score(ROC_Y,SCORES_B):.4f}")
    for threshold in (0.9,0.7,0.5,0.4,0.1):
        print(f"Threshold {threshold:.1f}:",threshold_metrics(threshold))
    if args.plot:
        make_plots(Path(__file__).resolve().with_name("lesson02-evaluation-plots.svg"))


if __name__ == "__main__":
    main()
