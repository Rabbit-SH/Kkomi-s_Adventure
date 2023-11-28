import cv2
import numpy as np
import tensorflow as tf
from sklearn.cluster import KMeans
from PIL import Image
import torchvision.models as models
import torchvision.transforms as transforms
import torch

slim = tf.contrib.slim

def _fixed_padding(inputs, kernel_size, rate=1):
    kernel_size_effective = [
        kernel_size[0] + (kernel_size[0] - 1) * (rate - 1),
        kernel_size[0] + (kernel_size[0] - 1) * (rate - 1),
    ]
    pad_total = [kernel_size_effective[0] - 1, kernel_size_effective[1] - 1]
    pad_beg = [pad_total[0] // 2, pad_total[1] // 2]
    pad_end = [pad_total[0] - pad_beg[0], pad_total[1] - pad_beg[1]]
    padded_inputs = tf.pad(
        inputs,
        [[0, 0], [pad_beg[0], pad_end[0]], [pad_beg[1], pad_end[1]], [0, 0]],
        mode="SYMMETRIC",
    )
    return padded_inputs

g_encoder_cfg = {
    "l_num": 3,
    "l0_c": 32,
    "l0_k": 3,
    "l0_s": 2,  
    "l1_c": 64,
    "l1_k": 3,
    "l1_s": 2,  
    "l2_c": 128,
    "l2_k": 3,
    "l2_s": 2,  
}

g_residual_cfg = {"l_num": 1, "c": 128, "k": 3}

g_decoder_cfg = {
    "l_num": 3,
    "l0_c": 64,
    "l0_k": 3,
    "l0_s": 2, 
    "l1_c": 32,
    "l1_k": 3,
    "l1_s": 2, 
    "l2_c": 16,
    "l2_k": 3,
    "l2_s": 2,
}

g_skip_conn_cfg = {"l_num": 2}


def build_generator(inp, name="generator", reuse=tf.compat.v1.AUTO_REUSE):
    g_state = inp  # No prep
    with tf.compat.v1.variable_scope(name, reuse=reuse):
        cfg = g_encoder_cfg
        skip_conn = []
        with slim.arg_scope(
            [slim.conv2d, slim.separable_conv2d],
            activation_fn=tf.nn.relu,
            normalizer_fn=slim.instance_norm,
            padding="VALID",
        ):
            for index in range(cfg["l_num"]):
                g_state = _fixed_padding(g_state, [cfg["l%d_k" % index]])
                g_state = slim.separable_conv2d(
                    g_state,
                    None,
                    [cfg["l%d_k" % index], cfg["l%d_k" % index]],
                    depth_multiplier=1,
                    stride=cfg["l%d_s" % index],
                    scope="enc_%d_dw" % index,
                )
                g_state = slim.conv2d(
                    g_state,
                    cfg["l%d_c" % index],
                    [1, 1],
                    stride=1,
                    scope="enc_%d_pw" % index,
                )
                skip_conn.append(g_state)

        cfg = g_residual_cfg
        with slim.arg_scope(
            [slim.conv2d, slim.separable_conv2d],
            activation_fn=tf.nn.relu,
            normalizer_fn=slim.instance_norm,
            padding="VALID",
        ):
            for index in range(cfg["l_num"]):
                res_g = g_state
                g_state = _fixed_padding(g_state, [cfg["k"]])
                g_state = slim.separable_conv2d(
                    g_state,
                    None,
                    [cfg["k"], cfg["k"]],
                    depth_multiplier=1,
                    stride=1,
                    scope="res_%d_dw" % index,
                )
                g_state = slim.conv2d(
                    g_state,
                    cfg["c"],
                    [1, 1],
                    stride=1,
                    activation_fn=None,
                    scope="res_%d_pw" % index,
                )
                g_state = tf.nn.relu(g_state + res_g)

        cfg = g_decoder_cfg
        with slim.arg_scope(
            [slim.conv2d, slim.separable_conv2d],
            activation_fn=None,
            normalizer_fn=slim.instance_norm,
            padding="VALID",
        ):
            for index in range(cfg["l_num"]):
                g_state = tf.image.resize(
                    g_state,
                    (g_state.shape[1] * 2, g_state.shape[2] * 2),
                    method=tf.image.ResizeMethod.NEAREST_NEIGHBOR,
                )
                g_state = _fixed_padding(g_state, [cfg["l%d_k" % index]])
                g_state = slim.separable_conv2d(
                    g_state,
                    None,
                    [cfg["l%d_k" % index], cfg["l%d_k" % index]],
                    depth_multiplier=1,
                    stride=1,
                    scope="dec_%d_dw" % index,
                )
                g_state = slim.conv2d(
                    g_state,
                    cfg["l%d_c" % index],
                    [1, 1],
                    stride=1,
                    scope="dec_%d_pw" % index,
                )
                # sc = slim.conv2d(skip_conn[?], 128, [1, 1], stride=1, scope='sc')
                if index < g_skip_conn_cfg["l_num"]:
                    g_state = tf.nn.relu(
                        g_state + skip_conn[g_skip_conn_cfg["l_num"] - index - 1]
                    )
                else:
                    g_state = tf.nn.relu(g_state)
        g_state = _fixed_padding(g_state, [3])
        g_state = slim.conv2d(
            g_state,
            3,
            [3, 3],
            stride=1,
            padding="VALID",
            activation_fn=tf.nn.tanh,
            normalizer_fn=None,
            scope="output",
        )
    return g_state

# segmentation 코드 추가
def segment_person(image_path):
    net = models.segmentation.fcn_resnet101(pretrained=True)
    net.eval()
    input_image = Image.open(image_path)
    input_image = input_image.resize((1024, 1024))
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)
    with torch.no_grad():
        prediction = net(input_batch)['out']
    output_predictions = prediction.squeeze().cpu().numpy()
    predicted_class = np.argmax(output_predictions, axis=0)
    human_mask = (predicted_class == 15).astype(np.uint8)
    return human_mask


def open_img(img_path):
	img = cv2.imread(img_path)
	img = (img / 255.0 - 0.5) * 2.0
	return img

def segment_image(image, k=3):
    # 이미지를 NumPy 배열로 변환
    data = np.array(image)

    # 이미지 데이터를 2D로 변환 (각 픽셀은 RGB 색상을 가짐)
    w, h, d = data.shape
    data = data.reshape((w * h, d))

    # KMeans 클러스터링
    kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
    labels = kmeans.predict(data)

    # 클러스터링 결과에 따라 색상 재할당
    segmented_data = kmeans.cluster_centers_.astype("uint8")[labels]

    # 2D 데이터를 원래 이미지 크기로 다시 변환
    segmented_image = segmented_data.reshape((w, h, d))

    return Image.fromarray(segmented_image)


def adjust_brightness_dynamic(image, dark_factor=1.5, bright_factor=1):
    if image.dtype != np.float32:
        image = image.astype(np.float32)

    mean_value = np.mean(image)

    adjusted_image = np.where(
        image <= mean_value, image / dark_factor, image * bright_factor
    )

    adjusted_image = np.clip(adjusted_image, 0, 255).astype(np.uint8)

    return adjusted_image


def load_and_preprocess(image_path):
    # 이미지 읽어오기
    image = cv2.imread(image_path)

    # 이미지 크기 확인
    height, width = image.shape[:2]

    # 이미지 크기를 10241024x1024로 조정
    new_width = 1024
    new_height = 1024
    resized_image = cv2.resize(image, (new_width, new_height))

    # color segmentation
    segmented_img = segment_image(resized_image, 5)

    # numpy 오류 해결
    if isinstance(segmented_img, Image.Image):
        segmented_img = np.array(segmented_img)

    # 그레이스케일로 변경
    gray_image = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2GRAY)

    # 클라해 수행
    # Adaptive Histogram Equalization 적용
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    clahe_image = clahe.apply(gray_image)

    # 픽셀 조절
    dynamic_img = adjust_brightness_dynamic(clahe_image)

    dynamic_img = cv2.cvtColor(dynamic_img, cv2.COLOR_GRAY2BGR)

    return dynamic_img


## 이미지 스타일 변환
def soomuk(input_path, output_path):

    preprocessed_img = load_and_preprocess(input_path)

    # preprocessed_img = cv2.imread(input_path)

    device = "cpu"
    batch_size = 1
    feed_size = 1024

    resize_rate = max(preprocessed_img.shape[0], preprocessed_img.shape[1]) / feed_size
    feed_shape_x, feed_shape_y = preprocessed_img.shape[1], preprocessed_img.shape[0]

    feed_shape_y = feed_shape_y / resize_rate
    feed_shape_x = feed_shape_x / resize_rate
    feed_shape_y = int((feed_shape_y // 8) * 8)
    feed_shape_x = int((feed_shape_x // 8) * 8)

    feed_img = np.expand_dims(
        cv2.resize(preprocessed_img, (feed_shape_x, feed_shape_y)), axis=0
    )

    # 수정 부탁 
    model_save = "model_save"
    tf.reset_default_graph() 

    gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)

    with tf.device(device), tf.compat.v1.Session( # 수정 부분 
        config=tf.compat.v1.ConfigProto(gpu_options=gpu_options)
    ) as sess:
        input_r = tf.compat.v1.placeholder(
            tf.float32, shape=[batch_size, feed_shape_y, feed_shape_x, 3], name="inpr"
        )
        g_state = build_generator(input_r, name="generator")
        g_var_ls =  tf.compat.v1.trainable_variables(scope="generator")
        sess.run(tf.compat.v1.global_variables_initializer())
        saver = tf.compat.v1.train.Saver(g_var_ls)
        chkpt_fname = tf.train.latest_checkpoint(model_save)

        saver.restore(sess, chkpt_fname)

        noise = np.random.normal(
            0, 1, size=(batch_size, feed_shape_y, feed_shape_x, 3)
        ).astype(np.float32)
        sess.run(g_state, feed_dict={input_r: noise})

        render_oup = sess.run(g_state, feed_dict={input_r: feed_img})

    result_img = ((render_oup[0] + 1) / 2) * 255
    result_img = cv2.resize(
        result_img, (preprocessed_img.shape[1], preprocessed_img.shape[0])
    )

    cv2.imwrite(output_path, result_img)


## 이미지 스타일 변환
def seg_soomuk(input_path, output_path):
    
    content = open_img(input_path)

    content = cv2.resize(content, (1024, 1024))


    human_mask = segment_person(input_path)
    preprocessed_img = load_and_preprocess(input_path)

    # preprocessed_img = cv2.imread(input_path)

    device = "cpu"
    batch_size = 1
    feed_size = 1024

    resize_rate = max(preprocessed_img.shape[0], preprocessed_img.shape[1]) / feed_size
    feed_shape_x, feed_shape_y = preprocessed_img.shape[1], preprocessed_img.shape[0]

    feed_shape_y = feed_shape_y / resize_rate
    feed_shape_x = feed_shape_x / resize_rate
    feed_shape_y = int((feed_shape_y // 8) * 8)
    feed_shape_x = int((feed_shape_x // 8) * 8)

    feed_img = np.expand_dims(
        cv2.resize(preprocessed_img, (feed_shape_x, feed_shape_y)), axis=0
    )

    # 수정 부탁 
    model_save = "model_save"
    tf.reset_default_graph() 

    gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)

    with tf.device(device), tf.compat.v1.Session( # 수정 부분 
        config=tf.compat.v1.ConfigProto(gpu_options=gpu_options)
    ) as sess:
        input_r = tf.compat.v1.placeholder(
            tf.float32, shape=[batch_size, feed_shape_y, feed_shape_x, 3], name="inpr"
        )
        g_state = build_generator(input_r, name="generator")
        g_var_ls =  tf.compat.v1.trainable_variables(scope="generator")
        sess.run(tf.compat.v1.global_variables_initializer())
        saver = tf.compat.v1.train.Saver(g_var_ls)
        chkpt_fname = tf.train.latest_checkpoint(model_save)

        saver.restore(sess, chkpt_fname)

        noise = np.random.normal(
            0, 1, size=(batch_size, feed_shape_y, feed_shape_x, 3)
        ).astype(np.float32)
        sess.run(g_state, feed_dict={input_r: noise})

        render_oup = sess.run(g_state, feed_dict={input_r: feed_img})

    result_img = ((render_oup[0] + 1) / 2) * 255
    result_img = cv2.resize(
        result_img, (preprocessed_img.shape[1], preprocessed_img.shape[0])
    )

# 원본사진(content) 는 -1 ~ 1 정규화 값을 가짐
    background_image = content.copy() 
	# 배경 영역에 스타일 적용된 이미지를 만듭니다.  이 과정에서 background_image 픽셀값이 output 픽셀 범위에 의해 정규화 해제
    background_image[human_mask == 0] = result_img[human_mask == 0]  
	# 최종 결과물에서 원본 사진을 보려면 정규화 해제 필요
    final_ouput = (content + 1) * 127.5
    final_ouput[human_mask == 0] = background_image[human_mask == 0]  # 사람이 아닌 부분에 배경 이미지를 합칩니다.



    cv2.imwrite(output_path, final_ouput)


## 이것만 실행시키면 됩니다 ,,
# soomuk("33.jpg", "result33.jpg")


seg_soomuk("22.jpg", "result3.jpg")