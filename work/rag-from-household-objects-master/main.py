import ollama
print('imported ollama')
from sentence_transformers import SentenceTransformer
print('imported sentence_transformers')
from sentence_transformers.util import cos_sim
print('imported cos_sim')

# file with our "documents"
fn = '/home/hgolawska/llm_summer_project/Dynamics-Language-Model/work/rag-from-household-objects-master/data/ig.txt'

embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'
llm_model = 'phi3:mini-128k'

chunk_size = 250
chunk_overlap = 50

# how many results to use as context
top_k = 5

# read the documents and create the chunks
with open(fn) as f:
    raw = f.read()

chunks = []

for i in range(0, len(raw), chunk_size):
    chunks.append(raw[i:i + chunk_size])

# print(chunks[0])  # print the first chunk

# create the embeddings for the documents
model = SentenceTransformer(embedding_model)
print('loaded an embedding model')

doc_embeddings = model.encode(chunks, show_progress_bar=True)
print('calculated embeddings')

while True:
    query = input('Ask a question: ')
    query_embedding = model.encode(query)

    similarities = cos_sim(query_embedding, doc_embeddings).flatten()

    # take the chunks with the top_k largest similarities
    best_chunk_indexes = similarities.argsort()[-top_k:]
    best_chunks = [chunks[i] for i in best_chunk_indexes]

    # create some background info
    info = "\n----------\n".join(best_chunks)

    prompt = f"""Please answer the question using the provided background info:
    
    question: {query}
    
    background info: {info}"""

    stream = ollama.generate(llm_model, prompt, stream=True)

    for chunk in stream:
        print(chunk['response'], end='', flush=True)

    print("\n\n")