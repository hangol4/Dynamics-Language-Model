# Dynamics Language Model

Summer project: building a llama-based large language model (LLM) specialised in galaxy dynamics by leveraging Retrieval-Augmented Generation (RAG). Our main source of information is a well-known textbook 'Galactic Dynamics' by James Binney and Scott Tremaine (Second Edition). To translate PDF files into text, we use [Nougat](https://github.com/facebookresearch/nougat/tree/main) -  a PDF parser that understands LaTeX math and tables. It performs an Optical Character Recognition (OCR) task for processing scientific documents into a markup language. 

The main output from the project is the `visualise_embedding.py` script that reads in the text of Binney and Tremaine from a .mmd file, splits it into subsections, and embeds these subsections using a chosen embedding model. Then, it reduces the dimensionality of the embeddings to 2D and 3D using [UMAP](https://umap-learn.readthedocs.io/en/latest/index.html), and visualises the results in interactive plots. The script can also embed a question and visualise it in the same embedding space as the textbook subsections. Example output plots can be found in the [Dynamics-Language-Model-Plots](https://github.com/hangol4/Dynamics-Language-Model-Plots) repository. 

To build a specialist LLM, work presented in this repository must be followed by fine-tuning or advanced RAG, as all the simple RAG examples we managed to find were not satisfactory for our purposes. The RAG examples can be found in the [rag_examples](work/rag_examples) directory, and are summarised in the [RAG examples](#rag-examples) section below.

The project was carried out by Hanna Golawska, supervised by Michael Petersen and funded by the Physics and Astronomy Career Development Scholarship from School of Physics and Astronomy, University of Edinburgh.

## Table of Contents
- [Dynamics Language Model](#dynamics-language-model)
- [Table of Contents](#table-of-contents)
- [Getting started with Ollama](#getting-started-with-ollama)
    - [Locally](#locally)
    - [Cuillin](#cuillin)
    - [Model file](#model-file)
    - [Downloading models from the internet](#downloading-models-from-the-internet)
    - [Model Choice](#model-choice)
- [Getting started with Nougat on Cuillin](#getting-started-with-nougat-on-cuillin)
- [Visualising embeddings](#visualising-embeddings)
    - [Running the script](#running-the-script)
    - [Setting up Sentence Transformers](#setting-up-sentence-transformers)
    - [Embedding model selection](#embedding-model-selection)
- [RAG examples](#rag-examples)
    - [rag-from-household-objects.py](#rag-from-household-objects.py)
    - [ollama_rag_example.py](#ollama_rag_example.py)
    - [langchain/qa/qa.ipynb](#langchainqaqa.ipynb)
    - [mistralai_rag_examples/basic_RAG.ipynb](#mistralairag_examplesbasic_rag.ipynb)
    - [langchain/run_locally/rag-locally-on-intel-cpu.ipynb](#langchainrun_locallyrag-locally-on-intel-cpu.ipynb)

## Getting started with Ollama

### Locally
(Apple MacBook with M2 chip, macOS Sonoma 14.5)

1. Initialisation

    Go to <https://ollama.com/> and install Ollama

2. Usage

    To run and chat with a selected model, e.g. Llama 3.2:

    ```bash
    ollama run llama3.2
    ```
    Only the first download will take long (depending on the size of the model). If you run `ollama run llama3.2` once again later on, it will be loaded from memory.

3. Exiting

    Type `/bye` to end a conversation, hit `cmd + C` / `ctrl + C` to interrupt generating.
   
### Cuillin
Adapted from [Mike's fork](https://github.com/michael-petersen/Dynamics-Language-Model/tree/5c41b9ec0f960147380407597075edf569fcdc29/cuillin)

1. Initialisation

    First, download ollama for Linux
    ```bash
    curl --fail --show-error --location --progress-bar "https://ollama.com/download/ollama-linux-amd64.tgz" | tar -xzf - -C /home/<username>
    ```

2. To get Ollama in your path (and be able to use the 'ollama' command instead of '/home/<username>/bin/ollama'), add the following line to /home/<username>/.bashrc:
    ```
    export PATH=/home/<username>/bin:$PATH
    ```


3. Obtaining new models

    On the login node,
    ```bash
    export OLLAMA_MODELS="/cephfs/<username>/LLM"
    ollama serve &
    ollama run llama4:scout
    ollama run llama4:maverick
    ollama run phi4-mini:latest
    ```
    To simply pull models without running, we can replace `run` with `pull`:
    ```bash
    ollama pull llama4:maverick
    ```

4. Production

    ```
    # request resources
    srun -n 16 --pty --mem=128GB $SHELL
    export OLLAMA_MODELS="/cephfs/<username>/LLM"

    # set the number of threads for Ollama to use
    export OLLAMA_NUM_THREADS=16

    # worker088, worker094 and worker095 are uniquely suited to take large process jobs
    srun -n 64 --pty --mem=256GB $SHELL
    export OLLAMA_MODELS="/cephfs/<username>/LLM"

    # set the number of threads for Ollama to use
    export OLLAMA_NUM_THREADS=64

    # start the server as a background process
    ollama serve &

    # start the LLM
    ollama run llama4:scout
    ```

    The larger models can take quite a while to load: review the memory usage before making plans for a quick session! 

5. Closing the server

    Once you're done, run `lsof -i :11434`, then identify the PID of the LISTEN process. Then run `kill <PID>` to close the server.
    

### Model file

A model file serves as the blueprint for creating and sharing models with Ollama. It can be used to control the model's hyperparameters, such as temperature and size of the context window, and to set the system prompt. 

An example model file can look like this:

```
FROM llama3.2
# sets the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 1
# sets the context window size to 4096, this controls how many tokens the LLM can use as context to generate the next token
PARAMETER num_ctx 4096

# sets a custom system message to specify the behavior of the chat assistant
SYSTEM You are Mario from super mario bros, acting as an assistant.
```

To use this:

1. Save it as a file (e.g. `Modelfile`)
2. `ollama create choose-a-model-name -f <location of the file e.g. ./Modelfile>`
3. `ollama run choose-a-model-name`
4. Start using the model!

Find more information, instructions and valid hyperparameters and values on the [Ollama GitHub page](https://github.com/ollama/ollama/blob/c9e6d7719e91d0bfa3bc6e73ddce0f5c7c3c26f1/docs/modelfile.md#instructions).

### Downloading models from the internet

Some community models are not accessible via Ollama, but can be downloaded from the internet as .gguf files. For example, [AstroSage](https://doi.org/10.48550/arXiv.2505.17592) can be downloaded from [Hugging Face](https://huggingface.co/AstroMLab).

To build a model from a .gguf file:

1. Find the desired .gguf file on Hugging Face, click on 'copy download link'
2. To download a file to your local machine via terminal, use the `wget` command:
   ```bash
   wget https://huggingface.co/AstroMLab/AstroSage-8B-GGUF/resolve/main/AstroSage-8B-Q8_0.gguf
   ```
3. Create a file named Modelfile, and add a FROM instruction with the local filepath to AstroSage, e.g.,
    ```
    FROM ./AstroSage-8B-Q8_0.gguf
    ```
4. Create the model in Ollama
    ```
    ollama create astrosage -f path_to_modelfile
    ```
5. Run AstroSage locally
    ```
    ollama run astrosage
    ```

### Model choice
Useful resources for choosing a model:
- [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783) - academic paper presenting the Llama 3 set of foundation models, including training procedures, architecture and performance benchmarks,
- [The Llama 4 herd](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) - release blog post by Meta AI,
- [Model library](https://ollama.com/library) on Ollama's website - a list of available models with download instructions and descriptions, containing information such as model size, context window size, and input formats (text, image, audio). See a shorter summary of the most popular models on [Ollama GitHub](https://github.com/ollama/ollama?tab=readme-ov-file#model-library),
- [AstroMLab 1: Who Wins Astronomy Jeopardy!?](https://doi.org/10.48550/arXiv.2407.1119) - the authors of this paper compared various large language models using the first astronomy-specific benchmarking dataset, with the division into proprietary and open-weights models. Find a more up-to-date comparison on [AstroMLab's Hugging Face](https://huggingface.co/AstroMLab),
- online benchmark leaderboards such as [LibeBench](https://livebench.ai/#/), [Vellum Leaderboard](https://www.vellum.ai/open-llm-leaderboard) and [Artificial Analysys Leaderboard](https://artificialanalysis.ai/leaderboards/models)- these compare skills such as math comprehension, reasoning and coding.

Considerations:
- memory: you should have at least 8 GB of RAM available to run the 7B models, 16 GB to run the 13B models, and 32 GB to run the 33B models,
- context window size: the larger the context window, the more information the model can use to generate the next token, but it might require more memory and make it slower,
- availability of API keys: some RAG scripts (e.g., many examples from LangChain) require an API key to access the model, which is not always available ([you must be in the US](https://llama.developer.meta.com/join_waitlist) to get a key for all Meta models). You can obtain a Mistral AI key to use Mistral Small for free [here](https://docs.mistral.ai/getting-started/quickstart/), but it does not always work, or try [these](https://github.com/langchain-ai/langchain/tree/master/cookbook) example notebooks from LangChain on running open source LLMs locally on Intel CPU (also discussed in the [RAG examples](#rag-examples) section below).

## Getting started with Nougat on Cuillin

1. About Nougat: it is a PDF document parser that understands LaTeX math and tables and translates them into [markdown language](https://mathpix.com/docs/mathpix-markdown/overview). 
    
2. Useful resources:
    - [MathPix Markdown](https://mathpix.com/docs/mathpix-markdown/how-to-mmd-vscode)  - a VS code extension to render markdown in VS code,
    - [Nougat website](https://facebookresearch.github.io/nougat/) with examples,
    - [Nougat GitHub page](https://github.com/facebookresearch/nougat/tree/main) with installation and usage instructions,
    - [Nougat: Neural Optical Understanding for Academic Documents](https://arxiv.org/abs/2308.13418) - academic paper introducing Nougat.

2. Initialisation

    On the login node, run 
    ```bash 
    module load anaconda
    pip install nougat-ocr
    pip install albumentations==1.0
    pip install transformers==4.38.2
    ```
3. Usage

    Nougat can be run on the worker/fcfs nodes:
    ```bash
    /home/<username>/.local/bin/nougat <path_to_pdf> -o <output_directory> --no-skipping --recompute
    ```
    the `--no-skipping` flag prevents Nougat from skipping pages even if they are problematic to convert, and `--recompute` forces it to recompute already computed PDF, discarding previous predictions.

    However, Nougat runs faster on GPUs. In order to do that, run these commands first: 
    ```bash 
    srun --pty -p GPU -n 1 --gres=gpu:1 --mem=64GB $SHELL
    export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
    ``` 
    and then run Nougat as usual.

4. Problems with Nougat
    - sometimes it omits some sections and subsections, identifying them with ** instead of ## (merging two or more subsections into one), uses an incorrect number of hashtags or omits section numbers,
    - it misinterprets boxes in Binney and Tremaine, recognising them as new sections but then merging with the rest of the text,
    - it makes mistakes while translating tables and equations, especially in subscripts and superscripts,
    - sometimes it replaces a paragraph with gibberish that doesn’t exist in the original text. The model can degenerate into repeating the same sentence over and over again, alternate between two sentences or sometimes change some words, so a strict repetition detection will not suffice. Even harder to detect are predictions where the model counts its own repetitions, which sometimes happens in the references section. Getting stuck in a repetitive loop is a known problem with Transformer-based models when sampled with greedy decoding ([source](https://arxiv.org/abs/2308.13418)). For the Dynamics Language Model, I used [clean_mmd.py](https://github.com/tijmen/cosmosage/blob/main/clean_mmd.py) from the creators of [Cosmosage](https://arxiv.org/html/2407.04420v1) to clean the Nougat output of these repetitions. It usually removes most of them, but not all.

## Visualising embeddings

### Running the `visualise_embedding.py` script

1. Install necessary libraries:
    ```bash
    module load anaconda
    pip install ollama
    pip install umap-learn
    pip install bokeh
    pip install plotly
    ```
2. Start an ollama server
    ```bash 
    ollama serve &
    ```
3. Tweak necessary lines, such as paths to input files and names for the plots.
4. Run the script: 
    ```bash
    python visualise_embedding.py 
    ```
    Optional arguments:

    `-q`, `--question` - add this flag if you want to ask a question and visualise it in the Binney and Tremaine embedding space,

    `-d`, `--min_dist <float>` - minimum distance for UMAP,

    `-n`, `--n_neighbours <int>` - number of nearest neighbours for UMAP.

    Find more information about UMAP parameters [here](https://umap-learn.readthedocs.io/en/latest/parameters.html).
5. At the end, close the Ollama server following the instructions in the [Getting started with Ollama on Cuillin](#cuillin) section.
6. The plots will get saved in the directory `work/plots`. To see example outputs, visit the accompanying repository [Dynamics-Language-Model-Plots](https://github.com/hangol4/Dynamics-Language-Model-Plots).


### Code structure

1. Read in an .mmd file and break it into chunks using '#' as delimiter - each chunk will be a subsection of Binney and Tremaine,
2. Read in subsection titles from the uncleaned version of the file because cleaning removes line breaks,
3. Select an embedding model and use the Ollama API to embed the chunks:
    ```python
    model = 'nomic-embed-text'
    response = ollama.embed(model=model, input=chunks)
    doc_embeddings = np.array(response["embeddings"])
    ```
    Alternatively, if using an embedding model accessible through Sentence Transformers:
    ```python
    embedding_model = 'sentence-transformers/all-MiniLM-L6-v2'
    model = SentenceTransformer(embedding_model, cache_folder=caches_dir, local_files_only=True)
    doc_embeddings = np.array(model.encode(chunks, show_progress_bar=True))
    ```
    See the next section for instructions on setting up Sentence Transformers.
4. The produced NumPy array has hundreds of dimensions - reduce its dimensionality to 2D and 3D using UMAP:
    ```python
    # reduce to 2D
    flat_embeddings = umap.UMAP(n_components=2, min_dist=min_dist, n_neighbors=n_neighbours, metric='cosine').fit(doc_embeddings)
    ```
    The `metric` parameter controls how distance is computed in the ambient space of the input data. We use the cosine metric, which uses the cosine of the angle between two vectors, which reflects the semantic similarity between chunks and is commonly used for calculating embeddings. 

5. Visualise and save the embeddings with `matplotlib` and `bokeh` in 2D, and with `plotly` in 3D. 

### Setting up Sentence Transformers
Adapted from [Mike's fork](https://github.com/michael-petersen/Dynamics-Language-Model/tree/5c41b9ec0f960147380407597075edf569fcdc29/cuillin)

1. Initialisation

    First, install through the terminal:
    ```bash
    module load anaconda
    pip install sentence-transformers
    ```
    You might need to update `timm` with `pip install --upgrade timm` as well.

    Then the login node, in Python:

    ```python
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2",cache_folder="/cephfs/mpetersen/LLM/")
    ```

    Both commands will take a good amount of time when they are first run, but successive caches will help.

3. Production

    On fcfs or worker nodes, in Python:
    ```python
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2",cache_folder="/cephfs/mpetersen/LLM/",local_files_only=True)
    ```

    After the model is cached, the import step is the only somewhat expensive one.


### Embedding model selection

1. Considerations:
    - context window size - if we give a text embedding model a string that’s too long, it will only encode the meaning of the first N tokens of the string, where N is the number of tokens in its context window ([source](https://nachi-keta.medium.com/context-window-and-vector-dimension-of-embedding-models-773167a04edb)). Embedding models with large context windows allow them to consider more surrounding text when creating embeddings, leading to better contextual understanding and more relevant results, especially for longer documents. While LLMs are pushing the boundaries of context window sizes, embedding models are often optimised for efficiency and speed. 
    - memory and model training - for transformer models like BERT, RoBERTa, DistilBERT, etc., the runtime and memory requirements grow quadratically with the input length. This limits transformers to inputs of certain lengths. A common value for BERT-based models is 512 tokens, which corresponds to about 300-400 words (for English). Also, note that if a model was trained on short texts, the representations for long texts might not be that good ([source](https://sbert.net/examples/sentence_transformer/applications/computing-embeddings/README.html#input-sequence-length))

2. Open source model comparison

| Embedding model          | Parameter size          | Size          | Context window (tokens)          | Source                          |
|--------------------------|-------------------------|---------------|----------------------------------|------------------------------------------|
| mxbai-embed-large        | 334M                    | 670MB         | 512                              | Ollama                                   |
| all-minilm               | 23M                     | 67MB          | 512                              | Ollama                                   |
| all-MiniLM-L6-v2         | 22.7M                   | 80MB          | 256                              | ST                                       |
| all-mpnet-base-v2        | 109M                    | 420MB         | 384                              | ST (best performance overall)            |
| gtr-t5-xxl               | 4.86B                   | 9230MB        | 512                              | ST (fine-tuned for semantic search)      |
| nomic-embed-text-v1      | 137M                    | 547MB         | 8192                             | Nomic (accessible through ST and Ollama) |


ST = Sentence Transformers

We selected `nomic-embed-text-v1` due to its large context window, which is necessary to embed entire subsections of Binney and Tremaine at once.

## RAG examples

Over the course of the project, we downloaded from the internet and tested many RAG examples. The performacnce of neither of them was satisfactory for our purposes. They can be found in the [rag_examples](work/rag_examples) directory, and are summarised below. 

### `rag-from-household-objects.py`
- [source](https://github.com/joelgrus/rag-from-household-objects)
- follow instructions in [Setting up Sentence Transformers](#setting-up-sentence-transformers)
- when using the suggested database of ig nobels, it can't answer simple questions such as 'Who won the 2014 ig nobel prize for psychology?' or 'What did Brian Wansink win an ig nobel for?', even when one chunk is the entry for an entire year. It seems like the less common words, such as '2014' and proper nouns, don't get embedded

### `ollama_rag_example.py`
- [source](https://ollama.com/blog/embedding-models)
- before running the script, install Chroma with `pip install chromadb`
- it answers the example questions about llamas well, but when trying to query the ig nobel database it doesn't retrieve the relevant chunk, even when we try to retrieve the two most relevant chunks and use relatively large chunks (2000 characters - see [retrieved_chunks_ollama_rag_example](work/rag_examples/retreived_chunks_ollama_rag_example/))

### `langchain/qa/qa.ipynb`
- [source](https://github.com/hwchase17/chroma-langchain/blob/master/qa.ipynb)
- Ollama API keys necessary, doesn't work with free API keys from Mistral AI

### `mistralai_rag_examples/basic_RAG.ipynb`
- [source](https://github.com/mistralai/cookbook/blob/main/mistral/rag/basic_RAG.ipynb), also see [this](https://docs.mistral.ai/guides/rag/) website
- the free API key only allows to use Mistral small, not Mistral large

### `langchain/run_locally/rag-locally-on-intel-cpu.ipynb`
- [source](https://github.com/langchain-ai/langchain/blob/master/cookbook/rag-locally-on-intel-cpu.ipynb), see also [this](https://python.langchain.com/docs/how_to/local_llms/) website
- when using the `nomic-embed-text-v1.5` in GGUF format with `llama.cpp`, it changes the context window to 2048 tokens
- mistral large [is not available](https://docs.mistral.ai/getting-started/models/models_overview/#open-models) as .gguf file, I found some [here](https://huggingface.co/bartowski/Mistral-Large-Instruct-2407-GGUF) but it's not the official source. Same with [Llama 4](https://huggingface.co/lmstudio-community/Llama-4-Scout-17B-16E-Instruct-GGUF)


