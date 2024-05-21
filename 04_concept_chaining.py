from config import *
from rag_retriever import use_rag
open_logs("concept_chaining")


# README: This script can be used to chain followup questions automatically in a chain.

# RAG Parameters
question = "What is the list of building program?"
embeddings_json= "../LLM-Knowledge-Pool-RAG/knowledge_pool/Competition_brief.json"
num_results = 10

def brainstorm_brief(rag_result: str)-> str:
    response = client.chat.completions.create(
        model=completion_model,
        messages=[
            {
                "role": "system",
                "content":
                       "You are a world famous architect and you are going to enter an architecture competition. You are creative and poetic in your responses. You are very knowledgable of design and architecture theory",
            },
            {
                "role": "user",
                "content": f""" ###Competition brief### : {rag_result}
                Given your own experienced interpretation, what do you think about the challenge?
                What would be your approach and concept for the building design in order to win the competition?
                What would you name your design?
                Focus on the characteristics of form, facades, materials, relationship to the place, etc.
                """,
            },
        ],
    )
    return response.choices[0].message.content

def conceptualize_programe(brainstorm: str)-> str:
    response = client.chat.completions.create(
        model=completion_model,
        messages=[
            {
                "role": "system",
                "content":
                       "You are a world famous architect and you are going to enter an architecture competition. You are creative and poetic in your responses. You are very knowledgable of design and architecture theory. Answer in a list format",
            },
            {
                "role": "user",
                "content": f""" 
                After reading through the Concept Guidelines provided below, what are the names of the spaces you are going to design?
                Pretend that you are a visitor. What would you see and feel in each of the spaces?
                Focus on the characteristics of form, facades, materials, relationship to the place, etc.
                Answer
                ###Concept Guidelines### : {brainstorm}
                """,
            },
        ],
    )
    return response.choices[0].message.content

# antes, uma completion so a pedir o nome do edificio
def make_prompt(programe: str)-> str:
    response = client.chat.completions.create(
        model=completion_model,
        messages=[
            {
                "role": "system",
                "content":
                       "You are a paiting critique that needs to come up with prompts that descibe what can be seen in a picture. Answer in the required format.",
            },
            {
                "role": "user",
                "content": f""" 
                Make a prompt for each space provided in the ###Descriptions### list.
                Your prompts should follow a structure: mentioning the broader characteristics of the space, then the specifics of the space.
                Here are some examples:
                Description: Functional Radial Wings: These extensions house distinct areas such as dining halls, lodging facilities, spas or recreational spaces - each designed to meet specific needs of visitors during their skiing adventure while maintaining visual connections with the central hub and surrounding landscape.
                Prompt: The radial shaped wings of the Ice-cabin hotel host many different facilities, letting the skiing adventure finish in a place of visual connections with the central hub and surrounding landscape.
                Description: Native Landscaping and Pathways: These initiatives merge seamlessly into the existing terrain around the building, reinforcing its connection to Iceland's wilderness. Carefully curated native flora serves as a living boundary while lava rock pathways lead directly from skiing gates to our retreat, further immersing guests in nature's embrace.
                Prompt: The Ice-cabin hotel reinforces its connection to Iceland's wilderness with lava rock pathways leading directly from skiing gates of the retreat.
                
                Other descriptions:
                ###Descriptions### : {programe}
                """,
            },
        ],
    )
    return response.choices[0].message.content

# def get_name(brainstorm: str)-> str:
#     response = client.chat.completions.create(
#         model=completion_model,
#         messages=[
#             {
#                 "role": "system",
#                 "content":
#                        "YAnswer in the required format.",
#             },
#             {
#                 "role": "user",
#                 "content": f""" 
#                 {brainstorm}
#                 Reply only the name itself, and nothing else.
#                 QUESTION:What is the name of the building present in the above text?
#                 ANSWER:
#                 """,
#             },
#         ],
#     )
#     return response.choices[0].message.content
# # depois, esta funcao
# def style_prompt(building_name, prompt):
#     new_prompts = []
#     entries = prompt.split('\n\n')
#     for entry in entries:
#         new_entry =  f"{building_name} - {entry.strip()}"
#         new_prompts.append(new_entry)

#     return new_prompts
    


# Execute the pipeline
rag_result = use_rag(question, embeddings_json, num_results)
print("###RAG RESULT###")
print(rag_result)
print("________________")

brainstorm = brainstorm_brief(rag_result)
print("###BRAINSTORM###")
print(brainstorm)
print("________________")

conceptualize = conceptualize_programe(brainstorm)
print("###CONCEPTUALIZE###")
print(conceptualize)
print("________________")

print("###PROMPTS###")
prompts = make_prompt(conceptualize)
print(prompts)
print("________________")

# name = get_name(brainstorm)
# print("###OTHERS###")
# print(name)
# fin = style_prompt(name, prompts)
# print(fin)

close_logs()