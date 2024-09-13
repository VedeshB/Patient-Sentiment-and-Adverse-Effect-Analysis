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
