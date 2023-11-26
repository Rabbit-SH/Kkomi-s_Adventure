import cv2
import numpy as np
import tensorflow as tf
import util
import time
import model
import os
from argparse import ArgumentParser


#배치크기 읽어오기
imbatch_read     = util.imbatch_read
# RGB 확인 후 0~255 조정
img_write        = util.img_write
# 미니배치로 학습할떄 사용하는 리스트
pickup_list      = util.pickup_list
# json 형식으로 반환
ls_files_to_json = util.ls_files_to_json
# 사람 segmentation
segment_person   = util.segment_person

build_generator  = model.build_generator

def build_parser():
	parser = ArgumentParser()
	parser.add_argument('--model', type=str,
					dest='model',
					help='dir to load model',
					required=True)
	parser.add_argument('--inp', type=str,
					dest='inp_path',
					help='input content images',
					required=True)
	parser.add_argument('--oup', type=str,
					dest='out_path',
					help='output stylized images',
					required=True)
	parser.add_argument('--bs', type=int,
					dest='batch_size',
					default=1,
					help='batch size',
					required=False)
	parser.add_argument('--size', type=int,
					dest='net_size',
					default=256,
					help='network feed size',
					required=False)
	parser.add_argument('--cpu', type=str,
					dest='use_cpu',
					default='false',
					help='processing by cpu',
					required=False)
	parser.add_argument('--noise', type=float,
					dest='noise',
					default=0.0,
					help='noise',
					required=False)
	return parser




args = build_parser().parse_args()

MODEL_SAVE_PATH = args.model

BATCH_SIZE  = args.batch_size
# 콘텐츠 이미지 변환 사이즈
FEED_SIZE   = args.net_size
IMGSRC_PATH = args.inp_path
NOISE_RATE  = args.noise

if (not os.path.isdir(args.out_path)):
	os.makedirs(args.out_path)

DEVICE = ''
if args.use_cpu.upper()=='TRUE':
	DEVICE = '/cpu:0'

# content 범위 -1 ~ 1
content = util.open_img(IMGSRC_PATH)
human_mask = segment_person(IMGSRC_PATH)

#FEED_SIZE : 변환 사이즈.  resize_rate 크기 조절하여 사용
resize_rate = max(content.shape[0], content.shape[1]) / FEED_SIZE
feed_shape_x, feed_shape_y = content.shape[1], content.shape[0]

feed_shape_y = feed_shape_y / resize_rate
feed_shape_x = feed_shape_x / resize_rate

# 8의 배수로 조절 - 2의 거듭제곱으로 해야 연산 속도 향상
feed_shape_y = int((feed_shape_y // 8) * 8)
feed_shape_x = int((feed_shape_x // 8) * 8)

# 모델 입력 일관성 유지 (성능 효율성 향상이 일어난다네요)
feed_img = np.expand_dims(
		cv2.resize(content, (feed_shape_x, feed_shape_y)),
	axis=0)

# 변환 단계 추후 공부
gpu_options = tf.GPUOptions(allow_growth=True)
with tf.device(DEVICE), tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
	input_r = tf.placeholder(tf.float32, shape=[BATCH_SIZE, feed_shape_y, feed_shape_x, 3], name='inpr')
	g_state = build_generator(input_r, name='generator')
	g_var_ls = tf.trainable_variables(scope='generator')
	sess.run(tf.global_variables_initializer())
	saver = tf.train.Saver(g_var_ls)
	chkpt_fname = tf.train.latest_checkpoint(MODEL_SAVE_PATH)
	saver.restore(sess, chkpt_fname)
	# Warm up network and test...
	noise = np.random.normal(0, 1, size=(BATCH_SIZE, feed_shape_y, feed_shape_x, 3)).astype(np.float32)
	sess.run(g_state, feed_dict={input_r: noise})
	# Begin...
	if NOISE_RATE != 0:
		noise = np.random.normal(0, 1,
			size=(BATCH_SIZE, feed_shape_y, feed_shape_x, 3)).astype(np.float32)
		feed_img = feed_img + noise * NOISE_RATE 
	time_start = time.time()
	render_oup = sess.run(g_state, feed_dict={input_r: feed_img})
	print('Feed shape: %d * %d, network dataflow time: %f'%
		(feed_shape_x, feed_shape_y, time.time()-time_start))


	output = ((render_oup[0] + 1) / 2) * 255
	output = cv2.resize(output, (content.shape[1], content.shape[0]))


	
	# 원본사진(content) 는 -1 ~ 1 정규화 값을 가짐
	background_image = content.copy() 
	# 배경 영역에 스타일 적용된 이미지를 만듭니다.  이 과정에서 background_image 픽셀값이 output 픽셀 범위에 의해 정규화 해제
	background_image[human_mask == 0] = output[human_mask == 0]  

	# 최종 결과물에서 원본 사진을 보려면 정규화 해제 필요
	final_ouput = (content + 1) * 127.5
	final_ouput[human_mask == 0] = background_image[human_mask == 0]  # 사람이 아닌 부분에 배경 이미지를 합칩니다.
	
	cv2.imwrite(args.out_path + '/stylized.jpg', final_ouput)

