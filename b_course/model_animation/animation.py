import os
import argparse

from PIL import Image
import numpy as np

import torch
from torchvision.transforms.functional import to_tensor, to_pil_image
from .model import Generator

# CUDA 설정 비 활성화
torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True


def load_image(image_path):
    img = Image.open(image_path).convert("RGB")

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


# 모델 초기화 및 이미지 변환을 수행하는 함수
def animation(
    input_image,
    output_image,
    checkpoint="./b_course/model_animation/weights/face_paint_512_v2.pt",
    device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
):
    # 모델 초기화
    net = Generator()
    net.load_state_dict(torch.load(checkpoint, map_location=device))
    net.to(device).eval()

    # 이미지 처리
    image = load_image(input_image)
    with torch.no_grad():
        image_tensor = to_tensor(image).unsqueeze(0) * 2 - 1
        out = net(
            image_tensor.to(device), False
        ).cpu()  # upsample_align 매개변수는 기본적으로 False로 설정
        out = out.squeeze(0).clip(-1, 1) * 0.5 + 0.5
        out = to_pil_image(out)
        out.save(output_image)

    print(f"Image converted and saved: {output_image}")
