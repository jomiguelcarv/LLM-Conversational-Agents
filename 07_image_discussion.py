#py 3.8.6
from tools import generate_img, review_img, caption_img
from autogen import ConversableAgent
from autogen import register_function
from autogen import GroupChat, GroupChatManager
from config import *

open_logs("image_discussion")

if mode == "local":
    print("Warning: change mode on config.py to openai to run this script")
    exit()
# README: This script creates a conversation where images are generated and reviewed to check if they belong to the original image.
## IMPORTANT: This script only runs in "openai" mode


#First we send an image to a caption agent
#The caption is sent to a diffusion model
#Another agent compares both and scores them
#Create an iterated prompt to improve score
#Repeat image generation...

image = "https://media.istockphoto.com/id/490734017/photo/old-factory-building-facade.jpg?s=612x612&w=0&k=20&c=Z5ixfLuF_2mNgkh5SICiPcXvpzBVvuaQqBaUe3SarqQ="
space_prompt = "the lobby of the hotel"

# Define the agents involved in the conversation


image_generator = ConversableAgent(
    name="Image_Generator",
    system_message = """
    You are a world class AI image prompt engineer and you will be given: an image of a fake building and a text prompt describing an imaginary space inside of that building (either original prompt or the iterated prompt from img reviewer).
    With the information given, you will use generate_img to generate an image of a space inside of that building.
    You will continuously iterate the image based on feedback from img_reviewer until the img_reviewer is satisfied with the result.
    """,
    llm_config = {
        "config_list": gpt4_vision,
        },
    )

# An agent that reviews if images look alike
img_reviewer = ConversableAgent(
    name="Image_Reviewer",
    system_message = """
    You will review both original_image as well as generated_image by the img_generator based on image urls.
    Classify if the interior space in image from img_generator is 95% match of belonging to the original building image.
    Take into consideration the architectural features of the building, like the shape of windows and materials, that should be identical to what is seen from outside.
    If more than 95% match, just return "95% match", if not 95% match, list out the discrepancy
    and generate an interated text prompt for the img generation model to fill the gap of discrepancy.
    """,
    llm_config = {
        "config_list": gpt4_vision,
        # "timeout": 120,
    },
    is_termination_msg = lambda msg: "95% match" in msg["content"].lower(),
)

# An agent that makes an image caption
img_captioner = ConversableAgent(
    name="Image_Captioner",
    system_message = """
    Your goal is to come up with an image prompt describing an interior space inside the building shown in the image.
    Answer in the specific format that is required.
    """,
    llm_config = {
        "config_list": gpt4_vision,
        # "timeout": 120,
    },
    is_termination_msg = lambda msg: "95% match" in msg["content"].lower(),
)

# An agent that decides what agents / tools to call
user_proxy = ConversableAgent(
    name="User",
    llm_config = {
        "config_list": gpt4_vision,
        # "timeout": 120,
    },
    is_termination_msg = lambda msg: msg.get("content") is not None
    and "TERMINATE" in msg["content"],
    human_input_mode = "NEVER",
)

register_function(generate_img,
    caller = image_generator,
    executor = user_proxy,
    name="generate_img",
    description="generate interior space image with ai model based on original building image and text prompt",
)

register_function(review_img,
    caller = img_reviewer,
    executor = user_proxy,
    name="review_img",
    description="compare and review images",
)

register_function(caption_img,
    caller = img_captioner,
    executor = user_proxy,
    name="caption_img",
    description="create a text prompt of the image",
)


group_chat = GroupChat(
    agents=[img_captioner, image_generator, img_reviewer, user_proxy],
    messages = [],
    max_round = 15,
)

group_chat_manager = GroupChatManager(
    groupchat = group_chat,
    llm_config={
        "config_list": gpt4_vision,
    }
)

chat_result= user_proxy.initiate_chats(
    [
        {
            "recipient": group_chat_manager,
            "message": f"""
                **original_building_img**: {image}
                ----
                First, call for caption_img with the original image. 
                Then use the response as the prompt for the image generator.
                Generate a realistic photo of the interior space based on the original building image and base prompt above that pass 100% match from img_reviewer.
                """,
            "summary_method": "reflection_with_llm",
            "summary_args": {"summary_prompt": "Including the latest latest_ai_img_url, as well as original_building_img, latest_prompt"
            },
        },
    ]
)

close_logs()