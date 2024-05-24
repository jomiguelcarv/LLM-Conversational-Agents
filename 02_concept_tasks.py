from config import *
open_logs("concept_tasks")


# README: This script uses one concept you want to investigate further.
# Choose between "local" or "openai" mode in config.py

concept = """**Concept 1: The Whispering Grove**
In the heart of the bustling city, a tranquil haven unfolds - The Whispering Grove. 
This brutalist edifice takes inspiration from the organic world, weaving together nature and urbanity in an harmonious dance. 
Its facade, etched with intricate patterns reminiscent of tree bark, invites the curious passerby to explore its depths. 
A labyrinth of concrete columns, resembling mighty trunks, support a canopy of glass leaves, filtering sunlight into the building's core. 
Here, within the sanctuary, functional zones are neatly arranged like blossoms on branches, providing the necessary nourishment for productivity and creativity to thrive."""

tasks = """ 1. First, list out the names of all interior spaces in this building.
            2. Second, explain how they are connected and one can move from space to space across the building.
            3. Third, describe what a visitor will see and find inside each of the spaces."""  

def question_concept(tasks: str, concept: str)-> str:
    # client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=completion_model,
        messages=[
            {
                "role": "system",
                "content": """ 
                       You are a world renowed architect. You answer questions about building design concepts.""",
            },
            {
                "role": "user",
                "content": 
                        f"""You are given a set of tasks and a brief summaries of a building design concept.
                        Be imaginative and creative in your answers:
                        #CONCEPTS#: {concept}
                        #TASKS#: {tasks}
                        """,
            },
        ],
        #max_tokens=450,
    )
    return response.choices[0].message.content


answer = question_concept(tasks, concept)
print(answer)

close_logs()


