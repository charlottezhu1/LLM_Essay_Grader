# LLM_Essay_Grader
Stanford CS139 Final Project
By: Charlotte Zhu & Nancy Hoang

- [Final Presentation Slides](https://docs.google.com/presentation/d/1IAzWkQknlMgr-yVjqIZ2XEUrS-5UGfL5ZiL8-iyvthU/edit?usp=sharing)  


## Project Overview
We explores the Efficacy and Ethics of AI Graders in Essay Evaluation.
The code component can grade essay using the GPT, Claude, and Gemini API.

## Research Question
How consistent was the AI grading across models compared to human grader?

## How to Run

1. Add a settings.py with API Keys
   OPENAI_API_KEY="your key"
   ANTHROPIC_API_KEY="your key"
   GEMINI_API_KEY="your key"

2. Run The follwing commands
   ```
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
   
3. To grade the essay, run:
   ```
   python3 main.py
   ```
   The default is gemini-1.5-flash with temperature 1. You can change it to other models and temperature with extra command line arguments.

   For example:
   ```
   python3 main.py --company openai --model gpt-4o --temperature 0.5
   ```
   Make sure the company and model are aligned. 

4. The sort.ipynb file include method to analyze the output.
