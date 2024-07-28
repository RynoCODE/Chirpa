from django.shortcuts import render, HttpResponse, get_object_or_404
from .info import groq_api_key
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from groq import Groq
import re
from . models import Question
from .email_validator import is_valid_email
import pyotp
from .models import UserProfile
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


personal_prompt="give 1 question based on the language to judge the proficiency of the user in the language ,some topics to be asked compulsorly is oops, dsa , api fetch and decode and many more important topics  no answer required strictly in this format. Strictly use maximum 50 words only for question"


# llama3 = ChatOpenAI(
#     api_key=groq_api_key
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
questions =[]


# @login_required
def question_maker(request):
    if request.method == 'GET':
        user_query = request.GET.get('query', '')

    generated_questions = []
    for i in range(5):
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
        questions.append(response_content)
        question = Question(
            user = request.user,
            text = response_content
        )
        question.save()
        generated_questions.append(question)

    print(generated_questions)
    # questions_list = extract_questions_and_answers(response_content)
    # formatted_questions = [{'text': q} for q in questions_list]
    print(questions)
    return render(request, 'question_list.html', {'questions': generated_questions})

# @login_required
# def question_maker(request):
#     if request.method == 'GET':
#         user_query = request.GET.get('query', '')

#     generated_questions = []
#     for i in range(5):
#         try:
#             chat_completion = client.chat.completions.create(
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": f"{personal_prompt} : python"
#                     }
#                 ],
#                 model="llama3-8b-8192"
#             )
            
#             response_content = chat_completion.choices[0].message.content
#             generated_questions.append(response_content)
            
#             # Ensure request.user is not an AnonymousUser
#             if request.user.is_authenticated:
#                 question = Question(
#                     user=request.user,
#                     text=response_content
#                 )
#                 question.save()
#             else:
#                 print("User is not authenticated")
                
#         except Exception as e:
#             print(f"Error generating or saving question: {e}")

#     print(generated_questions)
#     return render(request, 'question_list.html', {'questions': generated_questions})
    

def index(request):
    return render(request, 'index.html')

def notepad(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    return render(request, 'notepad.html', {'question': question.text})






# Handeling Text Area form
from .forms import TextAreaForm

def process_textarea(request):
    if request.method == 'POST':
        form = TextAreaForm(request.POST)
        if form.is_valid():
            text_data = form.cleaned_data['text_data']
            print(text_data)
            # Process the text data as needed
            return HttpResponse(f'Text received: {text_data}')
            
    
    else:
        form = TextAreaForm()
        
    return render(request, 'your_template.html', {'form': form, 'question': 'Your question here'})


