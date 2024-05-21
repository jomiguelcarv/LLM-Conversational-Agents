# LLM-Knowledge-Pool-RAG

The repository contains **Part 2** of an LLM Pipeline for Design Exploration.

This project covers different techniques to approach and explore design concepts out of a project Knowledge Pool - checkout [Part 1](https://github.com/jomi13/LLM-Knowledge-Pool-RAG) first.

## Setup
1. Clone this repo into the same parent folder as the repo of **Part 1**.
```bash
git clone https://github.com/jomi13/LLM-Knowledge-Pool-RAG
```
2. Move the `myenv` folder (virtual environment) created in last class to the parent folder of this project. Your folder structure should look like this:
```bash
>parent folder<
    -LLM-Knowlege-Pool-RAG
    -LLM-Conversational-Agents
    -myenv
```
3. Go to Visual Studio Code `settings` and search `python.venvPath`. In the path field, enter the path to the parent folder (e.g. /Users/joao/`parentfolder`).
This will guarantee that anytime the project in open in VSC, it will use python from your virtual environment. Do the same for Part 1 repo.
![alt text](https://i.ibb.co/GVxQFMV/vsc.png)


4. Copy `keys.py` from **Part 1** repo to this project. Grab an API key from [Replicate](https://replicate.com) and add it to `keys.py` like so:

```python
os.environ["REPLICATE_API_TOKEN"] = "your-api-key"
```


## Running

--This project contains 7 examples to be explored by order:
- `01_concept_generator` generates 5 short concepts that respond to the context retrieved by the RAG agent on the knowledge pool.
- `02_concept_tasks` takes one concept you want to investigate further with pre-defined tasks.
- `03_concept_q&a` is similar, but uses questions instead of tasks.
- `04_concept_chaining` is a prompt-chaining script where you can chain your instructions.
- `05_concept_discussion` makes a conversation between an intern (creates concepts) and a jury (asks questions about them).
- `06_image_caption` creates detailed descriptions from images to create caption datasets.
- `07_image_discussion` opens a conversation where images are generated and reviewed to check if they belong to the building on the first image.

**Experiment with these scripts to see how they interact with the LLM. Each one serves as an example. Adapt them to your logic, map out successful chains, and explore different ideas in system prompts. Have fun.**
