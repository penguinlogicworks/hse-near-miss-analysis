import pandas as pd

df = pd.read_csv("near_miss_data.csv")

print("Dataset preview:")
print(df.head())

print("\nTotal near-miss records:")
print(len(df))

print("\nNear misses by hazard category:")
print(df["Hazard_Category"].value_counts())

print("\nAverage severity by hazard category:")
print(
    df.groupby("Hazard_Category")["Severity"]
      .mean()
      .sort_values(ascending=False)
      .round(2)
)

import matplotlib.pyplot as plt

hazard_counts = df["Hazard_Category"].value_counts().sort_values()

plt.figure(figsize=(9, 6))

hazard_counts.plot(kind="barh")

plt.xlabel("Number of Near-Miss Records")
plt.ylabel("Hazard Category")
plt.title("Near-Miss Frequency by Hazard Category")

plt.tight_layout()

plt.savefig(
    "near_miss_by_hazard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

priority = (
    df.groupby("Hazard_Category")
      .agg(
          Frequency=("Hazard_Category", "size"),
          Average_Severity=("Severity", "mean")
      )
)

priority["Priority_Score"] = (
    priority["Frequency"] *
    priority["Average_Severity"]
)

priority = priority.sort_values(
    "Priority_Score",
    ascending=False
).round(2)

print("\nHazard priority summary:")
print(priority)
priority.to_csv("hazard_priority_summary.csv")

priority_plot = (
    priority["Priority_Score"]
    .sort_values()
)

plt.figure(figsize=(9, 6))

priority_plot.plot(kind="barh")

plt.xlabel("Priority Score")
plt.ylabel("Hazard Category")
plt.title("Near-Miss Hazard Priority Screening")

plt.tight_layout()

plt.savefig(
    "hazard_priority_score.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

priority["Priority_Rank"] = (
    priority["Priority_Score"]
    .rank(method="dense", ascending=False)
    .astype(int)
)

priority = priority.sort_values("Priority_Rank")

print("\nHazard priority ranking:")
print(priority)
priority.to_csv("hazard_priority_summary.csv")

top_hazard = priority.index[0]
top_score = priority.iloc[0]["Priority_Score"]

print("\nKey finding:")
print(
    f"{top_hazard} ranked highest in this screening "
    f"with a priority score of {top_score:.2f}."
)