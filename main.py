from fastapi import FastAPI,UploadFile, File, BackgroundTasks,Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
from fastapi.middleware.cors import CORSMiddleware
from b_course.model_cartoon.cartoon import cartoonize
from b_course.model_sumug.sumug import sumug,seg_sumug
from b_course.model_animation.animation import animation
import os

# AVX2오류 무시
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
   

app = FastAPI()

#CORS문제 해결
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프론트엔드 서버 주소
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)
# 정적파일 마운트
app.mount(
    "/watertoad",
    StaticFiles(
        directory="./b_course/dist",
        html=True,
    ),
    name="watertoad",
)

#시작페이지 제공
@app.get("/")
async def gotowatertoad():
    return FileResponse("./b_course/dist/index.html")

# 파일 삭제 함수
def remove_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(f"Error while deleting file {path}: {e}")

# aipainter 요청시, 수묵화,애니메이션,만화풍 + 가족사진(세그멘테이션) 수묵화 변환 기능 제공
@app.post("/aipainter")
async def aipainter(background_tasks: BackgroundTasks, file: UploadFile = File(...),convertoption: int = Form(...)):
    try:
        # 업로드된 사진 경로 설정해서 저장.
        input_image_path = f"./b_course/input/watertoad_{convertoption}_{file.filename}"
        with open(input_image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # 변환 이미지 파일명, 경로 설정.
        # 폴더가 없으면 생성.
        convert_path = "./b_course/output/"
        os.makedirs(convert_path, exist_ok=True)
        convert_image_path = f"{convert_path}watertoad_{convertoption}_converted_{file.filename}"
        
        # Aipainting 옵션
        if (convertoption==1):
            #수묵화 변환 함수 호출
            sumug(input_image_path,convert_image_path)
        elif (convertoption==2):
            #애니메이션 변환 함수 호출
            cartoonize(input_image_path,convert_image_path)
        elif (convertoption==3):
            #만화 변환 함수 호출
            animation(input_image_path,convert_image_path)
        elif (convertoption==4):
            #가족사진(세그멘테이션) 수묵화 변환 함수 호출
            seg_sumug(input_image_path,convert_image_path)

        response = FileResponse(convert_image_path,media_type="media/jpeg")
        
        # 파일 전송 후 백그라운드에서 삭제
        background_tasks.add_task(remove_file, input_image_path)
        background_tasks.add_task(remove_file, convert_image_path)

        return response
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
