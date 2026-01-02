import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    # Agar .env nahi chala toh yahan direct key daal sakte hain
    api_key = "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"

client = Groq(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/humanize', methods=['POST'])
def humanize_text():
    data = request.json
    input_text = data.get('text')
    if not input_text:
        return jsonify({'error': 'Text is empty'}), 400

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Rewrite the following text to make it sound 100% human, natural, and conversational. Remove any AI-like patterns."},
                {"role": "user", "content": input_text}
            ],
            temperature=0.7,
        )
        return jsonify({'humanized_text': completion.choices[0].message.content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)