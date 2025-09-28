from google import genai

client = genai.Client()

def compose_email(lastName, abstract):

    
    contact = 'Dear Professor' + lastName

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain how AI works in a few words"
    )
    
    print(response.text)
