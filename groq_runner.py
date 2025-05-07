import os
import sys
import json
from groq import Groq

def main():
    try:
        input_data = json.loads(sys.stdin.read())
        prompt = input_data.get("prompt", "")

        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-70b-8192"
        )

        response_text = chat_completion.choices[0].message.content
        
        print(json.dumps({"response": response_text.strip()}))
        sys.stdout.flush()

    except Exception as e:
        print(json.dumps({"sentence": None, "error": str(e)}))
        sys.stdout.flush()

if __name__ == "__main__":
    main()
