from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks,Form
from fastapi.responses import (
    FileResponse,
    JSONResponse,
)
from fastapi.staticfiles import StaticFiles
import shutil
import os
from io import BytesIO
from a_course.model_cartoon.cartoon import cartoonize
from a_course.model_soomuk.soomuk import soomuk
from a_course.model_animation.animation import animation
import os
# from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프론트엔드 서버 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.mount("/static", StaticFiles(directory="./a_course/public"), name="static")

# scheduler = BackgroundScheduler()

app.mount(
    "/watertoad",
    StaticFiles(
        directory="./b_course/dist",
        html=True,
    ),
    name="watertoad",
)


@app.get("/")
async def root():
    return FileResponse("./a_course/public/StartPage/start.html")


@app.get("/watertoad")
async def waterfrog():
    return FileResponse("./b_course/dist/index.html")


@app.get("/course")
async def course():
    return FileResponse("./a_course/public/course/course.html")


@app.get("/practice")
async def start():
    return FileResponse("./a_course/public/main.html")


# 코스를 불러오는 API
@app.get("/json/{course:int}코스.json")
async def course_json(course: int):
    if 1 <= course <= 13:
        return FileResponse(f"public/{course}코스.json")
    else:
        raise HTTPException(status_code=404, detail="Course not found")


# 원본 사진을 저장 API
def save_original(file, path):
    with open(path, "wb") as f:
        f.write(file.file.read())


# 파일 업로드 시 원본, 모네 이미지 저장 API
@app.post("/upload_image/{missionNum}")
async def img_convert(
    file: UploadFile = File(...),
    missionNum: int = 1,
    userId: int = 0,
    styleNum: int = 0,
):
    try:
        original_filename = str(missionNum) + "_" + str(userId) + "_original.jpg"
        convert_filename = str(missionNum) + "_" + str(userId) + "_convert.jpg"

        original_path = f"./a_course/public/benefit/img/{original_filename}"
        convert_path = f"./a_course/public/benefit/img/{convert_filename}"

        save_original(file, original_path)
        if styleNum == 1:
            soomuk(original_path, convert_path)
        elif styleNum == 2:
            cartoonize(original_path, convert_path)
        elif styleNum == 3:
            animation(original_path, convert_path)

        return {"original_path": original_path}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# 파일 업로드 시 원본, 수묵화 저장 API (백그라운드)
@app.post("/upload_image/background/{missionNum}")
async def img_convert(
    background_task: BackgroundTasks,
    file: UploadFile = File(...),
    missionNum: int = 1,
    userId: int = 0,
):
    try:
        original_filename = str(missionNum) + "_" + str(userId) + "_original.jpg"
        monet_filename = str(missionNum) + "_" + str(userId) + "_convert.jpg"

        original_path = f"./a_course/public/benefit/img/{original_filename}"
        convert_path = f"./a_course/public/benefit/img/{monet_filename}"

        # 이미지 저장 백그라운드 작업
        background_task.add_task(save_original, file, original_path)
        # 모델 백그라운드 작업
        background_task.add_task(soomuk, original_path, convert_path)

        return {"original_path": original_path}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# 이미지 폴더를 클리닝 API
@app.delete("/delete_all")
def remove_files():
    directory_to_cleanup = "./public/benefit/img"
    # 현재 시간 출력
    print(f"Cleaning up directory {directory_to_cleanup} at {datetime.now()}")
    # 디렉토리 내 모든 파일 삭제
    for filename in os.listdir(directory_to_cleanup):
        file_path = os.path.join(directory_to_cleanup, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


# 매일 자정에 img 파일에 담긴 이미지 삭제 (개인정보 보호)
# @app.on_event("startup")
# def start_scheduler():
#     scheduler.add_job(remove_files, "cron", hour=0)
#     scheduler.start()
#     print("Scheduler has been started.")


###### B팀 코드 API

from PIL import Image
from fastapi.staticfiles import StaticFiles
import numpy as np
from sklearn.cluster import KMeans
import requests
import tempfile
from io import BytesIO
from sklearn.cluster import MeanShift, estimate_bandwidth
import cv2
import subprocess
import os
import uvicorn
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
from b_course.model_cartoon.cartoon import cartoonize
from b_course.model_sumug.sumug import sumug,seg_sumug
from b_course.model_animation.animation import animation


def remove_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(f"Error while deleting file {path}: {e}")

# def segment_image(image, k=3):
#     # 이미지를 NumPy 배열로 변환
#     data = np.array(image)

#     # 이미지 데이터를 2D로 변환 (각 픽셀은 RGB 색상을 가짐)
#     w, h, d = data.shape
#     data = data.reshape((w * h, d))

#     # KMeans 클러스터링
#     kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
#     labels = kmeans.predict(data)

#     # 클러스터링 결과에 따라 색상 재할당
#     segmented_data = kmeans.cluster_centers_.astype("uint8")[labels]

#     # 2D 데이터를 원래 이미지 크기로 다시 변환
#     segmented_image = segmented_data.reshape((w, h, d))

#     return Image.fromarray(segmented_image)


# def adjust_brightness_dynamic(image, dark_factor=1.5, bright_factor=1):
#     # Ensure the image is a float type for calculations
#     if image.dtype != np.float32:
#         image = image.astype(np.float32)

#     # Find the mean value of the image for threshold
#     mean_value = np.mean(image)

#     # Apply different factors based on brightness
#     adjusted_image = np.where(
#         image <= mean_value, image / dark_factor, image * bright_factor
#     )

#     # Clip the values to ensure they remain within the range and convert back to original data type
#     adjusted_image = np.clip(adjusted_image, 0, 255).astype(np.uint8)

#     return adjusted_image


# def load_and_preprocess(image_path):
#     # 이미지 읽어오기
#     image = cv2.imread(image_path)
#     # 이미지 크기 확인
#     height, width = image.shape[:2]
#     # 이미지 크기를 절반으로 조정
#     resized_image = cv2.resize(image, (width // 2, height // 2))
#     # color segmentation
#     segmented_img = segment_image(resized_image, 5)

#     # numpy 오류 해결
#     if isinstance(segmented_img, Image.Image):
#         segmented_img = np.array(segmented_img)

#     # 그레이스케일로 변경
#     gray_image = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2GRAY)

#     # 클라해 수행
#     # Adaptive Histogram Equalization 적용
#     clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
#     clahe_image = clahe.apply(gray_image)

#     # 픽셀 조절
#     dynamic_img = adjust_brightness_dynamic(clahe_image)

#     return dynamic_img

# AIPainter 수묵화,애니메이션,만화풍 + 가족사진(세그멘테이션) 수묵화 변환
@app.post("/aipainter")
async def aipainter(background_tasks: BackgroundTasks, file: UploadFile = File(...),convertoption: int = Form(...)):
    # 업로드된 사진 경로 설정해서 저장.
    input_image_path = f"./b_course/input/watertoad_{convertoption}_{file.filename}"
    with open(input_image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    convert_image_path = f"./b_course/input/watertoad_{convertoption}_converted_{file.filename}"
    
    if (convertoption==1):
        sumug(input_image_path,convert_image_path)
    elif (convertoption==2):
        #애니메이션 변환 함수 호출
        cartoonize(input_image_path,convert_image_path)
    elif (convertoption==3):
        #만화 변환 함수 호출
        animation(input_image_path,convert_image_path)
    elif (convertoption==4):
        seg_sumug(input_image_path,convert_image_path)
        
    response = FileResponse(convert_image_path,media_type="media/jpeg")

    # 파일 전송 후 삭제
    background_tasks.add_task(remove_file, input_image_path)
    background_tasks.add_task(remove_file, convert_image_path)

    return response
