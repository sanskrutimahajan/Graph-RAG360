import requests
response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3", "prompt": "Hello!", "stream": False}
)
print("Status code:", response.status_code)
print("Raw text:", response.text)
try:
    print("JSON:", response.json())
except Exception as e:
    print("Error parsing JSON:", e) 