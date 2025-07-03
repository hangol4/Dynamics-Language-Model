# Dynamics Language Model

Summer project: building a llama-based large language model specialised in galaxy dynamics by leveraging Retrieval-Augmented Generation (RAG). The main source of information is a well-known textbook 'Galactic Dynamics' by James Binney and Scott Tremaine (Second Edition). To translate PDF files into text, we use [Nougat](https://github.com/facebookresearch/nougat/tree/main) -  a PDF parser that understands LaTeX math and tables. It performs an Optical Character Recognition (OCR) task for processing scientific documents into a markup language. 

## Getting started with Ollama

### My laptop 
(Apple MacBook with M2 chip, macOS Sonoma 14.5)

1. Go to <https://ollama.com/> and install Ollama
2. To run and chat with a selected model, e.g. Llama 3.2:

```bash
ollama run llama3.2
```
Only the first download will take long (depending on the size of the model). If you run `ollama run llama3.2` once again later on, it will be loaded from the memory.

3. Type `/bye` to end a conversation, hit `cmd + C` to interrupt generating.
   
### Cuillin
Adapted from [Mike's fork](https://github.com/michael-petersen/Dynamics-Language-Model/tree/5c41b9ec0f960147380407597075edf569fcdc29/cuillin)

1. Initialisation

First, download ollama for linux
```
curl --fail --show-error --location --progress-bar "https://ollama.com/download/ollama-linux-amd64.tgz" | tar -xzf - -C /home/s2239723
```

2. Obtaining new models 

On the login node,
```
export OLLAMA_MODELS="/cephfs/mpetersen/LLM"
ollama serve &
ollama run llama4:scout
ollama run llama4:maverick
ollama run phi4-mini:latest
```
To simply pull models without running, we can replace `run` with `pull`:
```
ollama pull llama4:maverick
```


3. Production

```
# request resources
srun -n 16 --pty --mem=128GB $SHELL
export OLLAMA_MODELS="/cephfs/mpetersen/LLM"

# set the number of threads for ollama to use
export OLLAMA_NUM_THREADS=16

# worker088, worker094 and worker095 are uniquely suited to take large process jobs
srun -n 64 --pty --mem=256GB $SHELL
export OLLAMA_MODELS="/cephfs/mpetersen/LLM"

# set the number of threads for ollama to use
export OLLAMA_NUM_THREADS=64

# start the server as a background process
ollama serve &

# start the LLM
ollama run llama4:scout
```

The larger models can take quite a while to load: review the memory usage before making plans for a quick session!

### Model Choice
[The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783)
[Ollama GitHub](https://github.com/ollama/ollama?tab=readme-ov-file)

## Getting started with Nougat on Cuillin

## Visualising embeddings

## Other scripts: rag from household objects, ollama example, LangChain Jupyter Notebooks

## Downloading files from the internet
To download files from the internet, you can use the `wget` command in a terminal.
For example, to download a file from a URL, you can use:
```bash
wget https://example.com/file.txt
```
