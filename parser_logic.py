import google.generativeai as genai
import json

PROMPT_TEMPLATE = """
You are an intelligent document parser.

Extract structured data and return ONLY valid JSON.

If something is missing, return null.

Schema:
{
  "document_type": "",
  "name": "",
  "date": "",
  "amount": "",
  "invoice_number": ""
}
"""

def get_gemini_response(model, image):
    response = model.generate_content([PROMPT_TEMPLATE, image])
    return response.text


def clean_json_output(raw_text):
    try:
        return json.loads(raw_text)
    except:
        # fallback cleaning
        raw_text = raw_text.strip("```json").strip("```")
        return json.loads(raw_text)