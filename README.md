# Dynamics Language Model

Summer project: building a llama-based large language model specialised in galaxy dynamics by leveraging Retrieval-Augmented Generation (RAG). The main source of information is a well-known textbook 'Galactic Dynamics' by James Binney and Scott Tremaine (Second Edition). To translate PDF files into text, we use [Nougat](https://github.com/facebookresearch/nougat/tree/main) -  a PDF parser that understands LaTeX math and tables. It performs an Optical Character Recognition (OCR) task for processing scientific documents into a markup language. 

## Table of Contents
- [Dynamics Language Model](#dynamics-language-model)
- [Table of Contents](#table-of-contents)
- [Getting started with Ollama](#getting-started-with-ollama)
    - [My laptop](#my-laptop)
    - [Cuillin](#cuillin)
    - [Model file](#model-file)
    - [Downloading models from the internet](#downloading-models-from-the-internet)
    - [Model Choice](#model-choice)
- [Getting started with Nougat on Cuillin](#getting-started-with-nougat-on-cuillin)
- [Visualising embeddings](#visualising-embeddings)
- [Other scripts](#other-scripts)

## Getting started with Ollama

### My laptop 
(Apple MacBook with M2 chip, macOS Sonoma 14.5)

1. Initialisation

    Go to <https://ollama.com/> and install Ollama

2. Usage

    To run and chat with a selected model, e.g. Llama 3.2:

    ```bash
    ollama run llama3.2
    ```
    Only the first download will take long (depending on the size of the model). If you run `ollama run llama3.2` once again later on, it will be loaded from the memory.

3. Exiting

    Type `/bye` to end a conversation, hit `cmd + C` / `ctrl + C` to interrupt generating.
   
### Cuillin
Adapted from [Mike's fork](https://github.com/michael-petersen/Dynamics-Language-Model/tree/5c41b9ec0f960147380407597075edf569fcdc29/cuillin)

1. Initialisation

    First, download ollama for linux
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

A model file is the blueprint to create and share models with Ollama. It can be used to control the model's hyperparameters such as temperature and size of the context window and to set the system prompt. 

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
2. To download file to your local machine via terminal, use the `wget` command:
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
- [The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783) - academic paper presenting the Llama 3 set of foundation models, including training preocedures, architecture and performance benchmarks,
- [The Llama 4 herd](https://ai.meta.com/blog/llama-4-multimodal-intelligence/) - release blog post by Meta AI,
- [Model library](https://ollama.com/library) on Ollama's website - a list of available models with download instructions and descriptions, containing information such as model size, context window size, and input formats (text, image, audio). See shorter summary of the most popular models on [Ollama GitHub](https://github.com/ollama/ollama?tab=readme-ov-file#model-library),
- [AstroMLab 1: Who Wins Astronomy Jeopardy!?](https://doi.org/10.48550/arXiv.2407.1119) - authors of this paper compared various large language models using the first astronomy-specific benchmarking dataset, with the division into proprietary and open-weights models. Find more up-to-date comparison on [AstroMLab's Hugging Face](https://huggingface.co/AstroMLab),
- online benchmark leaderbords such as [LibeBench](https://livebench.ai/#/), [Vellum Leaderboard](https://www.vellum.ai/open-llm-leaderboard) and [Artificial Analysys Leaderboard](https://artificialanalysis.ai/leaderboards/models)- these compare skills such as math comprehension, reasoning and coding.

Considerations:
- size: you should have at least 8 GB of RAM available to run the 7B models, 16 GB to run the 13B models, and 32 GB to run the 33B models,
- context window size: the larger the context window, the more information the model can use to generate the next token, but it might require more memory and make it slower,
- availability of API keys: some RAG scripts (e.g. many examples from LangChain) require an API key to access the model, which is not always available ([you have to be in the US](https://llama.developer.meta.com/join_waitlist) to get a key for all Meta models). You can get a Mistral AI key for free [here](https://docs.mistral.ai/getting-started/quickstart/) but it does not always work, or try [these](https://github.com/langchain-ai/langchain/tree/master/cookbook) example notebooks from LangChain on running open source LLMs locally on Intel CPU (I don't think they require API keys but I might be wrong).

## Getting started with Nougat on Cuillin

## Visualising embeddings

## Other scripts

rag from household objects, ollama example, LangChain Jupyter Notebooks

