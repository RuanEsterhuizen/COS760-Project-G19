import glob
import pandas as pd
import os

folder_path = ''
all_files = glob.glob(os.path.join(folder_path, '*.csv'))

df_list = []
for file in all_files:
    df = pd.read_csv(file)
    df_list.append(df)
combined_df = pd.concat(df_list, ignore_index=True)
combined_df.to_csv('combinedData.csv', index=False)
