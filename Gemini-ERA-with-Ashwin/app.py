
from flask import Flask, render_template, request, jsonify, session
import os
import google.generativeai as genai
from dotenv import load_dotenv
import traceback
# For loading your gemini use load_dotenv 
# make a file .env 
# and add your gemini api in .env file and load the file with dotenv
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("Enter your gemini-api")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(question):
    try:
        model = genai.GenerativeModel('enter-your-gemini-model-name')
        response = model.generate_content(question)
        if response.text:
            return response.text
        else:
            return "I apologize, but I couldn't generate a response. Please try again."
    except Exception as e:
        print(f"Error in get_gemini_response: {str(e)}")
        print(traceback.format_exc())
        return "I apologize, but there was an error processing your request. Please try again."

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    if request.method == 'POST':
        try:
            question = request.form.get('question', '').strip()
            if not question:
                return jsonify({
                    'error': 'Please enter a question'
                }), 400

            response = get_gemini_response(question)
            
            # Add the conversation to chat history
            session['chat_history'].append({
                'question': question,
                'response': response
            })
            
            return jsonify({
                'question': question,
                'response': response
            })
        except Exception as e:
            print(f"Error in index route: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'error': 'An error occurred while processing your request'
            }), 500
    
    return render_template('index.html', chat_history=session['chat_history'])

@app.route('/new-chat', methods=['POST'])
def new_chat():
    try:
        session['chat_history'] = []
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error in new_chat route: {str(e)}")
        return jsonify({
            'error': 'An error occurred while clearing chat history'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)