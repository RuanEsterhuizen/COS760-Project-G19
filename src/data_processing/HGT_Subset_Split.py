import pandas as pd
import numpy as np
import os

RANDOM_SEED = 16


df = pd.read_csv("../../data/raw/combinedData.csv")

def get_category(source):
    if source == "AfriHate":
        return "AfriHate"
    elif source == "vukuzenzele":
        return "vukuzenzele"
    else:
        return "isiZuluNews"


df["category"] = df["source"].apply(get_category)

splits = [[], [], []]

for category, group in df.groupby("category"):
    group = group.sample(frac=1, random_state=RANDOM_SEED)

    indices = np.array_split(group.index, 3)

    for i in range(3):
        splits[i].append(group.loc[indices[i]])

final_splits = [
    pd.concat(split_parts, ignore_index=True)
    for split_parts in splits
]

for i in range(3):
    final_splits[i] = (
        final_splits[i]
        .sample(frac=1, random_state=RANDOM_SEED)
        .reset_index(drop=True)
    )

for i, split_df in enumerate(final_splits, start=1):
    print(f"\nSplit {i}")

    counts = (
        split_df["category"]
        .value_counts()
        .reindex(
            ["AfriHate", "vukuzenzele", "isiZuluNews"],
            fill_value=0
        )
    )

    print(counts)
    print(f"Total samples: {len(split_df)}")

os.makedirs("../../data/hgts", exist_ok=True)

for i, split_df in enumerate(final_splits, start=1):
    split_df = split_df.drop(columns=["category"])

    filename = f"../../data/hgts/hgt_split_{i}.csv"
    split_df.to_csv(filename, index=False)

    print(f"Saved {filename}")