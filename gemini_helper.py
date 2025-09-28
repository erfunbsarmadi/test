import os
from google import genai

def compose_email(lastName, abstract):
    
    client = genai.Client()
    prompt = os.getenv("COMPOSITION_PROMPT")
    body = os.getenv("EMAIL_BODY")
    contact = 'Dear Professor ' + lastName + ','
    contents = prompt + '\n' + contact + '\n' + body + '\n' + abstract
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )
    
    return response.text


def suggest_subject(emailBody):
    
    client = genai.Client()
    prompt = os.getenv("SUBJECT_SUGGESTION")
    contents = prompt + '\n' + emailBody
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )
    
    return response.text

def compose_reminder(emailBody):
    
    client = genai.Client()
    prompt = os.getenv("COMPOSE_REMINDER")
    contents = prompt + '\n' + emailBody
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )
    
    return response.text

def clarity_check(text):
    client = genai.Client()
    prompt = os.getenv("CLARITY_PROMPT")
    contents = prompt + '\n' + text
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )
    
    return response.text
