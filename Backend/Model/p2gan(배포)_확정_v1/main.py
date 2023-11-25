import cv2
import numpy as np
import tensorflow as tf
import time
import model
from sklearn.cluster import KMeans
from PIL import Image
import requests


## 전처리 
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
    segmented_data = kmeans.cluster_centers_.astype('uint8')[labels]

    # 2D 데이터를 원래 이미지 크기로 다시 변환
    segmented_image = segmented_data.reshape((w, h, d))

    return Image.fromarray(segmented_image)

def adjust_brightness_dynamic(image, dark_factor=1.5, bright_factor=1):

    if image.dtype != np.float32:
        image = image.astype(np.float32)

    mean_value = np.mean(image)

    adjusted_image = np.where(image <= mean_value, image / dark_factor, image * bright_factor)

    adjusted_image = np.clip(adjusted_image, 0, 255).astype(np.uint8)

    return adjusted_image

def load_and_preprocess(image_url):

    # url에서 이미지 가져오기
    response = requests.get(image_url)
    
    # 요청이 성공적으로 되는지 확인
    if response.status_code == 200:
        
        # 이미지를 numpy로 변환
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)    
        # 이미지 읽기
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        # 이미지 전처리 단계 수행
        height, width = image.shape[:2]
        
        # 이미지 압축
        # 이미지 크기가 1024x1024보다 작으면 크기 조정 X
        if width > 1024 or height > 1024:
            resized_image = cv2.resize(image, (width // 2, height // 2))
            print("이미지 조정 완료!")
        else:
            resized_image = image
            print("이미지 조정 안했습니다")
            
        # color segmentation 
        segmented_img = segment_image(resized_image, 5)

        # 이미지 numpy 배열로 변환
        if isinstance(segmented_img, Image.Image):
            segmented_img = np.array(segmented_img)

        # 클라해 적용을 위해 gray image로 변경 
        gray_image = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2GRAY)

        # 클라해 적용
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        clahe_image = clahe.apply(gray_image)

        # 이미지 명도 조절
        dynamic_img = adjust_brightness_dynamic(clahe_image)

        # 흑백 이미지를 컬러 형식으로 변환
        color_image = cv2.cvtColor(dynamic_img, cv2.COLOR_GRAY2BGR)

        return color_image
    
    else:
        print("서버 연결 실패", response.status_code)
        return None


## 이미지 스타일 변환
def main(input_url, output_url): 

    preprocessed_img = load_and_preprocess(input_url)

    device = 'cpu'
    batch_size = 1
    feed_size = 1024

    resize_rate = max(preprocessed_img.shape[0], preprocessed_img.shape[1]) / feed_size
    feed_shape_x, feed_shape_y = preprocessed_img.shape[1], preprocessed_img.shape[0]

    feed_shape_y = feed_shape_y / resize_rate
    feed_shape_x = feed_shape_x / resize_rate
    feed_shape_y = int((feed_shape_y // 8) * 8)
    feed_shape_x = int((feed_shape_x // 8) * 8)

    feed_img = np.expand_dims(
        cv2.resize(preprocessed_img, (feed_shape_x, feed_shape_y)), axis=0)
    
    # 모델 checkpoint 파일은 수정될 수 있습니다 .. 
    model_save = "model_save"

    gpu_options = tf.GPUOptions(allow_growth=True)

    with tf.device(device), tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
        input_r = tf.placeholder(tf.float32, shape=[batch_size, feed_shape_y, feed_shape_x, 3], name='inpr')
        g_state = model.build_generator(input_r, name='generator')
        g_var_ls = tf.trainable_variables(scope='generator')
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver(g_var_ls)
        chkpt_fname = tf.train.latest_checkpoint(model_save)

        saver.restore(sess, chkpt_fname)

        noise = np.random.normal(0, 1, size=(batch_size, feed_shape_y, feed_shape_x, 3)).astype(np.float32)
        sess.run(g_state, feed_dict={input_r: noise})

        time_start = time.time()
        render_oup = sess.run(g_state, feed_dict={input_r: feed_img})
        print('Feed shape: %d * %d, network dataflow time: %f'%
            (feed_shape_x, feed_shape_y, time.time()-time_start))
            
    result_img = ((render_oup[0] + 1) / 2) * 255
    result_img = cv2.resize(result_img, (preprocessed_img.shape[1], preprocessed_img.shape[0]))

    cv2.imwrite(output_url, result_img)


## 이것만 실행시키면 됩니다 ,, 
main(input_url, output_url)