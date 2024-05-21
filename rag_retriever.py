# This script can run both locally (w/LM Studio) or with an OpenAI key.
import numpy as np
import json
from config import *

# README: This script is only used as a tool for the other scripts (to begin with RAG knowledge).
# Choose between "local" or "openai" mode in config.py

def get_embedding(text, model=embedding_model):
    text = text.replace("\n", " ")
    response = local_client.embeddings.create(input = [text], model=model)
    vector = response.data[0].embedding
    return vector

def similarity(v1, v2):
    return np.dot(v1, v2)

def load_embeddings(embeddings_json):
    with open(embeddings_json, 'r', encoding='utf8') as infile:
        return json.load(infile)
    
def get_vectors(question_vector, index_lib, num_results):
    scores = []
    for vector in index_lib:
        score = similarity(question_vector, vector['vector'])
        scores.append({'content': vector['content'], 'score': score})

    scores.sort(key=lambda x: x['score'], reverse=True)
    best_vectors = scores[0:num_results]
    return best_vectors

def rag_answer(question, prompt, model=completion_model):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", 
             "content": prompt
            },
            {"role": "user", 
             "content": question
            }
        ],
        temperature=0.1,
    )
    return completion.choices[0].message.content

def use_rag(question, embeddings_json, num_results):
    print("Initiating RAG...")
    # Embed our question
    question_vector = get_embedding(question)

    # Load the knowledge embeddings
    index_lib = load_embeddings(embeddings_json)

    # Retrieve the best vectors
    scored_vectors = get_vectors(question_vector, index_lib, num_results)
    scored_contents = [vector['content'] for vector in scored_vectors]
    rag_result = "\n".join(scored_contents)

    # Get answer from rag informed agent
    prompt = f"""Answer the question based on the provided information. 
                You are given the extracted parts of a long document and a question. Provide a direct answer.
                If you don't know the answer, just say "I do not know." Don't make up an answer.
                PROVIDED INFORMATION: """ + rag_result
    
    # prompt = f"""Make a summary of the provided information. 
    #             You are given the extracted parts of a long document. 
    #             PROVIDED INFORMATION:  + {rag_result}
    #             SUMMARY: """

    answer = rag_answer(question, prompt)
    return answer

# text = use_rag("hello")
# print(text)