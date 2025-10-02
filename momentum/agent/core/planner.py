# agent/core/planner.py

import google.generativeai as genai
from agent.core import config # Make sure this import is here
from agent.models.schemas import PlanCreate, TaskCreate
import json
import ast

# Configure the Gemini API with our key from our settings file
# We explicitly pass the key to avoid any confusion
try:
    genai.configure(api_key=config.settings.GEMINI_API_KEY)
except Exception as e:
    print(f"Could not configure Gemini API key. Check your .env file. Error: {e}")
    # We can exit here if the key is not set, as the app won't work.
    # Or we can let it fail when it tries to generate a plan.
    # For now, let's print a warning and continue.
    print("Agent will run, but AI generation will fail.")


def generate_plan_with_ai(plan: PlanCreate) -> list[TaskCreate]:
    """
    Uses Google's Gemini to generate a list of tasks for a given plan.
    """
    # Create the prompt for the AI
    prompt = f"""
    You are an expert learning coach. Create a {plan.duration_weeks}-week syllabus for a beginner to learn '{plan.goal}'.
    
    Please structure the output as a JSON list of objects. Each object represents a week and should have the following keys:
    - "week_number": An integer from 1 to {plan.duration_weeks}
    - "title": A clear, concise title for that week's theme.
    - "description": A short description of what will be covered.
    - "topics": A list of 3-4 specific topics or sub-tasks for that week.

    Example format:
    [
        {{"week_number": 1, "title": "Introduction to Python", "description": "Learn the basics.", "topics": ["Variables", "Data Types", "Loops"]}},
        ...
    ]
    
    Do not include any text before or after the JSON list. The entire response must be a valid, parseable JSON list.
    """

    response = None # Initialize response to None
    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Generate the content
        response = model.generate_content(prompt)
        
        # The response text is a string, so we need to parse it into a Python list
        ai_plan_json = ast.literal_eval(response.text)
        
        # Convert the AI's JSON into our Pydantic TaskCreate models
        tasks_to_create = []
        for week_data in ai_plan_json:
            task_title = f"Week {week_data['week_number']}: {week_data['title']}"
            task = TaskCreate(
                week_number=week_data['week_number'],
                title=task_title,
                description=week_data['description'],
                resource_links=[] 
            )
            tasks_to_create.append(task)
            
        return tasks_to_create

    except Exception as e:
        print(f"An error occurred during AI generation: {e}")
        # We only try to print the response text if the response object exists
        if response:
             print(f"AI Response was: {response.text}")
        # Return an empty list if something goes wrong
        return []
