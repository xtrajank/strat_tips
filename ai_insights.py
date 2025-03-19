# business insights processing with chatGPT
import openai
from config import Config

openai.api_key = Config.openai_key

def generate_insight(financial_data):
    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": 
                   f'Analyze this financial data and suggests improvements: {financial_data}'}])
    
    return response["choices"][0]["message"]["content"]