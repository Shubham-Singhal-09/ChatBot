from flask import Flask, render_template, request
import openai
import os
from textwrap import dedent
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

    return raw_json

    try:
        json_data = loads(raw_json)
        analysis_results.append(json_data)

        log.debug(f"JSON response: {pprint(json_data)}")

        extra_prompts.append(f"\n{text}\n{raw_json}")
    except Exception as e:
        log.error(f"Failed to parse '{raw_json}' -> {e}")
        analysis_results.append([])
        

    # df["analysis"] = analysis_results
    # df.to_csv("./feedbacks_analysis.csv", index=False)
    

openai.api_key = os.getenv("OPENAI_API_KEY")

ABSA_PROMPT = dedent(
    f"""
    Please extract aspect expressions, related segments and related sentiments from the following text and format output in JSON:

    This product is good but the battery doesn't last. It's lightweight and very easy to use. Well worth the money.

    [
      {{ "aspect": "Overall satisfaction", "segment": "This product is good", "sentiment": "positive" }},
      {{ "aspect": "Battery", "segment": "the battery doesn't last", "sentiment": "negative" }},
      {{ "aspect": "Weight", "segment": "It's lightweight", "sentiment": "positive" }},
      {{ "aspect": "Usability", "segment": "very easy to use", "sentiment": "positive" }},
      {{ "aspect": "Value for money", "segment": "Well worth the money", "sentiment": "positive" }}
    ]

    I don't like this product, it's very noisy. Anyway, it's very cheap. The other one I had was better.

    [
      {{ "aspect": "Overall satisfaction", "segment": "I don't like this product", "sentiment": "negative" }},
      {{ "aspect": "Noise", "segment": "it's very noisy", "sentiment": "negative" }},
      {{ "aspect": "Price", "segment": "it's very cheap", "sentiment": "positive" }},
      {{ "aspect": "Comparison", "segment": "The other one I had was better.", "sentiment": "negative" }}
    ]
"""
)


def analyze(
    text,
    prompt_text=ABSA_PROMPT,
    extra_prompt="",
    temperature=0.5,
    max_tokens=128,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
):
    prompt = f"{prompt_text}\n{extra_prompt}\n{text}"

    return openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

app = Flask(__name__)

model_engine = "text-davinci-003"
openai.api_key = "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"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    analysis_results = analysis(userText)
    print( f"{userText} {analysis_results}")
    return f"{userText} {analysis_results}"


if __name__ == "__main__":
    app.run()