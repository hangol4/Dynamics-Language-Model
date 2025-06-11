'''
Code to embed a text file into a vector space and visualise it using UMAP
'''

#import ollama
import umap
import umap.plot
import matplotlib.pyplot as plt
import string
import textwrap
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

def most_common_word(chunk):
    # remove punctuation, convert to lowercase and split the chunk into words
    chunk = chunk.translate(str.maketrans('', '', string.punctuation))
    chunk = chunk.lower()
    words = chunk.split()
    # remove stop words
    stop_words = set(['the', 'is', 'in', 'and', 'to', 'a', 'of', 'that', 'it', 'for', 'on', \
                      'with', 'as', 'this', 'by', 'an', 'are', 'was', 'at', 'be', 'from', 'or', 'not', 'but', 'which', 'we'])
    words = [word for word in words if word not in stop_words]
    # keep the data in a dictionary
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    # Find the word with the highest count
    most_common = None
    highest_count = 0
    for word, count in word_count.items():
        if count > highest_count:
            most_common = word
            highest_count = count
    return most_common

embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'
caches_dir = '/home/hgolawska/llm_summer_project/caches'
filename = './work/pdf_to_txt/output/Binney_and_Tremaine_chap2.mmd'

chunk_size = 250
chunk_overlap = 50

# read the documents and create the chunks
with open(filename) as f:
    raw = f.read()

chunks = []

for i in range(0, len(raw), chunk_size):
    chunks.append(raw[i:i + chunk_size])

#chunks = raw.split('#')
# remove empty chunks
chunks = [chunk for chunk in chunks if chunk]

# Get labels for each chunk
labels = [most_common_word(chunk) for chunk in chunks]
#labels = [chunk.split('\n')[0] for chunk in chunks]
#print(labels[:10])  # print the first 10 labels for debugging


# print(chunks[0])  # print the first chunk
# print(labels[0])  # print the label for the first chunk

# create the embeddings for the documents
model = SentenceTransformer(embedding_model, cache_folder=caches_dir, local_files_only=True)
print('loaded an embedding model')

doc_embeddings = model.encode(chunks, show_progress_bar=True)
print('calculated embeddings')

print('embedding shape:', doc_embeddings.shape)

# reduce the dimensionality of the embeddings using UMAP
flat_embeddings = umap.UMAP(n_components=2, metric='cosine').fit(doc_embeddings)
print('flat embedding shape:', flat_embeddings.embedding_.shape)

# plot the embeddings

plt.figure(figsize=(10, 10))
plt.title('UMAP projection of the document embeddings')
umap.plot.points(flat_embeddings)
plt.savefig('work/plots/umap_projection_words.png', dpi=300)

fig, ax = plt.subplots(figsize=(12,12))
ax.scatter(flat_embeddings.embedding_[:, 0], flat_embeddings.embedding_[:, 1], color='lightblue', alpha=0.4, s=30, edgecolors=None)
ax.set_aspect('equal')
# add a label for one in 10 points
for i in range(0, flat_embeddings.embedding_.shape[0], 10):
    # Wrap the label to a maximum width (e.g., 15 characters per line)
    wrapped_label = "\n".join(textwrap.wrap(labels[i], width=15))
    ax.text(flat_embeddings.embedding_[i, 0],
            flat_embeddings.embedding_[i, 1],
            wrapped_label,
            color='black',
            fontsize=8,
            horizontalalignment='center',
            verticalalignment='center',
           )
plt.title('UMAP projection of the document embeddings with labels')
plt.savefig('work/plots/umap_projection_words.png', dpi=300)