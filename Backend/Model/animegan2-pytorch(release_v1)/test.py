import os
import argparse

from PIL import Image
import numpy as np

import torch
from torchvision.transforms.functional import to_tensor, to_pil_image

from model import Generator


torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True



def load_image(image_path):
    img = Image.open(image_path).convert("RGB")

    max_size = 1024
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


def test(args):
    device = args.device
    
    net = Generator()
    net.load_state_dict(torch.load(args.checkpoint, map_location="cpu"))
    net.to(device).eval()
    print(f"model loaded: {args.checkpoint}")
    
    os.makedirs(args.output_dir, exist_ok=True)

    for image_name in sorted(os.listdir(args.input_dir)):
        if os.path.splitext(image_name)[-1].lower() not in [".jpg", ".png", ".bmp", ".tiff","jpeg"]:
            continue
        print(image_name)
        image = load_image(os.path.join(args.input_dir, image_name))
        
        name_split=image_name.split(".")
        resize_image=name_split[0]+"_resize."+name_split[1]
        image.save(os.path.join(args.output_dir, resize_image))
                   

        with torch.no_grad():
            image = to_tensor(image).unsqueeze(0) * 2 - 1
            out = net(image.to(device), args.upsample_align).cpu()
            out = out.squeeze(0).clip(-1, 1) * 0.5 + 0.5
            out = to_pil_image(out)

        out.save(os.path.join(args.output_dir, image_name))
        print(f"image saved: {image_name}")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--checkpoint',
        type=str,
        default='./weights/paprika.pt',
    )
    parser.add_argument(
        '--input_dir', 
        type=str, 
        default='./samples/inputs',
    )
    parser.add_argument(
        '--output_dir', 
        type=str, 
        default='./samples/results',
    )
    parser.add_argument(
        '--device',
        type=str,
        default='cuda:0',
    )
    parser.add_argument(
        '--upsample_align',
        type=bool,
        default=False,
        help="Align corners in decoder upsampling layers"
    )
  
    args = parser.parse_args()
    
    test(args)
