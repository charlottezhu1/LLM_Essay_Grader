import base64
import httpx
import json
import csv
import os
from docx import Document
import google.generativeai as genai
from settings import *
from parse_json import*

genai.configure(api_key=GEMINI_API_KEY)
image_path = "https://enpuyfxhpaelfcrutmcy.supabase.co/storage/v1/object/public/grader/Essay%20Rubric.png"
image = httpx.get(image_path)


def simple_gen_gem(prompt, model="gemini-1.5-flash"):
    model = genai.GenerativeModel(model)
    response = model.generate_content([{'mime_type':'image/jpeg', 'data': base64.b64encode(image.content).decode('utf-8')}, prompt])
    content = response.text
    try:
        json_content = parse_json(content)
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
    prompt = "Caption this image."

    response = model.generate_content([{'mime_type':'image/jpeg', 'data': base64.b64encode(image.content).decode('utf-8')}, prompt])
    print(response.text)