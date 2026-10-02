from pathlib import Path
from PIL import Image
import torch
from transformers import AutoProcessor, BlipForConditionalGeneration
import streamlit as st


@st.cache_resource
def load_caption_model():

    processor = AutoProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    ).to("cpu")
    model.eval()

    return processor, model



def caption_image(image_input):

    processor, model = load_caption_model()

    if isinstance(image_input, (str, Path)):
        image = Image.open(image_input)
    else:
        image = image_input

    inputs = processor(images=image, return_tensors="pt").to("cpu")

    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=15,
            num_beams=1,
            do_sample=False,
        )

    generated_text = processor.batch_decode(
        generated_ids, skip_special_tokens=True
    )[0].strip()

    return generated_text