# code adapted from https://ollama.com/blog/embedding-models 

import ollama
import chromadb

# file with our "documents"
fn = '/home/hgolawska/llm_summer_project/Dynamics-Language-Model/work/rag-from-household-objects-master/data/ig.txt'

documents = [
  "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
  "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
  "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
  "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
  "Llamas are vegetarian and have very efficient digestive systems",
  "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]

# Step 1: Generate embeddings

client = chromadb.Client()
collection = client.create_collection(name="docs")

with open(fn) as f:
    raw = f.read()

documents = []

chunk_size = 500
chunk_overlap = 50

for i in range(0, len(raw), chunk_size):
    documents.append(raw[i:i + chunk_size])

# store each document in a vector embedding database
for i, d in enumerate(documents):
  response = ollama.embed(model="nomic-embed-text", input=d)
  embeddings = response["embeddings"]
  collection.add(
    ids=[str(i)],
    embeddings=embeddings,
    documents=[d]
  )

# Step 2: Retrieve

# an example input
example_input = "Who won the 2014 ig nobel prize for psychology?"

# generate an embedding for the input and retrieve the most relevant doc
response = ollama.embed(
  model="nomic-embed-text",
  input=example_input
)
results = collection.query(
  query_embeddings=response["embeddings"],
  n_results=5
)


data = results['documents'][0]


# Step 3: Generate

# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="llama3.2",
  prompt=f"Using this data: {data}. Respond to this prompt: {example_input}",
)

print(f"Retrieved data: {data}")

print(output['response'])

# exit


