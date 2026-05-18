import pandas as pd
import os
from huggingface_hub import login
from datasets import load_dataset # Needs to be installed: pip install datasets

'''
Note: 
- This code needs to be run in the Project Root Directory in order for file paths to work correctly
'''



data_split = ("train", "test", "validation")

dir_path = "data/raw/"
os.makedirs(dir_path, exist_ok=True)

# Get your API Token from your Hugging Face Account
hf_token = ""

# Read Token From Hugging Face
login(token=hf_token)

for split in data_split:
    dataset = load_dataset("afrihate/afrihate", name="zul", split=split)
    df = dataset.filter(lambda label: label['label'] == "Normal")
    
    # Add Source Columns
    source_data = ["AfriHate"] * len(df)
    df = df.add_column("source", source_data)

    # Add MGT Column
    mgt_data = [True] * len(df)
    df = df.add_column("MGT", mgt_data)

    # Remove and Rename Columns
    df = df.remove_columns(["label", 'length'])
    df = df.rename_column('tweet', 'text')


    # Storing Process
    column_order = ['id', 'source', 'text', 'MGT']

    pandas_df = df.to_pandas()
    pandas_df = pandas_df[column_order]
    pandas_df.to_csv(f"{dir_path}afrihate_{split}.csv", index=False)
