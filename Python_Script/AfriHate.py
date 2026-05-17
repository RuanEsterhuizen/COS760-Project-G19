import pandas as pd
import os
from huggingface_hub import login
from datasets import load_dataset # Needs to be installed: pip install datasets

data_split = ("train", "test", "validation")

dir_path = "AfriHate/"
os.makedirs(dir_path, exist_ok=True)

# Get your API Token from your Hugging Face Account
hf_token = ""

# Read Token From Hugging Face
login(token=hf_token)

urls = ["afrihate/afrihate/parquet/zul/train"]


for split in data_split:
    dataset = load_dataset("afrihate/afrihate", name="zul", split=split)
    df = dataset.filter(lambda label: label['label'] == "Normal")
    df.to_json(f"{dir_path}afrihate_{split}.jsonl", orient="records", lines=True)