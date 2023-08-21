
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

class ChatGPTBotAPI:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        openai.api_key = self.openai_api_key
        self.prompts = []

    def create_prompt(self, prompt):
        self.prompts.append(prompt)
        return len(self.prompts) - 1

    def get_response(self, prompt_index):
        prompt = self.prompts[prompt_index]
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=50
        )
        return response.choices[0].text.strip()

    def update_prompt(self, prompt_index, new_prompt):
        self.prompts[prompt_index] = new_prompt

chatbot = ChatGPTBotAPI("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")

@app.route('/create_prompt', methods=['POST'])
def create_prompt():
    data = request.get_json()
    prompt = data['prompt']
    prompt_index = chatbot.create_prompt(prompt)
    return jsonify({"prompt_index": prompt_index})

@app.route('/get_response/<int:prompt_index>', methods=['GET'])
def get_response(prompt_index):
    response = chatbot.get_response(prompt_index)
    return jsonify({"response": response})

@app.route('/update_prompt/<int:prompt_index>', methods=['PUT'])
def update_prompt(prompt_index):
    data = request.get_json()
    new_prompt = data['new_prompt']
    chatbot.update_prompt(prompt_index, new_prompt)
    return jsonify({"message": "Prompt updated successfully"})

if __name__ == '__main__':
    app.run(debug=True)
