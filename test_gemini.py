from google import genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-3.1-flash-lite-image",
    contents="A cute baby elephant, black and white coloring book page, thick bold outlines, white background, no shading"
)

print(response)