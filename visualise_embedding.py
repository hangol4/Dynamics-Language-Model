'''
Code to embed a text file into a vector space and visualise it using UMAP
'''

import ollama
import umap
import umap.plot
import matplotlib.pyplot as plt
import argparse
import textwrap
import numpy as np
import plotly.graph_objects as go
from bokeh.plotting import figure, show, save
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

print(f"Using min_dist={min_dist} and n_neighbours={n_neighbours} for UMAP")

#min_dist = 0.9
#n_neighbours = 30

caches_dir = '/home/hgolawska/llm_summer_project/caches'
filename = './work/pdf_to_txt/output/cleaned/Binney_and_Tremaine_chap2_v1_all.mmd'
labels_filename = './work/pdf_to_txt/output/to_clean/Binney_and_Tremaine_chap2_v1.mmd'

plot_title = f'UMAP projection of the entire B&T embeddings with nomic-embed-text\nmin_dist={min_dist}, n_neighbors={n_neighbours}'
outfile_title = f'./work/plots/umap_whole_interactive_test.png'

#embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'
#model = SentenceTransformer(embedding_model, cache_folder=caches_dir, local_files_only=True)

#model = 'mxbai-embed-large'
model = 'nomic-embed-text'

chunks = chunks_from_file(filename)
chunks_uncleaned = chunks_from_file(labels_filename)
# use the first line of each chunk as the label
labels = [chunk.split('\n')[0] for chunk in chunks_uncleaned]

# if the question flag is set, add the question input by the user to the chunks
if args.question:
    print("Question mode activated")
    question = input("Enter the question to embed: ")
    chunks.append(question)  # add the question to the chunks if in question mode
    labels.append('question')

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

mode = '3D'

if mode == '2D':
    # reduce the dimensionality of the embeddings using UMAP
    flat_embeddings = umap.UMAP(n_components=2, min_dist=min_dist, n_neighbors=n_neighbours, metric='cosine').fit(doc_embeddings)


    # plot the embeddings

    fig, ax = plt.subplots(figsize=(12,12))
    ax.scatter(flat_embeddings.embedding_[:-1, 0], flat_embeddings.embedding_[:-1, 1], color='lightblue', alpha=1, s=30, edgecolors=None)
    # add the last point in red
    ax.scatter(flat_embeddings.embedding_[-1, 0], flat_embeddings.embedding_[-1, 1], color='red', alpha=1, s=30, edgecolors=None)
    # add the labels to all points except for the last one
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
        # add the last point and label it 'question'
    ax.text(flat_embeddings.embedding_[-1, 0],
            flat_embeddings.embedding_[-1, 1],
            'question',
            color='red',
            fontsize=8,
            horizontalalignment='center',
            verticalalignment='center',
            )
    ax.set_aspect('equal')
    plt.title(plot_title)
    plt.savefig(outfile_title, dpi=300)
    #plt.show()

    # interactive plot using bokeh
    source = ColumnDataSource(data=dict(
        x=flat_embeddings.embedding_[:, 0], 
        y=flat_embeddings.embedding_[:, 1], 
        label=labels))
    question_source = ColumnDataSource(data=dict(
        x=[flat_embeddings.embedding_[-1, 0]],
        y=[flat_embeddings.embedding_[-1, 1]],
        label=['question']))

    output_file(f"./work/plots/interactive_scatter_all_question.html")

    p = figure(title=plot_title, tools="pan,wheel_zoom,box_zoom,reset,save", width=800, height=800)
    p.scatter('x', 'y', source=source, size=10, color='deepskyblue', alpha=0.5, legend_label='Binney and Tremaine')
    if args.question:
        p.scatter('x', 'y', source=question_source, size=10, color='red', legend_label=f'Question: {question}')
    hover = HoverTool(tooltips = [("", "@label")])
    p.add_tools(hover)
    #show(p)


    save(p)

else:
    flat_embeddings = umap.UMAP(n_components=2, min_dist=min_dist, n_neighbors=n_neighbours, metric='cosine').fit(doc_embeddings)
    embeddings_array = flat_embeddings.embedding_
    print('embeddings shape:', embeddings_array.shape)

    x, y, z = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 200).transpose()
    trace1 = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=12,
            line=dict(
                color='rgba(217, 217, 217, 0.14)',
                width=0.5
            ),
            opacity=0.8
        )
    )

    x2, y2, z2 = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 200).transpose()
    trace2 = go.Scatter3d(
        x=x2,
        y=y2,
        z=z2,
        mode='markers',
        marker=dict(
            color='rgb(127, 127, 127)',
            size=12,
            symbol='circle',
            line=dict(
                color='rgb(204, 204, 204)',
                width=1
            ),
            opacity=0.9
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )
    fig = go.Figure(data=data, layout=layout)
    fig.write_html('./work/plots/simple-3d-scatter.html')

#print('maximum number of words in a chunk:', max(words))
#print('average number of words in a chunk:', sum(words) / len(words))
