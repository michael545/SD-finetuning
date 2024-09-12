import json
import requests
import io
import base64
import os
import sys
import random
import argparse
from datetime import datetime
from PIL import Image

url = "http://127.0.0.1:7862" # spremeni na svoj url :7862 ce je 1 instance odprt
imgWidth = 512
imgHeight = 512
restoreFaces = "true"

#ce je empty so vsi modeli, ki so v folderju models
modelList = []

##################################################
# CLI arguments / defaults
##################################################
parser = argparse.ArgumentParser(
    prog='model_sampler.py',
    description='Generate batches of stable diffusion outputs for multiple models to easily compare the same prompt')
parser.add_argument('-p', '--prompt', default='', help='Text prompt to run. Leave blank to load ./prompt.txt file')
parser.add_argument('-n', '--negative-prompt', default='', help='Negative prompt. Leave blank to load ./prompt_neg.txt file')
parser.add_argument('-b', '--batch-size', default='5', help='Number of images to generate per model')
parser.add_argument('-s', '--steps', default='25')
parser.add_argument('-d', '--seed', default='-1', help='Seed to start at, consecutive batch images increment by 1')
parser.add_argument('-H', '--hires', default='false', help='Enable hi-res fix')
parser.add_argument('-D', '--denoise', default='0.7', help='De-noising strength')
parser.add_argument('-c', '--cfg', default='7', help='Config Scale')
args = parser.parse_args()

# nalozi prompt
if args.prompt == '':
    with open(r"prompt.txt", "r") as fileHandle:
        prompt = fileHandle.read()
else:
    prompt = args.prompt

# - prompt
if args.negative_prompt == '':
    with open(r"prompt_neg.txt", "r") as fileHandle:
        prompt_neg = fileHandle.read()
else:
    prompt_neg = args.negative_prompt

# nastavi seed
if int(args.seed) == -1:
    seedNum = random.randrange(sys.maxsize)
else:
    seedNum = int(args.seed)

# Populate model list dynamically if not provided
if len(modelList) == 0:
    response = requests.get(url=f'{url}/sdapi/v1/sd-models')
    print(response)
    for _model in response.json():
        modelList.append({"model": _model['title'], "keywords": ""})

##################################################
# API calli

def pr(msg):
    _time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{_time}] {msg}")

startTime = datetime.now()
for _model in modelList:
    modelName = _model['model']
    modelKeywords = _model['keywords']

    # nastvai model cez API
    option_payload = {
        "sd_model_checkpoint": modelName,
        "CLIP_stop_at_last_layers": 2
    }
    pr(f"Switching to model: {modelName}")
    response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)

    # Payload za generiracijo slik
    payload = {
        "prompt": prompt + ", " + modelKeywords,
        "negative_prompt": prompt_neg,
        "batch_size": int(args.batch_size),
        "steps": int(args.steps),
        "seed": seedNum,
        "enable_hr": args.hires,
        "denoising_strength": float(args.denoise),
        "cfg_scale": float(args.cfg),
        "width": imgWidth,
        "height": imgHeight,
        "restore_faces": restoreFaces,
    }
    pr(f"Generating {payload['batch_size']} images with {payload['steps']} steps.")

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    try:
        r = response.json()
    except ValueError:
        pr("Error: Not a valid JSON response")
        sys.exit(1)

    # shrani v folder poimenovan po modelu
    model_folder = modelName.replace("\\", "_").replace("/", "_")
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)

    for i, image_data in enumerate(r['images']):
        image = Image.open(io.BytesIO(base64.b64decode(image_data.split(",", 1)[0])))
        image.save(f'{model_folder}/image_{i + 1}.png')

    pr(f"Images saved in folder: {model_folder}")

pr("All models processed. Script completed.")
runtime = datetime.now() - startTime
pr(f"Completed in {int(runtime.total_seconds() / 60)} minutes and {int(runtime.total_seconds()) % 60} seconds")
