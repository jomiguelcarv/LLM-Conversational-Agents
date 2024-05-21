from config import *
from rag_retriever import use_rag
open_logs("image_caption")


# README: This script creates descriptions out of images

image = "https://media.istockphoto.com/id/490734017/photo/old-factory-building-facade.jpg?s=612x612&w=0&k=20&c=Z5ixfLuF_2mNgkh5SICiPcXvpzBVvuaQqBaUe3SarqQ="

def caption_image(image: str)-> str:
    response = client.chat.completions.create(
        model=vision_model,
        messages=[
                {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"""
                        Begin by generating a comprehensive portrayal of the image, focusing on architectural attributes, aesthetics, material composition, and the ambiance conveyed by the structure. 
                        Delve into specifics such as the facade, windows, and any discernible elements. 
                        """,
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{get_base_64_img(image)}"
                    },
                    },
                ],
                }
            ],
            max_tokens=1000,
    )
    return response.choices[0].message.content


caption = caption_image(image)
print(caption)

close_logs()