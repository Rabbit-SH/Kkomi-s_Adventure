import cv2
# GAN 모델 생성자, 식별자 모델 
import model
import os
import random
import tensorflow as tf
# 함수 정의
import util
# vgg16 모델
import vgg16part
# 파일 실행시 필요한 값들을 정의
from argparse import ArgumentParser

# json 형식으로 반환
ls_files_to_json = util.ls_files_to_json
# 패치 단위로 분할
make_input_batch = util.make_input_batch # Patch Permutation
open_img         = util.open_img
# 미니배치로 학습할떄 사용하는 리스트
pickup_list      = util.pickup_list
# 이미지 형태의 파일들을 배치형태(여러개 사진을 하나로)로 불러오기 
images_batch     = util.images_batch
# json 설정파일 읽어오는 코드
load_cfg         = util.load_cfg

build_generator     = model.build_generator
build_discriminator = model.build_discriminator

# 옵션 추가
def build_parser():
	# 객체생성
	parser = ArgumentParser()
	parser.add_argument('--model', type=str,
					# 변수명 지정
					dest='model_save',
					# 걍 인자 설명
					help='dir to save or load model',
					# 반드시 필요한지 여부
					required=True)
	parser.add_argument('--style', type=str,
					dest='style_path',
					help='style image',
					required=True)
	parser.add_argument('--dataset', type=str,
					dest='train_set',
					help='path to dataset',
					required=True)
	# 설정파일 (반복수, 체코포인트 등)
	parser.add_argument('--config', type=str,
					dest='cfg',
					default='cfg.json',
					help='path to config file',
					required=False)
	# 최대 저장 모델의 개수
	parser.add_argument('--max_to_keep', type=int,
					dest='max_to_keep',
					default=10,
					help='tf.train.Saver max_to_keep',
					required=False)
	parser.add_argument('--bs', type=int,
					dest='batch_size',
					default=8,
					help='batch size',
					required=False)
	parser.add_argument('--ps', type=int,
					dest='patch_size',
					default=9,
					help='patch size',
					required=False)
	parser.add_argument('--lambda', type=float,
					dest='arg_lambda',
					default=5.0e-6,
					help='lambda',
					required=False)
	return parser

# 해당 변수에 옵션과 값들이 파싱되어 저장. 커맨드라인 입력 가능화
args = build_parser().parse_args()

# 패치크기 : 입력 픽셀
supported_patch_size = {
	9 : 216,
	12: 240,
	15: 240,
	16: 256,
	32: 1024
}

# 패치사이즈 지원여부 확인
if not args.patch_size in supported_patch_size:
	exit("patch size not supported")

PATCH_SIZE   = args.patch_size
# 판별자 입력 이미지 크기
PSI_D_SIZE   = supported_patch_size[args.patch_size]
# 생성기 출력 이미지 크기
G_IMG_SIZE   = supported_patch_size[args.patch_size]
# 모델 레이어 개수
VGG_L        = 1
# 채널 수
VGG_FEATURES = 64
BATCH_SIZE   = args.batch_size
LAMBDA       = args.arg_lambda
MODEL_SAVE_PATH = args.model_save
STYLE_IMG       = args.style_path
TRAINSET_PATH   = args.train_set


style_img = open_img(STYLE_IMG)
# 해당 확장자명 파일들 훈련
input_ls = ls_files_to_json(TRAINSET_PATH, ext=['png', 'bmp', 'jpg', 'jpeg'])
TRAIN_SET = len(input_ls)




# 훈련 단계 추후 공부
# session 이란?  1.tensor연산실행	2.cpu, gpu 효율적 관리 
gpu_options = tf.GPUOptions(allow_growth=True)
with tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
# with tf.Session() as sess:
	# 판별자 입력 텐서
	input_s = tf.placeholder(tf.float32, shape=[BATCH_SIZE, PSI_D_SIZE, PSI_D_SIZE, 3], name='inps')
	# 생성자 입력 텐서
	input_c = tf.placeholder(tf.float32, shape=[BATCH_SIZE, G_IMG_SIZE, G_IMG_SIZE, 3], name='inpc')

	vgg_c = vgg16part.Vgg16()
	with tf.name_scope("content_vgg"):
		vgg_c.build(input_c)

	g_state = build_generator(input_c, name='generator')

	vgg_g = vgg16part.Vgg16()
	with tf.name_scope("content_vgg"):
		vgg_g.build(g_state)

	dp_real = build_discriminator(input_s, patch_size=PATCH_SIZE, name='discriminator')
	dp_fake = build_discriminator(g_state, patch_size=PATCH_SIZE, name='discriminator', reuse=True)

	d_raw = vgg_c.prob # 128 * 128 * 64
	d_gen = vgg_g.prob # 128 * 128 * 64

	d_real_d = tf.reduce_mean(dp_real)
	d_fake_d = tf.reduce_mean(dp_fake)

	mean_d_fake = tf.reduce_mean(dp_fake)
	d_fake_g = tf.reduce_mean((dp_fake) ** (1.0 - (dp_fake - mean_d_fake)))
	# d_fake_g = tf.reduce_mean(dp_fake)

	d_loss = -(tf.log(d_real_d) + tf.log(1 - d_fake_d))
	g_loss = (tf.norm(d_raw - d_gen) ** 2)*LAMBDA /(BATCH_SIZE*((G_IMG_SIZE/VGG_L)*(G_IMG_SIZE/VGG_L))*VGG_FEATURES)-tf.log(d_fake_g)
	# g_loss = tf.log(1 - d_fake_g) + (tf.norm(d_raw - d_gen) ** 2)*LAMBDA /(BATCH_SIZE*((G_IMG_SIZE/VGG_L)*(G_IMG_SIZE/VGG_L))*VGG_FEATURES)

	d_var_ls = tf.trainable_variables(scope='discriminator')
	# train_step_d = tf.train.AdamOptimizer(learning_rate=2e-4, beta1=0.5, beta2=0.9).minimize(d_loss, var_list=d_var_ls)
	update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
	with tf.control_dependencies(update_ops):
		train_step_d = tf.train.RMSPropOptimizer(5e-4).minimize(d_loss, var_list=d_var_ls)
	# train_step_d = tf.train.GradientDescentOptimizer(1e-3).minimize(d_loss, var_list=d_var_ls)

	g_var_ls = tf.trainable_variables(scope='generator')
	# train_step_g = tf.train.AdamOptimizer(learning_rate=2e-4, beta1=0.5, beta2=0.9).minimize(g_loss, var_list=g_var_ls)
	train_step_g = tf.train.RMSPropOptimizer(5e-4).minimize(g_loss, var_list=g_var_ls)
	# train_step_g = tf.train.GradientDescentOptimizer(1e-3).minimize(g_loss, var_list=g_var_ls)
	
	sess.run(tf.global_variables_initializer())
	var_ls = g_var_ls.append(d_var_ls)
	saver = tf.train.Saver(tf.trainable_variables(scope='generator'), max_to_keep=args.max_to_keep)
	epoch = 0
	train_cfg = load_cfg(args.cfg)
	if train_cfg['load_model']:
		chkpt_fname = tf.train.latest_checkpoint(MODEL_SAVE_PATH)
		saver.restore(sess, chkpt_fname)
	while epoch < train_cfg['epoch_lim']:
		train_cfg = load_cfg(args.cfg)
		random.shuffle(input_ls)
		travx = int(TRAIN_SET / BATCH_SIZE) + (1 if (TRAIN_SET % BATCH_SIZE) != 0 else 0)
		for offset in range(travx):
			train_cfg = load_cfg(args.cfg)
			sub_ls  = pickup_list(input_ls, BATCH_SIZE, offset * BATCH_SIZE)
			sub_img = images_batch(TRAINSET_PATH, sub_ls, prep=True,
								shape=(G_IMG_SIZE, G_IMG_SIZE), singleCh=False, remove_pad=True)	
			for td in range(train_cfg['D']['max_iter']):
				sess.run(train_step_d, feed_dict={
						input_s: make_input_batch(style_img, BATCH_SIZE, PSI_D_SIZE, PSI_D_SIZE, PATCH_SIZE),
						input_c: sub_img
					})
			for tg in range(train_cfg['G']['max_iter']):
				sess.run(train_step_g, feed_dict={
						input_c: sub_img
					})
			print('epoch %04d'%epoch, 'InnerProcess: %d/%d'%(offset, travx))

			if train_cfg['preview']:
				if train_cfg['view_iter'] == offset:
					util.silent_mkdir('preview/%d_%d'%(epoch, offset))
					util.save_batch_as_rgb_img(sess.run(g_state,
						feed_dict={input_c: sub_img}), 'preview/%d_%d'%(epoch, offset), prefix='0_')
			if train_cfg['save_model_iter'] == offset:
				saver.save(sess, os.path.join(MODEL_SAVE_PATH, "model"), global_step=epoch)


		cur_d_real = sess.run(d_real_d, feed_dict={
				input_s: make_input_batch(style_img, BATCH_SIZE, PSI_D_SIZE, PSI_D_SIZE, PATCH_SIZE),
				input_c: sub_img
			})
		cur_d_fake = sess.run(d_fake_d, feed_dict={
				input_c: sub_img
			})
		print('\33[1;32mEpoch %d D_TURN D real\33[0m = '%epoch, cur_d_real.mean())
		print('\33[1;31mEpoch %d D_TURN D fake\33[0m = '%epoch, cur_d_fake.mean())
		if epoch % train_cfg['export'] == 0:
			util.silent_mkdir('preview/%d'%epoch)
			util.save_batch_as_rgb_img(sess.run(g_state,
				feed_dict={input_c: sub_img}), 'preview/%d'%epoch, prefix='0_')
		if (epoch % train_cfg['save_step'] == 0 or epoch == train_cfg['save_at']):
			saver.save(sess, os.path.join(MODEL_SAVE_PATH, "model"), global_step=epoch)
		epoch = epoch + 1