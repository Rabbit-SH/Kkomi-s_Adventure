import os
import argparse

from PIL import Image, ExifTags
import numpy as np

import torch
from torchvision.transforms.functional import to_tensor, to_pil_image
from .model import Generator

# Disable CUDA settings
torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True


def load_image(image_path):
    img = Image.open(image_path)

    # Checking Exif data to determine rotation angle
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())

        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass  # Unable to find or handle Exif data

    # Resizing the image
    max_size = 1080
    width, height = img.size
    aspect_ratio = width / height

    if width > height:
        new_height = max_size
        new_width = int(max_size * aspect_ratio)
    else:
        new_width = max_size
        new_height = int(max_size / aspect_ratio)

    img = img.resize((new_width, new_height))

    return img


# Function to initialize the model and perform image transformation
def animation(
    input_image,
    output_image,
    checkpoint="./b_course/model_animation/weights/face_paint_512_v2.pt",
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
):
    # Initializing the model
    net = Generator()
    net.load_state_dict(torch.load(checkpoint, map_location=device))
    net.to(device).eval()

    # Image processing
    image = load_image(input_image)
    with torch.no_grad():
        image_tensor = to_tensor(image).unsqueeze(0) * 2 - 1
        out = net(
            image_tensor.to(device), False
        ).cpu()  # The upsample_align parameter is set to False by default
        out = out.squeeze(0).clip(-1, 1) * 0.5 + 0.5
        out = to_pil_image(out)
        out.save(output_image)
     
    print(f"Image converted and saved: {output_image}")