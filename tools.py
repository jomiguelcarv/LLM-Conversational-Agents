#py 3.8.6
import replicate
from keys import *
from config import *


#sdXL
def generate_img(original_img: str, prompt: str) -> str:
    output = replicate.run(
    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
    input={
        "width": 768,
        "height": 768,
        "prompt": prompt,
        "refine": "expert_ensemble_refiner",
        "scheduler": "K_EULER",
        "lora_scale": 0.6,
        "num_outputs": 1,
        "guidance_scale": 7.5,
        "apply_watermark": False,
        "high_noise_frac": 0.8,
        "negative_prompt": "",
        "prompt_strength": 0.8,
        "num_inference_steps": 25
    }
)
    return {
        "original_img": original_img,
        "prompt" : prompt,
        "generated_img": output,
    }

#gpt4-v (2 images)
# llava
def review_img(original_img: str, generated_img: str, text_prompt: str)-> str:
    # client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=vision_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                            original text prompt: {text_prompt}
                            1st image is the image of a building, 2nd image is an image of an interior space inside the same building;
                            Please compare and classify if the architectural space in the 2nd img is highly in agreement with the style and feel of the building of the 1st image, around 95% match with the style and characteristics of the building in the 1st image;
                            if more than 95% match, just return "95% match",
                            if less than 95% match, list out the discrepancy.
                            Iterate the original text prompt for the image generation model to fill the gap of discrepancy until you believe the space could indeed belong to the building
                            (just add/tweak details to the original prompt, do not do major structure changes);
                            The iterated prompt should not have references to the original prompt.

                            Return in specific format:
                            MATCH SCORE: xxx,
                            CRITIQUE: xxx,
                            ITERATED PROMPT: xxx
                            """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": original_img,
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": generated_img,
                        },
                    },
                ],
            },
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

#llava
def caption_img(original_img: str, space_prompt: str)-> str:
    # client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=vision_model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""


                            Begin by generating a comprehensive portrayal of the image, focusing on architectural attributes, aesthetics, material composition, and the ambiance conveyed by the structure. 
                            Delve into specifics such as the facade, windows, and any discernible elements. 
                            Subsequently, review the provided description of an interior space: {space_prompt}. 
                            Lastly, amalgamate the earlier crafted description with the interior space portrayal to formulate an image prompt depicting an imaginative scene within the confines of that edifice.

                            Return in specific format:
                            IMAGE PROMPT: xxx,
                            """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": original_img,
                        },
                    },
                ],
            },
        ],
        max_tokens=450,
    )
    return response.choices[0].message.content

                            # First, create a description of the image regarding architectural features, aesthetics, materiality 
                            # and overall feeling of the structure. Pay attention to details of the facade, windows and other visible elements.
                            # After that, read this description of an interior space: {space_prompt}
                            # Finally, use the description you made and the description of the interior space to create 
                            # an image prompt of an imaginary space inside of that building.