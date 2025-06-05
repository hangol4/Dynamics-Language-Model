import ollama

result = ollama.generate(
    # This model is reasonably fast even on my crappy laptop
    'llama3.2',
    'What is the best deep learning framework?',
)

print(result['response'])