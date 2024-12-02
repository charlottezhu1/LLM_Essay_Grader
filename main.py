import base64
import httpx
import os
from docx import Document
from openai import OpenAI
from anthropic import Anthropic 
from settings import *
from claude import *
oai = OpenAI(api_key = OPENAI_API_KEY)
ant = Anthropic()
ant.api_key = ANTHROPIC_API_KEY

rubric_url = "https://enpuyfxhpaelfcrutmcy.supabase.co/storage/v1/object/public/grader/Essay%20Rubric.png"
rubric_media_type = "image/png"
rubric_data = base64.standard_b64encode(httpx.get(rubric_url).content).decode("utf-8")

def run_claude():

def run_gemini():


if __name__ == "__main__":
    essays_dir = "./Essays"

    for filename in os.listdir(essays_dir):
        if filename.endswith(".docx"):
            student_index = int(filename.split()[1].split('.')[0])
            
            file_path = os.path.join(essays_dir, filename)
            
            # extract the text
            doc = Document(file_path)
            essay = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            print(essay)

            prompt = f"""
            You are an experienced teacher in the Human Centered Product Management class. You are tasked to grade your student's essay given the attached rubric.
            Try to be not too kind nor too critical. Remember, "Check Plus" maps to an A+, which is only reserved to a tiny portion of the class. You give Check Plus (full mark) only when the student's essay is beyond expectations.
            Give a score for each section, and a total score for this student. Pay close attention to the details given in the rubric.
            
            Output your response in JSON format with with keys: 
             “Introduction” (0 to 10),
             “Effective Communication” (0 to 30),
             “Negotiation and Conflict Resolution” (0 to 30),
             "Feedback Insights" (0 to 20),
             "Conclusion and Reflection" (0 to 10)
             "Total Score" (Introduction + Effective Communication + Negotiation and Conflict Resolution + Feedback Insights + Conclusion and Reflection; the sum of all sections above; 0 to 100)
             ""

            Example output:
            {{
                "Introduction": 8,
                "Effective Communication": 25,
                "Negotiation and Conflict Resolution": 28,
                "Feedback Insights": 18,
                "Conclusion and Reflection": 9,
                "Total Score": 88
            }}

            Student essay: {essay}
            """
            simple_gen_ant(prompt)
            break
