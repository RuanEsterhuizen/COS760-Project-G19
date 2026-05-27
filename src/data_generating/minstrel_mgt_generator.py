# Retired
import pandas as pd
from minstrel import Minstrel

import os
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("MINSTREL_API_KEY")

csv_file_path = "../../data/hgts/hgt_split_2.csv"