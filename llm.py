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
    Sends an expense description to the Gemini API and returns a raw JSON string.

    Constructs a structured prompt from the user input and passes it to the
    Gemini model. Supports English, Hinglish, and Hindi input.

    Args:
        user_input (str): Natural language description of an expense.

    Returns:
        str: Raw JSON string returned by the Gemini API.
    """    

    print("Parsing the text into JSON...\n")

    prompt = f"This is the expense made by the user {user_input} this might be in english, hinglish or hindi, Your job is to understand this expenese from its description and convert it into the JSON format that can be parsed by python easily, the structure for inside the JSON is given below \n\n" + """ 
            {
            "Category": "One of ['Travel', 'Food', 'Academics', 'Miscellaneous', 'Shopping'], if the products are from mixed categories, choose the dominant one!",
            "Amount" : "Return an integer, might be mentioned in the user description, if not mentioned take 0 as default!", 
            "Items": "Return a list of items", 
            "Date & Time" : "Return an empty string",
            "Description" : "Create a 1 liner well documented description from the user description"
        }""" + "Rules: 1. All expenses will be in Rupees, 2. For expenses with no amount, set it amount to 0, 3. Return only JSON object, no markdown, no explanations!"
    
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",  # faster and more accurate than 2.5 
        contents = prompt
    )

    return response.text




def json_to_dict(json_string):
    """
    Converts a JSON string returned by the Gemini API into a Python dictionary.
    Cleans the response, parses it, and attaches the current date and time.

    Args:
        json_string (str): Raw JSON string returned from parse_expense().

    Returns:
        dict: Expense dictionary with keys — Category, Amount, Items, Date & Time, Description.
        None: If JSON parsing fails.

    Raises:
        json.JSONDecodeError: Caught internally, prints error and returns None.
    """

    print("Converting JSON to dictionary...\n")
    
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
    # test_cases = ["maggi and chips for 40 rupees", "auto to college, 50", "netflix 649", "chai and samosa", "आज maggi खाई 30 में"]
    #     
    exp_desc = input("Enter the expense description here: ")
    json_string = parse_expense(exp_desc)   # gemini's JSON response
    exp_report = json_to_dict(json_string)
    print(exp_report)