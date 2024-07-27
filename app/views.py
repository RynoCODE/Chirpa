from django.shortcuts import render, HttpResponse
from langchain_openai import ChatOpenAI 
from .info import groq_api_key , personal_prompt
from .models import Question
from django.http import HttpResponseBadRequest
from groq import Groq
import re



# llama3 = ChatOpenAI(
#     api_key=groq_api_key,
#     base_url="https://api.groq.com/openai/v1",
#     model="llama3-8b-8192",
# )

def extract_questions_and_answers(text):
    pattern = re.compile(r'\*Question \d+:.*?\*\*.*?\*\*Answer:.*?[^*]', re.DOTALL)
    matches = pattern.findall(text)
    
    clean_matches = []
    for match in matches:
        cleaned = match.strip()
        if cleaned:
            clean_matches.append(cleaned)
    
    return clean_matches

def dashboard(request):
    return render(request, 'dashboard.html')


client = Groq(
    api_key=groq_api_key
)
def question_maker(request):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{personal_prompt} : python"
            }
        ],
        model="llama3-8b-8192"
    )

    response_content = chat_completion.choices[0].message.content
    questions_list = extract_questions_and_answers(response_content)
    formatted_questions = [{'text': q} for q in questions_list]
    print(response_content)
    return render(request, 'question_list.html', {'questions': formatted_questions})
    

def index(request):
    return render(request, 'index.html')
def notepad(request):
    return render(request, 'notepad.html')

