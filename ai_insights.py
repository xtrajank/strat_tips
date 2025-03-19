# business insights processing with chatGPT
import openai
from config import Config

openai.api_key = Config.openai_key

def generate_insight(financial_data):
    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": 
                   f'Analyze this financial data and suggests improvements: {financial_data}. I need raw reports and immediate expert-backed actions to improve their business today. TASK: Deliver 4 AI driven Profitability insights. Your response must include: 1. Prioritize list of top 4 revenue boosting or cost saving opportunities. 2. each insight must include an estimated financial report. 3. ai must site real benchmarks from business studies, financial reports, or similar industry cases. 4. for each insight include 3-step simple "Do This Now" guide for execution. 5. rate the implemenation effort. (Easy, Medium, Hard)'}])
    
    return response["choices"][0]["message"]["content"]