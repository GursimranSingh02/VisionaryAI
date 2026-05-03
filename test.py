from google import genai
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()
MODEL = "gemini-3-flash-preview"
# MODEL = "gemini-2.5-flash"

response = client.models.generate_content(
    model=MODEL,
    contents="How does AI work?"
)
print(response.text)