import random
from openai import OpenAI
from keys import *
import requests
import base64
import sys
from datetime import datetime
# Mode
mode = "openai" # "local" or "openai"

# API
local_client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Models
embedding_model = "nomic-ai/nomic-embed-text-v1.5-GGUF"

mistral_8x7b = [
        {
            "model": "cjpais/llava-1.6-mistral-7b-gguf/llava-1.6-mistral-7b.Q6_K.gguf",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
        }
]

mistral_7b = [
        {
            "model": "TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_S.gguf",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
        }
]

nous_capybara_3b = [
        {
            "model": "RichardErkhov/NousResearch_-_Nous-Capybara-3B-V1.9-gguf",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
        }
]

westlake = [
        {
            "model": "TheBloke/WestLake-7B-v2-GGUF",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
            "cache_seed": random.randint(0, 100000),
        }
]

# Notice how this model is not running locally. It uses an OpenAI key.
gpt4_turbo = [
        {
            "model": "gpt-4-turbo-preview",
            "api_key": OPENAI_API_KEY,
            "cache_seed": random.randint(0, 100000),
        }
]

gpt4_vision = [
        {
            "model": "gpt-4-vision-preview",
            "api_key": OPENAI_API_KEY,
            "cache_seed": random.randint(0, 100000),
        }
]

gpt4o = [
        {
            "model": "gpt-4o",
            "api_key": OPENAI_API_KEY,
            "cache_seed": random.randint(0, 100000),
        }
]


command_r = [
        {
            "model": "andrewcanis/c4ai-command-r-v01-GGUF",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
            "cache_seed": random.randint(0, 100000),
        }
]

llama3 = [
        {
            "model": "QuantFactory/Meta-Llama-3-8B-Instruct-GGUF",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
            "cache_seed": random.randint(0, 100000),
        }
]

llava = [
        {
            "model": "xtuner/llava-llama-3-8b-v1_1-gguf",
            'api_key': 'any string here is fine',
            'api_type': 'openai',
            'base_url': "http://localhost:1234/v1",
            "cache_seed": random.randint(0, 100000),
        }
]

# If you download any new models, make sure to add its configuration here. Simply change the "model" name to the correct one.
# myNewModel = [
#         {
#             "model": <the model name that you can find in LM Studio>,
#             'api_key': 'any string here is fine',
#             'api_type': 'openai',
#             'base_url': "http://localhost:1234/v1",
#             "cache_seed": random.randint(0, 100000),
#         }
# ]

# Util functions
def api_mode (mode):
    if mode == "local":
        client = local_client

        # Change the completion/vision model to whatever you want to use
        completion_model = mistral_7b #here
        vision_model = llava #and here

        # Dont change anything below
        agent_completion_model = completion_model
        agent_vision_model = vision_model
        return client, completion_model, vision_model, agent_completion_model, agent_vision_model
    
    elif mode == "openai":
        client = openai_client
        # Change the completion model to whatever you want to use
        completion_model = gpt4_turbo #here
        vision_model = gpt4_vision #and here

        # Dont change anything below
        completion_model = completion_model[0]['model']
        vision_model = vision_model[0]['model']
        agent_completion_model = completion_model
        agent_vision_model = vision_model

        return client, completion_model, vision_model, agent_completion_model, agent_vision_model
    else:
        raise ValueError("Please specify if you want to run local or openai models")

def image_to_base64_data_uri(file_path):
    with open(file_path, "rb") as img_file:
        base64_data = base64.b64encode(img_file.read()).decode('utf-8')
        return f"data:image/png;base64,{base64_data}"
    
def download_image(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")
    
def get_base_64_img(image):
    # Check if the image is a local file or a URL
    if "http" not in image:
        base64_image = base64.b64encode(open(image, "rb").read()).decode('utf-8')
    else:
        response = requests.get(image)
        base64_image = base64.b64encode(response.content).decode('utf-8')

    return base64_image
    
class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, text):
        for file in self.files:
            file.write(text)

    def flush(self):
        for file in self.files:
            file.flush()
    
    def close(self):
        for file in self.files:
            file.close()

def open_logs(script_name):
    sys.dont_write_bytecode = True
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logs = f"logs/{script_name}_{current_datetime}.txt"
    log_file = open(logs, "w")
    sys.stdout = Tee(sys.stdout, log_file)

def close_logs():
    print("Saving logs...")
    sys.stdout.close()
    sys.stdout = sys.__stdout__
client, completion_model, vision_model, agent_completion_model, agent_vision_model = api_mode(mode)