from config import *
from rag_retriever import use_rag
open_logs("concept_generator")


# README: This script can be used to generate 5 short concepts that respond to the context retrieved by the RAG agent on the knowledge pool.
# Choose between "local" or "openai" mode in config.py

# RAG Parameters
question = "What is the list of building program?"
embeddings_json= "../LLM-Knowledge-Pool-RAG/knowledge_pool/Competition_brief.json"
num_results = 10

def generate_concept(rag_result: str)-> str:
    response = client.chat.completions.create(
        model=completion_model,
        messages=[
            {
                "role": "system",
                "content": """You are an intern at a major architecture firm. 
                       Your goal is to come up with 3 imaginative and very different short concepts for building designs that the jury is happy with. 
                       For each, come up a short paragraph describing the concept in a very poetic and imaginative way.""",
            },
            {
                "role": "user",
                "content": f"""Come up with 5 short concepts for building designs. The concepts should be very different frome each other. 
                Use the following information as a starting point:
                {rag_result}""",
            },
        ],
    )
    return response.choices[0].message.content

# Execute the pipeline
rag_result= use_rag(question, embeddings_json, num_results)
concepts = generate_concept(rag_result)
print(concepts)

close_logs()
