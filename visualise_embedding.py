'''
Code to embed a text file into a vector space and visualise it using UMAP
'''

import ollama
import umap
import umap.plot
import matplotlib.pyplot as plt
import string
import textwrap
import numpy as np
#from sentence_transformers import SentenceTransformer
#from sentence_transformers.util import cos_sim

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

#embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'

min_dist = 0.9
n_neighbors = 30

caches_dir = '/home/hgolawska/llm_summer_project/caches'
filename = './work/pdf_to_txt/output/cleaned/Binney_and_Tremaine_1-3_no_rrp.mmd'

plot_title = f'UMAP projection of B&T 1-3 embeddings with nomic-embed-text\nmin_dist={min_dist}, n_neighbors={n_neighbors}'
outfile_title = f'./work/plots/umap_1-3_no_rrp_four_hashtags.png'

#model = SentenceTransformer(embedding_model, cache_folder=caches_dir, local_files_only=True)
#model = 'mxbai-embed-large'
model = 'nomic-embed-text'

chunk_size = 250
chunk_overlap = 50

# read the documents and create the chunks
with open(filename) as f:
    raw = f.read()

# split into fixed size chunks
'''
chunks = []

for i in range(0, len(raw), chunk_size):
    chunks.append(raw[i:i + chunk_size])
    # use the most common word in the chunk as the label
    labels = [most_common_word(chunk) for chunk in chunks]'''

# split into chunks corresponding to sections
chunks = raw.split(' #### ')
# remove empty chunks
chunks = [chunk for chunk in chunks if chunk]
# use the first line of each chunk as the label
labels = [chunk.split('\n')[0] for chunk in chunks]
#print(labels[:10])  # print the first 10 labels for debugging
# count the number of words in each chunk
words = [len(chunk.split()) for chunk in chunks] 



# print(chunks[0])  # print the first chunk
# print(labels[0])  # print the label for the first chunk

# create the embeddings for the documents



#doc_embeddings = model.encode(chunks, show_progress_bar=True)
response = ollama.embed(model=model, input=chunks)
doc_embeddings = response["embeddings"]
print('calculated embeddings')
doc_embeddings = np.array(doc_embeddings)
print('embedding shape:', doc_embeddings.shape)

min_dist = 0.5
n_neighbors = 15

# reduce the dimensionality of the embeddings using UMAP
flat_embeddings = umap.UMAP(n_components=2, min_dist=min_dist, n_neighbors=n_neighbors, metric='cosine').fit(doc_embeddings)
print('flat embedding shape:', flat_embeddings.embedding_.shape)

# plot the embeddings

fig, ax = plt.subplots(figsize=(12,12))
ax.scatter(flat_embeddings.embedding_[:, 0], flat_embeddings.embedding_[:, 1], color='lightblue', alpha=1, s=30, edgecolors=None)
ax.set_aspect('equal')
# add a label for one in 10 points
for i in range(0, flat_embeddings.embedding_.shape[0]):
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
plt.title(plot_title)
plt.savefig(outfile_title, dpi=300)

print('maximum number of words in a chunk:', max(words))
print('average number of words in a chunk:', sum(words) / len(words))