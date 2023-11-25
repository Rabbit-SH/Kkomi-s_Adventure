import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth
from skimage import io  # 이미지 로딩을 위한 라이브러리

def mean_shift_segmentation(image):
    # 이미지 로드
    image = np.array(image)  # 이미지를 NumPy 배열로 변환
    original_shape = image.shape

    # 이미지를 (n_samples, n_features) 형태의 2D 배열로 변환
    flat_image = np.reshape(image, [-1, 3])

    # Mean Shift를 위한 대역폭(bandwidth) 추정
    # quantile : 데이터 포인터 간 거리 기반으로 추정, 클러스터 생성 방법 (0.1 ~ 0.3)
    # n_samples : 대역폭 추정에 사용되는 샘플 데이터 포인트의 수 지정 (100 ~ 1000)
    bandwidth = estimate_bandwidth(flat_image, quantile=0.1, n_samples=100)

    # Mean Shift 알고리즘 적용
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(flat_image)

    # 각 픽셀에 대해 클러스터 중심을 할당
    segmented_image = ms.cluster_centers_[ms.labels_]

    # 원래 이미지 형태로 재구성
    segmented_image = segmented_image.reshape(original_shape).astype(np.uint8)

    return segmented_image


# 이미지 로드
image_path = 'C:/Users/User/Documents/GitHub/Kkomi-s_Adventure/Backend/Model/stable-diffusion-main/image/test(5).jpg'  # 실제 이미지 경로로 대체
image = io.imread(image_path)

# Mean Shift 세분화 수행
shift_image= mean_shift_segmentation(image)

# 결과 이미지 저장
shift_image.save(image,"color-segmentation.jpg")
