import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_with_gemini(flight_data):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"""You are a data analyst for an airline company.

Here is the flight dataset:
{flight_data}

Generate insights including:
- Most common routes
- Time patterns (peak hours or days)
- Status trends (delayed, scheduled, etc.)
- Anomalies or demand spikes

Keep it short and business-friendly."""

    response = model.generate_content(prompt)
    return response.text
