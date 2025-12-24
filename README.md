# mini-RAG
mini-RAG is a minimal implementation of Retrieval-Augmented Generation (RAG) using Hugging Face's Transformers and Datasets libraries. It demonstrates how to combine a retriever model with a generator model to enhance text generation with relevant context from a knowledge base.



## Requirements

- Python 3.8+ or higher



#### Installation Python using Miniconda

1. Install Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html).
2. Create a new conda environment:
   ```bash
   conda create -n mini-rag python=3.8 -y
   ```
3. Activate the environment:
   ```bash

    conda activate mini-rag
    ```
4. Install required packages:
   ```bash
    pip install -r requirements.txt
    ```


### (Optional) Setup command line prompt for better readability

Command:
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "

What it does:
Shows username, hostname, and current directory in green with a new line before the prompt.

---

Command:
export PS1="\[\033[34m\]\u@\h\[\033[00m\]:\w\$ "

What it does:
Displays username and hostname in blue followed by the current directory.

---

Command:
export PS1="\[\033[33m\][\t]\[\033[00m\] \w \$ "

What it does:
Adds the current time before the working directory.

---

Command:
export PS1="\w \$ "

What it does:
Minimal prompt showing only the current directory and the `$` symbol.

---

Command:
export PS1="\[\033[31m\]\u@\h:\w\$ \[\033[00m\]"

What it does:
Shows the prompt in red, useful as a warning style when working with sensitive commands.


     
