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
    contents = os.getenv("SUBJECT_SUGGESTION") + '\n' + emailBody
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )
    
    return response.text
