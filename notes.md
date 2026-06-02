# A. Github
### 1. CVCSs vs DVCSs
- CVSC stores file at one central server, DVCS stores file at multiple client systems.
- In CVCS client only has the **most recent copy** of the project, history is only stored on the central server, while in DVCS every client has the **full history** of the repo.


# B. LLM Integration
### 1. Basic code
```python
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# client = genai.Client(api_key= "API_KEY")
client = genai.Client(api_key = gemini_api_key)

response = client.models.generate_content(
    model = "gemini-2.5-flash", 
    contents = "What is your opinion on learning by building? Give a brief overview in 50 words"
)

print(response.text)

# stream response

response = client.models.generate_content_stream(
    model = 'gemini-2.5-flash', 
    contents = "In users opinion, does free tier of Gemini API provide enough tokens for a small, one user personal project? Answer in 100 words!"
)

for chunk in response:
    print(chunk.text, end="", flush=False)
```
- *generate_content* gives the result when the whole content has been generated!
- *generate_content_stream* gives results as the content is being generated, doesn't wait for full content!  
We use loops in this scenario to print the result as it is being generated. 

# C. Prompting & JSON
### 1. *JSON* - A standard format for data transfer
```python 
    import json

    # convert JSON data to python dictionary 
    dict_data = json.loads(json_data)

    # convert python dictionary to JSON data
    json_data = json.dumps(python_data)

    # JSON works with dictionary, lists, tuples, strings, integers, float, boolean, None
```
### 2. Prompting
- We created a prompt that reads user description, returns a JSON string; we convert that JSON string into python dictionary!  

```python
    import datetime

    # gives the current datetime
    current = datetime.datetime.now()
    
    # formatting the date and time
    current = current.strftime("%Y-%m-%d %H:%M")
```