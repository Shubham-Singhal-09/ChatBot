import os 
import logging
import sys

# Setup OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = "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"

# Setup logging

log = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)

# Update sys.path (or use PYTHONPATH)

sys.path.insert(0, '..')


def read_feedback():
    import pandas as pd

    df = pd.read_csv("./feedbacks.csv").dropna()

    df.head()
    
def filter_and_sampling():
    # Filter feedbacks text below 300 characters
    df = df[df.text.str.len() < 300].reset_index(drop=True)

    # Sample n feedbacks
    df = df.sample(n=15).reset_index()

    df.head()
    
def analysis(text):
    from random import choice
    from tqdm.notebook import tqdm
    from gpt3 import analyze
    from json import loads
    from pprint import pprint
    from textwrap import dedent

    analysis_results = []
    extra_prompts = []

    logging.getLogger("openai").setLevel(logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

    # for i in tqdm(range(len(text)), desc="Analyzing reviews"):
        # title = df.loc[i, "title"]
        # text = df.loc[i, "text"]

        # log.info(f"Analyzing feedback - \nTitle: {title}\nText: {text}\n")

    extra_prompt = choice(extra_prompts) if extra_prompts else ""

    res = analyze(
        text=text,
        extra_prompt="",
        max_tokens=1024,
        temperature=0.1,
        top_p=1,
    )
    
    

    raw_json = res["choices"][0]["text"].strip()

    try:
        json_data = loads(raw_json)
        analysis_results.append(json_data)

        log.debug(f"JSON response: {pprint(json_data)}")

        extra_prompts.append(f"\n{text}\n{raw_json}")
        return raw_json
       
    except Exception as e:
        log.error(f"Failed to parse '{raw_json}' -> {e}")
        analysis_results.append([])
        

    # df["analysis"] = analysis_results
    # df.to_csv("./feedbacks_analysis.csv", index=False)
    
    

    
        

