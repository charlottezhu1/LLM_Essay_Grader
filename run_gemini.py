import base64
import httpx
import json
import pandas as pd
import csv
import os
from docx import Document
from openai import OpenAI
from anthropic import Anthropic 
from settings import *
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
image_path = "https://enpuyfxhpaelfcrutmcy.supabase.co/storage/v1/object/public/grader/Essay%20Rubric.png"
image = httpx.get(image_path)


def gen_gem(prompt):
    response = model.generate_content([{'mime_type':'image/jpeg', 'data': base64.b64encode(image.content).decode('utf-8')}, prompt])
    content = response.text
    print("raw output", content)
    try:
        json_content = json.loads(content)
        print(type(json_content))
        print("json output", json_content)
        return json_content
    except json.JSONDecodeError as decode_error:
        print(f"Error decoding JSON: {decode_error}")
        raise decode_error
    except Exception as e:
        print(f"Error generating completion: {e}")
        raise e

if __name__ == "__main__":
    essays_dir = "./Essays"
    
    header=[
        'id', 'model', 'intro', 'effect', 'negotiation', 'feedback', 'conclusion', 'total', 'comment'
    ]
    
    with open('./gemini_scores.csv', 'w', newline='') as file1:
        writer1 = csv.writer(file1)
        writer1.writerow(header)

        for filename in os.listdir(essays_dir):
            if filename.endswith(".docx"):
                student_index = int(filename.split()[1].split('.')[0])
                
                file_path = os.path.join(essays_dir, filename)
                
                doc = Document(file_path)
                essay = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                
                print(essay)

                prompt = f"""
                You are an experienced teacher in the Human Centered Product Management class. You are tasked to grade your student's essay given the attached rubric.
                Try to be not too kind nor too critical. Remember, "Check Plus" maps to an A+, which is only reserved to a tiny portion of the class. You give Check Plus (full mark) only when the student's essay is beyond expectations.
                Return only the JSON output.
                
                Output your response in JSON format with with keys: 
                “Introduction” (0 to 10),
                “Effective Communication” (0 to 30),
                “Negotiation and Conflict Resolution” (0 to 30),
                "Feedback Insights" (0 to 20),
                "Conclusion and Reflection" (0 to 10)
                "Comment" (Your short comment for this essay. Include reasoning for any deduction; Guide the student to improve on the essay; Be personal, refer to clear details of the student's writing.)
                ""

                Sample JSON output: {{'Introduction': 9, 'Effective Communication': 28, 'Negotiation and Conflict Resolution': 27, 'Feedback Insights': 18, 'Conclusion and Reflection': 8, 'Comment': <your short comment>}}

                Student essay: {essay}
                """
                data = gen_gem(prompt)

                # Ensure total score is correctly calculated
                total_score = sum([
                    data["Introduction"],
                    data["Effective Communication"],
                    data["Negotiation and Conflict Resolution"],
                    data["Feedback Insights"],
                    data["Conclusion and Reflection"]
                ])
                
                # Append the results
                row = [student_index,
                    "claude-3-5-sonnet-20240620",
                    data["Introduction"],
                    data["Effective Communication"],
                    data["Negotiation and Conflict Resolution"],
                    data["Feedback Insights"],
                    data["Conclusion and Reflection"],
                    total_score,
                    data["Comment"]
                ]

                writer1.writerow(row)