'''
Code to embed a text file into a vector space and visualise it using UMAP
'''

import ollama
import umap
import matplotlib.pyplot as plt
import argparse
import textwrap
import numpy as np
import plotly.graph_objects as go
from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import output_file
#from sentence_transformers import SentenceTransformer
#from sentence_transformers.util import cos_sim


def chunks_from_file(filename):
    # read in a file and chunk it using # as the delimiter
    with open(filename) as f:
        raw = f.read()

    # split into chunks corresponding to sections
    chunks = raw.split('#')
    # remove empty chunks
    chunks = [chunk for chunk in chunks if chunk]

    # for chunks of fixed size, uncomment the following lines:
    '''
    chunk_size = 250 # size in characters
    chunk_overlap = 50
    chunks = []''

    for i in range(0, len(raw), chunk_size):
        chunks.append(raw[i:i + chunk_size])
        # use the most common word in the chunk as the label
        labels = [most_common_word(chunk) for chunk in chunks]'''

    return chunks

# get the mode and parameters from the command line
parser = argparse.ArgumentParser()
parser.add_argument("-q", "--question", help="set to True if want to add a question to embed", action="store_true")
parser.add_argument("-d", "--min_dist", type=float, default=0.5, help="minimum distance for UMAP")
parser.add_argument("-n", "--n_neighbours", type=int, default=15, help="number of neighbours for UMAP")
args = parser.parse_args()

min_dist = args.min_dist
n_neighbours = args.n_neighbours

filename = './work/pdf_to_txt/output/cleaned/Binney_and_Tremaine.mmd'
labels_filename = './work/pdf_to_txt/output/to_clean/Binney_and_Tremaine.mmd'

model = 'nomic-embed-text'

plot_title = f'UMAP projection of the entire B&T embeddings with {model}\nmin_dist={min_dist}, n_neighbors={n_neighbours}'
outfile_title = f'./work/plots/umap_whole_interactive_test.png'

chunks = chunks_from_file(filename)
chunks_uncleaned = chunks_from_file(labels_filename)
# use the first line of each chunk as the label
labels = [chunk.split('\n')[0] for chunk in chunks_uncleaned]

# if the question flag is set, add the question input by the user to the chunks
if args.question:
    question = input("Enter the question to embed: ")
    chunks.append(question)  # add the question to the chunks if in question mode
    labels.append('question')

# count the number of words in each chunk
words = [len(chunk.split()) for chunk in chunks] 

# create the embeddings for the documents

response = ollama.embed(model=model, input=chunks)
doc_embeddings = np.array(response["embeddings"])

# uncomment the following lines to use all-MiniLM-L6-v2 embedding model form Sentence Transformers instead
#embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'
#caches_dir = '/home/hgolawska/llm_summer_project/caches'
#model = SentenceTransformer(embedding_model, cache_folder=caches_dir, local_files_only=True)
#doc_embeddings = model.encode(chunks, show_progress_bar=True)

# visualise in 2D
    
# reduce the dimensionality of the embeddings using UMAP
flat_embeddings = umap.UMAP(n_components=2, min_dist=min_dist, n_neighbors=n_neighbours, metric='cosine').fit(doc_embeddings)

# plot the 2D embeddings

fig, ax = plt.subplots(figsize=(12,12))
ax.scatter(flat_embeddings.embedding_[:-1, 0], flat_embeddings.embedding_[:-1, 1], color='lightblue', alpha=1, s=30, edgecolors=None)

# add wrapped labels
for i in range(0, flat_embeddings.embedding_.shape[0]-1):
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
    
# change colors of the last point if question nmode is activated

if args.question:
    color_scatter = 'red'
    color_label = 'red'
else:
    color_scatter = 'lightblue'
    color_label = 'black'

ax.scatter(flat_embeddings.embedding_[-1, 0], flat_embeddings.embedding_[-1, 1], color=color_scatter, alpha=1, s=30, edgecolors=None)

wrapped_label = "\n".join(textwrap.wrap(labels[-1], width=15))
ax.text(flat_embeddings.embedding_[-1, 0],
        flat_embeddings.embedding_[-1, 1],
        wrapped_label,
        color='black',
        fontsize=8,
        horizontalalignment='center',
        verticalalignment='center',
    )

ax.set_aspect('equal')
plt.title(plot_title)
#plt.savefig(outfile_title, dpi=300)

# interactive 2D plot using bokeh

source = ColumnDataSource(data=dict(
    x=flat_embeddings.embedding_[:, 0], 
    y=flat_embeddings.embedding_[:, 1], 
    label=labels))
question_source = ColumnDataSource(data=dict(
    x=[flat_embeddings.embedding_[-1, 0]],
    y=[flat_embeddings.embedding_[-1, 1]],
    label=['Question']))

output_file(f"./work/plots/interactive_scatter_all_question.html")

p = figure(title=plot_title, tools="pan,wheel_zoom,box_zoom,reset,save", width=800, height=800)
p.scatter('x', 'y', source=source, size=10, color='deepskyblue', alpha=0.5, legend_label='Binney and Tremaine')
if args.question:
    p.scatter('x', 'y', source=question_source, size=10, color='red', legend_label=f'Question: {question}')
hover = HoverTool(tooltips = [("", "@label")])
p.add_tools(hover)

save(p)


# visualise in 3D - interactive plot using plotly

flat_embeddings = umap.UMAP(n_components=3, min_dist=min_dist, n_neighbors=n_neighbours, metric='cosine').fit(doc_embeddings)
embeddings_array = flat_embeddings.embedding_

x, y, z = embeddings_array[:, 0], embeddings_array[:, 1], embeddings_array[:, 2]
trace1 = go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    name='Binney and Tremaine chapters',
    text=labels,
    hovertemplate='%{text}<extra></extra>',
    marker=dict(
        color='rgba(0, 0, 245, 0.5)',
        size=12
    )
)

if args.question:

    # add the question point

    x2, y2, z2 = embeddings_array[-1, 0], embeddings_array[-1, 1], embeddings_array[-1, 2]

    trace2 = go.Scatter3d(
        x=[x2],
        y=[y2],
        z=[z2],
        mode='markers',
        text=[f'Question: {question}'],
        hovertemplate='%{text}<extra></extra>',
        name=f'Question: {question}',
        marker=dict(
            color='rgba(162, 32, 21, 0.7)',
            size=12,
            symbol='circle',
            line=dict(
                color='rgb(162, 32, 21)',
                width=1
            ),
        )
    )

    data = [trace1, trace2]

else: 
    data = [trace1]

layout = go.Layout(
    title_text=f'3D UMAP projection of the entire B&T embeddings with min_dist={min_dist} and n_neighbours={n_neighbours}',
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=50
    ),
        legend=dict(
        x=0,  # Position legend at left edge
        y=1,  # Position legend at top
        xanchor='left',  # Anchor to left side
        yanchor='top'    # Anchor to top
    )
)
fig = go.Figure(data=data, layout=layout)
fig.write_html('./work/plots/interactive-3d-scatter-all.html')

print(f"Using min_dist={min_dist} and n_neighbours={n_neighbours} for UMAP")


#print('maximum number of words in a chunk:', max(words))
#print('average number of words in a chunk:', sum(words) / len(words))
