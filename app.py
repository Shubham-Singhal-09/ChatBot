from flask import Flask, render_template, request
from absa import analysis
import openai
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