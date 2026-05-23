from groq import Groq
import os 
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
apiKey = os.getenv("GROQ_API_KEY")

groq_client = Groq(api_key=apiKey)

csv_file_path = "../../data/hgts/hgt_split_2.csv"