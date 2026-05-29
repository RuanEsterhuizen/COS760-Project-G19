import glob
import pandas as pd
import os

folder_path = '../../data/temp'
all_files = glob.glob(os.path.join(folder_path, '*.csv'))

df_list = []

for file in all_files:
    df = pd.read_csv(file)

    # ensure "MGT" and "mgt" are treated the same
    df.columns = df.columns.str.lower()
    if 'mgt' in df.columns:
        df['mgt'] = df['mgt'].astype(bool)

    df_list.append(df)

combined_df = pd.concat(df_list, ignore_index=True)

combined_df = combined_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

combined_df.to_csv('dataset.csv', index=False)