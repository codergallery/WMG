from dotenv import load_dotenv
import os
from google import genai
import datetime
import json

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# client = genai.Client(api_key= "API_KEY")
client = genai.Client(api_key = gemini_api_key)





def parse_expense(user_input):
    """
    Passes the user input to gemini, and returns the response (JSON)
    """    

    prompt = f"This is the expenese made by the user {user_input} this might be in english, hinglish or hindi, Your job is to understand this expenese from its description and convert it into the JSON format that can be parsed by python easliy, the structure for inside the JSON is given below \n\n" + """ 
            {
            "Category": "One of ['Travel', 'Food', 'Academics', 'Miscellaneous', 'Shopping'], if the products are from mixed categories, choose the dominant one!",
            "Amount" : "Return an integer, might be mentioned in the user description, if not mentioned take 0 as default!", 
            "Items": "Return a list of items", 
            "Date & Time" : "Return an empty string",
            "Description" : "Create a 1 liner well documented description from the user description"
        }""" + "Rules: 1. All expenses will be in Rupees, 2. For expenses with no amount, set it amount to 0, 3. Return only JSON object, no markdown, no explanations!"
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",  # using gemini-3.1-flash-lite model, worked faster than 2.5 
        contents = prompt
    )

    return response.text




def json_to_dict(json_string):
    """
    Safely converts Gemini's JSON response into Python Dictionary
    """

    # remove the unwanted characters from gemini's response
    try: 
        json_response = (json_string.replace("```json", "").replace("```", "").strip())
        exp_dict = json.loads(json_response)    # convert returned json to python dict
    except json.JSONDecodeError:
        print("Could not parse expense, please try again!")
        return 

    # include the current date and time
    try:
        current_time = datetime.datetime.now()
        exp_dict["Date & Time"] = str(current_time.strftime("%Y-%m-%d %H:%M"))
    except Exception as e:
        print(f"Unable to change dates! Please do it manually! \nError: {e}")
        
    return exp_dict



if __name__== "__main__":
    test_cases = ["maggi and chips for 40 rupees", "auto to college, 50", "netflix 649", "chai and samosa", "आज maggi खाई 30 में"]
    for test in test_cases:
        # exp_desc = input("Enter the expense description here: ")
        json_string = parse_expense(test)   # gemini's JSON response
        exp_report = json_to_dict(json_string)
        print(exp_report)