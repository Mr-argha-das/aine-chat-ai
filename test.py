import openai

# Set your OpenAI API key
api_key = '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'
openai.api_key = api_key

# Define your prompt
prompt = "Once upon a time,"

# Generate text using ChatGPT
response = openai.Completion.create(
    engine="gpt-3.5-turbo-instruct",  # Specify the model (ChatGPT)
    prompt=prompt,
    max_tokens=50  # Adjust as needed
)

# Output the generated text
print(response.choices[0].text.strip())
