import os, json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Use a model you have access to:
MODEL = os.getenv("LLAMA_MODEL_NAME", "gpt-3.5-turbo")

def extract_graph_from_text(text: str) -> dict:
    prompt = f"""
    Extract a knowledge graph from the following document. 
    Return JSON with two top-level keys: "nodes" and "edges"…
    Document:
    \"\"\"{text}\"\"\"
    """
    resp = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    content = resp.choices[0].message.content.strip()
    return json.loads(content)
