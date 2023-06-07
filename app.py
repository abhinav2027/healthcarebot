from flask import Flask, render_template, request, jsonify
import openai
from gtts import gTTS
from playsound import playsound


app = Flask(__name__)

openai.api_key = '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'  # Replace with your actual API key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    health_condition = request.form.get('health_condition')
    severity = request.form.get('severity')
    voice_en = request.form.get('voice')

    user_message = ""
    if health_condition:
        user_message += f"Health Condition: {health_condition}\n"
    if severity:
        user_message += f"Severity Level: {severity}"
    # print("User msg : ",user_message)
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=user_message,
        max_tokens=100,
        n =1,
        stop = '5',
        temperature=0.2
    )
    # print(response)
    bot_response = response.choices[0].text.strip()
    
    # # Convert the response text to speech using Google Text-to-Speech API
    if(voice_en == 'voice'):
        tts = gTTS(text=bot_response, lang='en')
        tts.save('response.mp3')

        # Play the generated speech
        playsound('response.mp3')

    # speak_text(bot_response)
    return render_template('result.html', response=bot_response)

if __name__ == '__main__':
    app.run()
