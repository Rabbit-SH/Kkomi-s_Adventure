from PIL import Image
import numpy as np

import torch
from torchvision.transforms.functional import to_tensor, to_pil_image

from model import Generator

# Set torch CUDA configurations if using GPU
torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True

# Function to load and preprocess an image
def load_image(image_path):
    img = Image.open(image_path)

    # Convert the image to RGB format
    img = img.convert("RGB")

    max_size = 1080
    width, height = img.size
    aspect_ratio = width / height

    # Check if the image size is smaller than the max_size
    if width <= max_size and height <= max_size:
        return img  # Return the original image without resizing

    # Resize the image while maintaining aspect ratio
    if width > height:
        new_height = max_size
        new_width = int(max_size * aspect_ratio)
    else:
        new_width = max_size
        new_height = int(max_size / aspect_ratio)

    img = img.resize((new_width, new_height))

    return img

# Function to initialize the model and perform image conversion
def convert(input_image_path, output_image_path, checkpoint='./weights/face_paint_512_v2.pt', device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')):
    # Initialize the model
    net = Generator()
    net.load_state_dict(torch.load(checkpoint, map_location=device))
    net.to(device).eval()

    # Image processing
    image = load_image(input_image_path)
    with torch.no_grad():
        image_tensor = to_tensor(image).unsqueeze(0) * 2 - 1
        # Perform inference on the model
        out = net(image_tensor.to(device), False)  # By default, upsample_align parameter is set to False
        out = out.cpu().squeeze(0).clip(-1, 1) * 0.5 + 0.5
        out = to_pil_image(out)
        out.save(output_image_path)

    print(f"Image converted and saved: {output_image_path}")