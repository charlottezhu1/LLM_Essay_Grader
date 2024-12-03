import argparse
import time
from run_claude import *
from run_openai import *
from run_gemini import *
essays_dir = "./Essays"

def run_llm_grade_essay(company, model, prompt, temperature):
    if company == "openai":
        data = simple_gen_oai(prompt, model, temperature) # default 'gpt-4o'
    elif company == "claude":
        data = simple_gen_ant(prompt, model) # default 'claude-3-5-sonnet-20240620'
    elif company == "gemini":
        data = simple_gen_gem(prompt, model)
    else: 
        raise ValueError(f"Company '{company}' is not supported. Please choose from 'openai', 'claude', or 'gemini'.")
    
    return data # JSON DATA


if __name__ == "__main__":
    # parse the argument
    parser = argparse.ArgumentParser(description="Batch run the essay grading.")
    parser.add_argument("--company", type=str, default="gemini", help="Model company to grade the essays (optional).")
    parser.add_argument("--model", type=str, default="gemini-1.5-flash", help="Specific model to grade the essays (optional).")
    parser.add_argument("--temperature", type=float, default=1.0, help="Model temperature to grade the essays (optional).")
    parser.add_argument("--prompt", type=int, default=1, help="Prompt to grade the essays (optional).")
    args = parser.parse_args()
    
    company = args.company
    model = args.model
    temperature = args.temperature
    prompt = args.prompt

    header=['id', 'company', 'model', 'temperature', 'prompt', 'intro', 'effect', 'negotiation', 'feedback', 'conclusion', 'total', 'comment']
    with open(f'csv_outputs/essay_scores.csv', 'a', newline='') as file1:
        writer1 = csv.writer(file1)
        # writer1.writerow(header)

        for filename in os.listdir(essays_dir):
            if filename.endswith(".docx"):
                # get current index
                student_index = int(filename.split()[1].split('.')[0])

                # get essay
                file_path = os.path.join(essays_dir, filename)
                doc = Document(file_path)
                essay = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                print(essay)

                if prompt == 1:
                    grade_prompt = f"""
                        You are an experienced teacher in the Human Centered Product Management class. You are tasked to grade your student's essay given the attached rubric.
                        Try to be not too kind nor too critical. Remember, "Check Plus" maps to an A+, which is only reserved to a tiny portion of the class. You give Check Plus (full mark) only when the student's essay is beyond expectations.
                        Return only the JSON output.
                        
                        Output your response in JSON format with with keys: 
                        “Introduction” (0 to 10),
                        “Effective Communication” (0 to 30),
                        “Negotiation and Conflict Resolution” (0 to 30),
                        "Feedback Insights" (0 to 20),
                        "Conclusion and Reflection" (0 to 10)
                        "Comment" (Your short comment for this essay. Include reasoning for any deduction; Guide the student to improve on the essay; Be personal, refer to clear details of the student's writing. Do not include any quotation mark in the comment.)
                        ""
                        For example, {{"Introduction": 8, "Effective Communication": 26, "Negotiation and Conflict Resolution": 30, "Feedback Insights": 15, "Conclusion and Reflection": 10, "Comment": <your short comment>}}
                        Student essay: {essay}

                        Use this JSON schema:

                        Score = {{"Introduction": int, "Effective Communication": int, "Negotiation and Conflict Resolution": int, "Feedback Insights": int, "Conclusion and Reflection": int, "Comment":str}}
                        Return: Score
                    """
                # get llm response
                data = run_llm_grade_essay(company, model, grade_prompt, temperature) # output JSON

                # store data
                total_score = sum([
                    int(data["Introduction"]),
                    int(data["Effective Communication"]),
                    int(data["Negotiation and Conflict Resolution"]),
                    int(data["Feedback Insights"]),
                    int(data["Conclusion and Reflection"])
                ])
                
                row = [student_index,
                    company,
                    model,
                    temperature,
                    prompt,
                    data["Introduction"],
                    data["Effective Communication"],
                    data["Negotiation and Conflict Resolution"],
                    data["Feedback Insights"],
                    data["Conclusion and Reflection"],
                    total_score,
                    data["Comment"]
                ]

                writer1.writerow(row)
                time.sleep(5)