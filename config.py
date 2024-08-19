import os
import openai

from dotenv import load_dotenv

load_dotenv()

# OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_model = "gpt-4o"

# Unpaywall API
user_email = os.getenv("USER_EMAIL")

# study details
topic="Age-Related Macular Degeneration - mechanism, symptoms, treatment"
RQs="""
    1. What are the mechanisms and pathophysiological processes involved in the development and progression of age-related macular degeneration (AMD)?
    2. What are the clinical symptoms of age-related macular degeneration, and what diagnostic methods are most effective in detecting and staging the disease?
    3. What are the current treatment options for both dry and wet forms of age-related macular degeneration, and how can these treatments be optimized for better efficacy and patient outcomes?
"""
short_name = "AMD"