import os
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import markdown

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

TRACK_OPTIONS = [
    "AI Track",
    "Education Track",
    "Social Good & Human Experience Track",
    "Health Track",
    "Environmental/Sustainability Track"
]

PRIZE_CATEGORIES = [
    "Best Use of Auth0",
    "Best AI Application Built with Cloudflare",
    "Best Use of Terraform",
    "Best Domain Name from GoDaddy Registry",
    "Best Use of Gen AI"
]

@app.route("/")
def index():
    return render_template('index.html', tracks=TRACK_OPTIONS, prizes=PRIZE_CATEGORIES)

@app.route("/generate_idea", methods=['POST'])
def generate_idea():
    track = request.form['track']
    prizes = request.form.getlist('prizes')
    prompt = f"Generate a project idea for SwampHacks under the {track}. " \
             f"Consider these prize categories: {', '.join(prizes)}. " \
             f"Focus on retro technology theme and learning/exploration."
    response = model.generate_content(prompt)
    markdown_text = response.text
    html_content = markdown.markdown(markdown_text)
    return html_content

@app.route("/chat", methods=['POST'])
def chat():
    user_message = request.form['message']
    response = model.generate_content(f"User: {user_message}")
    markdown_text = response.text
    html_content = markdown.markdown(markdown_text)
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
