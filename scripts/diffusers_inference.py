from diffusers import DiffusionPipeline, UNet2DConditionModel
from transformers import CLIPTextModel
import torch


path_to_unet = r"C:\Users\umzg\Documents\Projektil\dreambooth_output\SD_1_5_models\1_no_captions\unet"
path_to_model = r"C:\Users\umzg\Documents\Projektil\dreambooth_output\SD_1_5_models\1_no_captions"
unet = UNet2DConditionModel.from_pretrained(path_to_unet)

# if you have trained with `--args.train_text_encoder` make sure to also load the text encoder
#text_encoder = CLIPTextModel.from_pretrained("path/to/model/checkpoint-100/checkpoint-100/text_encoder")

pipeline = DiffusionPipeline.from_pretrained(path_to_model, unet=unet, dtype=torch.float16,
).to("cuda")

image = pipeline("a painting of a boy", num_inference_steps=50, guidance_scale=7.5).images[0]
image.save("boy_almnck.png")