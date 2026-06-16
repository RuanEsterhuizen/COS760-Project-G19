#Retired

#To run make sure to install the Groq Python SDK, which can be done using pip:
#pip install groq
from groq import Groq

import os 
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
apiKey = os.getenv("GROQ_API_KEY")

#Might need to change how API key is handled for each LLM API used. The following is for Groq.
groq_client = Groq(api_key=apiKey)

#Make sure to set this value to the name of the LLM you are using, this will be used in the output csv file to identify which LLM generated which text.
LLM_used = "Groq"
model_used = "llama-3.3-70b-versatile"

starting_prompt = "For each provided prompt after, output a similiar text that is written in your own words and in the same language."
#confirmation = groq_client.generate(starting_prompt)
#print(confirmation)

csv_file_path = "../../data/hgts/hgt_split_2.csv"
dfInput = pd.read_csv(csv_file_path)

inputs = dfInput["text"].tolist()
#inputs.insert(0, starting_prompt)

ids = dfInput["id"].tolist()
output_texts = []

"""for input in inputs:
    print(f"Input: {input}\n")
    response = groq_client.generate(input)
    output_texts.append(response)
    print(f"Output: {response}\n")"""

while True:
    input = inputs.pop(0)
    print(f"Input: {input}\n")
    if len(inputs) == 0:
        break

    outputs = groq_client.chat.completions.create(
        model = model_used,
        messages = [
            {"role": "system", "content": starting_prompt},
            {"role": "user", "content": input}
        ]
    )
    output_texts.append(outputs.choices[0].message.content)
    print(f"Output: {outputs.choices[0].message.content}\n")

dfOutput = pd.DataFrame({"id": ids, "source": LLM_used, "text": output_texts, "MGT": 1})
output_csv_path = "../../data/mgts/groq_mgt.csv"
dfOutput.to_csv(output_csv_path, index=False) 