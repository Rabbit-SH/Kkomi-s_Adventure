# TensorFlow 1.x와 호환되도록 설정
try:
    import tensorflow.compat.v1 as tf
except ImportError:
    import tensorflow as tf

import os
import cv2
import numpy as np

from .network import unet_generator
from .guided_filter import guided_filter  # 사용자 정의 가이드 필터 모듈


# 이미지를 재조정하고 크롭하는 함수
def resize_crop(image):
    h, w, c = np.shape(image)
    if min(h, w) > 720:
        if h > w:
            h, w = int(720 * h / w), 720
        else:
            h, w = 720, int(720 * w / h)
    image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
    h, w = (h // 8) * 8, (w // 8) * 8
    image = image[:h, :w, :]
    return image


# 카툰화를 수행하는 함수
def cartoonize(input_path, output_path):
    model_path = "./b_course/model_cartoon/saved_models"  # 모델 경로

    tf.reset_default_graph()  # 그래프 초기화

    input_photo = tf.placeholder(tf.float32, [1, None, None, 3])  # 입력 이미지 플레이스홀더
    network_out = unet_generator(input_photo)  # U-Net 생성자 네트워크
    final_out = guided_filter(input_photo, network_out, r=1, eps=5e-3)  # 가이드 필터 적용

    all_vars = tf.trainable_variables()  # 훈련 가능한 모든 변수
    gene_vars = [var for var in all_vars if "generator" in var.name]  # 생성자 변수
    saver = tf.train.Saver(var_list=gene_vars)  # 생성자 변수를 위한 Saver 객체 생성

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True  # GPU 메모리 할당을 동적으로 설정
    with tf.Session(config=config) as sess:  # 세션 생성
        sess.run(tf.global_variables_initializer())  # 변수 초기화
        saver.restore(sess, tf.train.latest_checkpoint(model_path))  # 체크포인트에서 변수 복원

        try:
            image = cv2.imread(input_path)  # 이미지 읽기
            image = resize_crop(image)  # 이미지 크기 조정 및 크롭
            batch_image = image.astype(np.float32) / 127.5 - 1  # 이미지 전처리
            batch_image = np.expand_dims(batch_image, axis=0)  # 배치 차원 추가
            output = sess.run(
                final_out, feed_dict={input_photo: batch_image}
            )  # 네트워크 실행
            output = (np.squeeze(output) + 1) * 127.5  # 출력 이미지 후처리
            output = np.clip(output, 0, 255).astype(np.uint8)  # 값 범위를 0-255로 조정
            cv2.imwrite(output_path, output)  # 이미지 저장
        except Exception as e:
            print("cartoonize {} failed: {}".format(input_path, e))  # 오류 발생시 출력
