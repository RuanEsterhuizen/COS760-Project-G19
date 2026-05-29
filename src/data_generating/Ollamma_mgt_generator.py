import pandas as pd
from ollama import chat
from tqdm import tqdm
import os

# MODEL = "qwen2.5:7b"
# MODEL = "llama3.1"
MODEL = "mistral:7b"
IN_FILE = "../../data/hgts/hgt_split_3.csv"
OUT_FILE = "../../data/mgts/mistral.csv"

SYSTEM_PROMPT = """
You are a data transformation model for generating machine text

Task:
Convert the given human-generated text into machine-generated text

Rules:
- Preserve meaning
- Preserve isiZulu and style
- Do not add explanations
- Output only the transformed text
- Output must be one line long
"""

df = pd.read_csv(IN_FILE)

if os.path.exists(OUT_FILE):
    done = pd.read_csv(OUT_FILE
)
    done_ids = set(done["id"].astype(str))
else:
    done_ids = set()
    pd.DataFrame(columns=["id", "source", "text", "mgt"]).to_csv(OUT_FILE, index=False)

for _, row in tqdm(df.iterrows(), total=len(df)):

    row_id = str(row["id"])

    if row_id in done_ids:
        continue

    hgt = row["text"]

    try:
        response = chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": hgt}
            ],
            options={
                "temperature": 0 # low temperature to prevent adding extra details
            }
        )

        mgt = response.message.content.strip()

    except Exception as e:
        mgt = f"ERROR: {str(e)}"

    # add entry to file
    out_row = pd.DataFrame([{
        "id": row_id,
        "source": MODEL,
        "text": mgt,
        "mgt": 1 # MGT=true
    }])

    out_row.to_csv(OUT_FILE, mode="a", header=False, index=False)

print(f"Finished generating MGTs using {MODEL}")