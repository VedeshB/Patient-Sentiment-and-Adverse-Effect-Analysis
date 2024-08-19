from groq import Groq
def genai(initial):
    client = Groq(api_key="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")
    chat_completion = client.chat.completions.create(
        messages=[
                {
                    "role": "user",
                    "content": initial,
                }
                ],
        model="llama3-8b-8192",
            )
    response=chat_completion.choices[0].message.content
    return response