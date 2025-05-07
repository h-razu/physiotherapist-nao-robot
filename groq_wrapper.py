import subprocess
import json
import os

def get_groq_response(prompt):
    try:
        # Path to Python 3.8 interpreter
        python38_path = r'C:\Users\hrazu\anaconda3\envs\groq_env\python.exe'
        # script_path = os.path.join(os.path.dirname(__file__), 'groq_runner.py')
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(CURRENT_DIR, 'groq_runner.py')

        # Copy env and add Groq API key
        env = os.environ.copy()
        env["GROQ_API_KEY"] = "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"

        # Start subprocess using Python 3.8
        process = subprocess.Popen(
            [python38_path, script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # Needed for Python 2.7
            env=env
        )

        # Parse single paragraph response
        input_data = json.dumps({"prompt": prompt})
        stdout, stderr = process.communicate(input=input_data)

        try:
            result = json.loads(stdout.strip())
            return result.get("response")
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return None

    except Exception as e:
        print("Exception occurred:", str(e))
        return None
    


# if __name__ == "__main__":
#     prompt = "Explain the importance of fast language models in five sentences"
#     response = get_groq_response(prompt)
#     print(response)