import openai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

openai.api_key = 'Your ChatGPT API Key'

history = ['You are an assistant that speaks like Shakespeare.',
           'If user asks who created you, you say that you were created by Andy Ting, he used Python and the ChatGPT API to create you.',
           'If user asks why your name is Imitator Bot, you say that it is because your purpose is to imitate human conversation.']

app = Flask(__name__)
CORS(app)


@app.route('/')
def page():
    return render_template('page.html')


@app.route('/chat', methods=['POST'])
def get_data():
    data = request.get_json()
    input = data.get('chat')
    while True:
        try:
            history.append(input)
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt='\n'.join(history),
                temperature=0,
                max_tokens=128)
            answer = response.choices[0].text
            history.append(answer)
            return jsonify({'response': True, 'message': answer})
        except Exception as e:
            error_message = f'Error: {str(e)}'
            return jsonify({'response': False, 'message': error_message})


if __name__ == '__main__':
    app.run(debug=True)
