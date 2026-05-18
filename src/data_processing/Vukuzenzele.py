# This script was used to process data from the vukuzenzele dataset (monolingual)
# Vukuzenzele Dataset: https://github.com/dsfsi/vukuzenzele-nlp

# Citation (Remember for report writing)
# @dataset{marivate_vukosi_2023_7598540,
#   author       = {Marivate, Vukosi and
#                   Njini, Daniel and
#                   Madodonga, Andani and
#                   Lastrucci, Richard and
#                   Dzingirai, Isheanesu and
#                   Rajab, Jenalea},
#   title        = {The Vuk'uzenzele South African Multilingual Corpus},
#   month        = feb,
#   year         = 2023,
#   publisher    = {Zenodo},
#   doi          = {10.5281/zenodo.7598539},
#   url          = {https://doi.org/10.5281/zenodo.7598539}
# }

import csv
import sys

from datasets import load_dataset
import pandas as pd
import re

def split_paragraphs(text: str) -> list[str]:
    paragraphs = text.split("\n")

    cleaned = []

    for p in paragraphs:
        p = p.replace("\t", " ")

        # remove bullets
        p = re.sub(r'[■•●"]', "", p)

        # normalize whitespace
        p = re.sub(r"\s+", " ", p).strip()

        # skip empty lines
        if not p:
            continue

        # remove separator lines
        if re.fullmatch(r"[-=]{5,}", p):
            continue

        # split large paragraphs into chunks
        chunks = []

        if len(p) > 256:
            words = p.split()
            chunk = ""

            for w in words:
                if len(chunk) + len(w) + 1 <= 256:
                    chunk += " " + w
                else:
                    chunks.append(chunk.strip())
                    chunk = w

            if chunk:
                chunks.append(chunk.strip())
        else:
            chunks.append(p)

        # remove chunks shorter than 50 characters
        for c in chunks:
            if len(c) < 50:
                continue

            cleaned.append(c)

    return cleaned


dataset = load_dataset("dsfsi/vukuzenzele-monolingual", "zul")

rows = []
global_id = 1

for split in dataset.keys():

    for article in dataset[split]:
        paragraph = article["text"]

        paragraphs = split_paragraphs(paragraph)

        for paragraph in paragraphs:
            rows.append({
                "id": global_id,
                "source":"vukuzenzele"
                "text": paragraph,
                "MGT": 0
            })
            global_id += 1


df = pd.DataFrame(rows)

if not rows:
    print("An error occurred when processing the dataset")
    sys.exit()

print("Vuk'uzenzele HGT Sample: \n", rows[0])

df.to_csv("../../data/raw/vukuzenzele_hgt.csv", index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)

print("Human Generated Texts from Vuk'uzenzele dataset saved to '~/data/raw/vukuzenzele_hgt.csv'")
