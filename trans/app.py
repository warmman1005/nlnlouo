from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data['text']
    target_language = data['targetLanguage']
    api_key = os.getenv('OPENAI_API_KEY')

    system_message = "You are a helpful assistant."
    if target_language == 'zh-TW':
        system_message = "Please translate the text to Traditional Chinese (繁體中文)."
    elif target_language == 'en':
        system_message = "Please translate the text to English."
    elif target_language == 'ja':
        system_message = "Please translate the text to Japanese."
    elif target_language == 'es':
        system_message = "Please translate the text to Spanish."

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    body = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=body)
    result = response.json()

    if 'error' in result:
        return jsonify({'error': result['error']['message']}), 500
    else:
        return jsonify({'translatedText': result['choices'][0]['message']['content'].strip()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
