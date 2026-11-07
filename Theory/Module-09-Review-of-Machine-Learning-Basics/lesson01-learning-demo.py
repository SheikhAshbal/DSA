"""Small fixed fixtures showing supervised fitting and unlabelled clustering."""
import argparse
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from threadpoolctl import threadpool_limits

TREE_X = np.array([[1,50],[2,60],[8,90],[7,85],[1,40],[9,95],[3,55],[6,80]],dtype=float)
TREE_Y = np.array([0,0,1,1,0,1,0,1])
CUSTOMERS = np.array([[2,1],[3,2],[1,1],[30,15],[28,14],[32,16],[15,7],[16,8]],dtype=float)
HOURS = np.arange(1,9,dtype=float).reshape(-1,1)
SCORES = np.array([52,58,63,71,74,80,85,88],dtype=float)


def fit_examples():
    # Avoid thread-startup overhead for the tiny teaching fixtures.
    with threadpool_limits(limits=1):
        tree = DecisionTreeClassifier(max_depth=2,random_state=0).fit(TREE_X,TREE_Y)
        km = KMeans(n_clusters=3,n_init=10,random_state=0).fit(CUSTOMERS)
        regression = LinearRegression().fit(HOURS,SCORES)
    return tree,km,regression


def ordered_centres(km):
    """Sort only for readable reporting; do not assign business meaning to IDs."""
    return km.cluster_centers_[np.argsort(km.cluster_centers_[:,0])]


def make_plots(output,models=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from sklearn.tree import plot_tree

    tree,km,regression = fit_examples() if models is None else models
    plt.rcParams.update({"svg.fonttype":"none","font.size":10})
    fig,axes = plt.subplots(1,3,figsize=(14,5),layout="constrained")
    fig.suptitle("Three foundational algorithms on tiny teaching fixtures",fontsize=16)
    plot_tree(tree,feature_names=["hours","attendance"],
              class_names=["not passed","passed"],filled=True,
              impurity=False,rounded=True,fontsize=9,ax=axes[0])
    axes[0].set_title("Decision tree: labels guide the split")

    ax = axes[1]
    colours = ["#2166ac","#c85b16","#459545"]
    for display_id,raw_id in enumerate(np.argsort(km.cluster_centers_[:,0]),1):
        group = CUSTOMERS[km.labels_ == raw_id]
        ax.scatter(group[:,0],group[:,1],s=55,color=colours[display_id-1],
                   label=f"Group {display_id} (display order)")
    ax.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],
               marker="X",color="#111111",s=100,label="Centres")
    ax.set(title="k-means: raw, unscaled features",xlabel="Annual spend (thousands)",ylabel="Visits per month")
    ax.legend(frameon=False,fontsize=8)

    ax = axes[2]
    ax.scatter(HOURS[:,0],SCORES,color="#2166ac",label="Observed scores")
    ax.plot(HOURS[:,0],regression.predict(HOURS),color="#c85b16",label="Fitted line")
    ax.set(title="Linear regression: predict a number",xlabel="Study hours",ylabel="Score")
    ax.text(0.03,0.95,"Fitted score = 5.25 x hours + 47.75",
            transform=ax.transAxes,va="top",fontsize=9)
    ax.legend(frameon=False,fontsize=8,loc="lower right")
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,format="svg")
    fig.savefig(output.with_suffix(".png"),dpi=120)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot",action="store_true",help="Requires Matplotlib")
    args = parser.parse_args()
    models = fit_examples()
    tree,km,regression = models
    rules = export_text(tree,feature_names=["hours","attendance"])
    print("Learned decision-tree rules:")
    print(rules)
    print("Prediction for [5 hours,75% attendance]:",int(tree.predict([[5,75]])[0]))
    print("Raw cluster IDs:",km.labels_.tolist())
    print("Centres sorted by annual spend:",ordered_centres(km).round(3).tolist())
    print(f"Linear fit: score = {regression.coef_[0]:.2f} * hours + {regression.intercept_:.2f}")
    print("These are training demonstrations, not held-out performance estimates.")
    if args.plot:
        make_plots(Path(__file__).resolve().with_name("lesson01-algorithm-examples.svg"),models)


if __name__ == "__main__":
    main()
