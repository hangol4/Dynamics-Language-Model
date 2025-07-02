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
