
from autogen import ConversableAgent
from config import *
from rag_retriever import use_rag
open_logs("concept_discussion")


# README: This script creates a conversation between an intern (creates concepts) and a jury (asks questions about them)
# Similar to script 2 and 3, but this time the questions are asked dinamically by another agent.

# RAG Parameters
question = "What is the list of building program?"
embeddings_json= "../LLM-Knowledge-Pool-RAG/knowledge_pool/Competition_brief.json"
num_results = 10

# Define the agents involved in the conversation
intern = ConversableAgent(name="intern",
                       description="Creates concepts for building design proposals and answers questions about them",
                       system_message=""" 
                       You are an intern at a major architecture firm. 
                       Your goal is to come up with 3 imaginative and very different short concepts for building designs that the jury is happy with. 
                       For each, come up a short paragraph describing the concept in a very poetic and imaginative way.
                       """,
                       is_termination_msg = lambda msg: msg.get("content") is not None
                        and "100%" in msg["content"],
                       llm_config={
                           "config_list": gpt4_turbo,
                           "temperature": 0.9,
                       },
                       code_execution_config=False,
                       )

jury= ConversableAgent(name="jury",
                       description="Reviews design concepts",
                       system_message="""
                       Your are a jury in the selection panel for an architecture competition and your role is to review design concepts.
                       You will follow this subtasks:
                       1. Think about the concept and make three questions that will expose additional detail about the design and architecture of the concept.
                       2. Classify between 0 and 100% how much the given concept answers your questions clearly and is related to the design context information.
                       You will always ask new questions about the concept to the intern until you are satisfied with the concept.
                       If you are satisfied, simply answer "100%"
                       """,
                       is_termination_msg = lambda msg: msg.get("content") is not None
                        and "100%" in msg["content"],
                        # human_input_mode="ALWAYS",
                       llm_config={
                           "config_list": gpt4_turbo,
                           "temperature": 0.9,
                       })

# Run RAG
rag_result= use_rag(question, embeddings_json, num_results)

# Start the conversation
chat_result= jury.initiate_chats(
    [
        {
            "recipient": intern,
            "message": f"""
                **design context information**: 
                {rag_result}
                ----
                Lets develop an idea for the design. 
                What should be the concepts for the architecture of our building?
                """,
            "summary_method": "reflection_with_llm",
        },
    ]
)

close_logs()