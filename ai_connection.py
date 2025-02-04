import os
import httpx
from openai import AzureOpenAI
from dotenv import dotenv_values
##2023-09-01-preview
try:
    # Initialize the Azure OpenAI client
    config = dotenv_values(".env")
    client = AzureOpenAI(
        azure_endpoint = config['azure_endpoint'],
        api_key=config['api_key'],  
        api_version="2024-08-01-preview",
        http_client = httpx.Client(verify=False),
        
    )     

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "What are the different types of road bikes?",
            }
        ],
        model="gpt4o",
        temperature=0.1,
    )

    for choice in chat_completion.choices:
        print(choice.message.content)
    
except Exception as ex:
    print("error")
    print(ex)

