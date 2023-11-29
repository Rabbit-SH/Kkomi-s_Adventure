<template>
    <div class="black-bg" v-if="show">
        <div class="white-bg">
            <img class = 'background' src= '@/assets/mission/bg_4.png'>
            <button class="close" @click="closeP">
                <img src="@/assets/mission/close.png">
            </button>
            <button class="info" @click="openinfo">
                <v-icon size="25">mdi-information-variant-circle</v-icon>
            </button>
            <div class="pic">
                <img src="@/assets/photo-bandal.png">
            </div>
            <div class="content">
                <div class="cam-container">
                    <div @click="triggerCamera" class="cam-button mb-3">
                        <v-btn class="custom-submit-button mt-3 pl-10 pr-10" color="#EF8200">사진 촬영하기</v-btn>
                    </div>
                    <input type="file" name="photofile" id="photofile" accept="image/*" capture="camera"
                    @change="onPhotoFileChange">
                </div>
                <br>
                <div class="img-container text-center">
                    <img src="" id="photoimg">
                </div>
            </div>
        </div>
        <v-dialog v-model="dialog" max-width="500">
            <v-card class="pa-3">
                <v-card-text>
                <v-row align="center" justify="center">
                    <v-col align="center">
                    <div class="img-container text-center">
                        <img :src="uploadedPhoto" id="dialogPhoto" style="max-height:100%; max-width:100%;">
                    </div>
                    <br>
                    <div class="text-center">
                        <p>이미지 다운로드를 원하면</p>
                        <p>아래의 <strong>다운로드</strong> 버튼을 눌러주세요.</p>
                    </div>
                    <div class="button-container">
                        <div class="btn">
                            <v-btn @click="downloadImage" class="download mr-2" color="#EF8200">다운로드</v-btn>
                        </div>
                        <div class="next">
                            <v-btn @click="handleDialogConfirmation" class="nextmission" color="#EF8200">다음 미션으로 >></v-btn>
                        </div>
                    </div>
                    </v-col>
                </v-row>
                </v-card-text>
            </v-card>
        </v-dialog>

        <v-dialog v-model="infodialog" class="infodialog">
            <v-card-text class="title">
                <h3>가족사진 데크길</h3>
                <img @click="infodialog = false" src="@/assets/mission/close.png" class="closeinfo">
            </v-card-text>
                <img src="@/assets/mission/missionInfo/info9.jpeg" class="pic-info">
        </v-dialog>

    </div>
</template>

<script >
import axios from 'axios';
export default {
    props: {
        show: {
            type: Boolean,
            required: true,
        },
        result4: {
            type: Boolean,
        }
    },
    data(){
      return {
        userResult: '', //사용자 응답 저장하는 데이터
        dialog: false,
        infodialog: false,
        error: false,
        errorMessage: '',
        userResponse:'',
        uploadedPhoto: null, // 업로드된 사진 데이터를 위한 변수
        response: null,
        uploadimg: null //업로드 사진
      }
    },
    methods: {
        closeP(){
            this.$emit('close');
        },
        openinfo(){
            this.infodialog = true;
        },
        triggerCamera(){
            const photoFileInput = this.$el.querySelector("#photofile");
            photoFileInput.click();
        },
        onPhotoFileChange(event){
            this.uploadimg = event.target.files[0]
            // 파일데이터를 갤러리 리스트에 추가합니다.
            const fileReader = new FileReader();
            fileReader.readAsDataURL(event.target.files[0]);
            fileReader.onload = () => {
                
                const photoDataUrl = fileReader.result;
                this.uploadedPhoto = photoDataUrl;

                // 갤러리에 사진 추가
                this.$store.commit('addPhoto', photoDataUrl);
                this.convert_img();
            }
            this.dialog = true;
        },
        async convert_img(){

              // 가족사진을 수묵화로 변환하기 위한 요청
                const formData = new FormData();
                formData.append("file",this.uploadimg);
                formData.append("convertoption",4);

                this.error = false;
                this.errorMessage = '';

                try {
                    // this.response = await axios.post('https://6984-1-244-138-205.ngrok-free.app/aipainter', formData,{responseType: 'blob'});
                    this.response = await axios.post('http://localhost:8000/aipainter', formData,{responseType: 'blob'});
                    this.imageUrl = URL.createObjectURL(this.response.data);
                } catch (error) {
                    console.error("Error during image processing:", error);
                    this.error = true;
                    this.errorMessage = 'Error processing image. Please try again.';
                }
                this.$store.commit('setFamily', this.imageUrl);
        },

        handleDialogConfirmation(){
            this.dialog = false;

            if (this.result4 === false){
                this.$emit('answerCorrect');
            }
            this.userResult = ''; // 사용자 응답 리셋
            this.closeP();        // 다이얼로그 닫기
        },

        downloadImage() {
            if (this.uploadedPhoto) {
            // 이미지를 다운로드하는 링크를 생성
            const link = document.createElement('a');
            link.href = this.uploadedPhoto;

            // 다운로드되는 파일의 이름 설정 (예: downloaded-image.jpg)
            const filename = 'family_img.jpg';
            link.download = filename;

            // 링크를 추가하고 클릭하여 다운로드 시작
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            } else {
            // 이미지가 없는 경우에 대한 처리 (예: 경고 또는 사용자에게 알리기)
            alert('이미지를 먼저 업로드하세요!');
            }
        },

    }
}
</script>

<style scoped>
    .black-bg{
        width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.5);
        position: fixed; 
        top: 0;
        left: 0;
        padding: 20px;
        z-index: 1500;
        display: flex;
        align-items: center;
        justify-content: center;
      }

    .img-container{
        justify-content: center;
        display: flex;
        align-items: center;
    }
    #photoimg {
        display: none;
        width: 50%;
        height: auto; /* 이미지의 원래 비율을 유지 */
        margin-top: 20px; /* 상단 여백 추가 */
    }

    #photofile{
        display:None;
    }

    #dialogPhoto {
        width: 80%; /* 이미지 크기 조절 */
    }
    .cam-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px; /* 상단 여백 추가 */
    }
    .button-container {
        width: 100%; /* 너비를 전체로 설정 */
        padding: 10px 20px; /* 패딩을 상하에만 적용 */
        display: flex; /* 버튼들을 가로로 정렬 */
        justify-content: center; /* 가운데 정렬 */
        margin-top: auto; /* 위쪽 요소들이 차지한 후 남은 공간을 모두 차지 */
    }
      .white-bg{
        width: 90%; height: 90%;
        position: fixed; 
        /* background-color: white; */
        overflow:hidden;
        display:flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

      }
    .background{
        width: 100%;
        height: 100%;
    }

    .content{
        width:100%;
        position: absolute;
        bottom: 7%;
        max-height: 45%;
        overflow-y: auto;
    }

    .close img{
        width: 22px;
        height: 22px;
        cursor: pointer;
        justify-content: center;
        align-items: center;
        position:absolute;
        top: 3%;
        right: 5%;
    }
    .custom-submit-button {
        color: white !important; /* 텍스트 색상을 흰색으로 */
        font-weight: bold; /* 글씨 두께를 굵게 */
        font-size: 18px; /* 글씨 크기를 18px로 설정 */
    }
    .next {
        justify-content: center; /* 내부 요소를 중앙 정렬 */
        }
    .download{
        color: white !important; 
        font-weight: bold; 
        font-size: 18px;
        width: 110px;
    }
    .nextmission{
        color: white !important; 
        font-weight: bold; 
        font-size: 18px;
        width: 190px;
    }
    .pic{
        width: auto;
        height: 35%;
        bottom: 17%;
        position: absolute;
        left: 52%;
        transform: translateX(-50%);
    }
    .pic img{
        width: 100%;
        height: 100%;
    }
    .info{
        position:absolute;
        top: 3%;
        left: 5%;
        width: 22px;
        height: 22px;
        cursor: pointer;
        justify-content: center;
        align-items: center;
    }
    .infodialog{
        position: absolute;
        box-shadow: none;
        /* width: 30%;
        height: auto; */
    }
    .closeinfo{
        width: 22px;
        height: 22px;
        cursor: pointer;
        justify-content: center;
        align-items: center;
        position:absolute;
        top: 30%;
        right: 5%;
    }
    .pic-info{
        width: 100%;
        height: auto;
    }
    .title{
        background-color: white;
        position: relative;
    }
    .v-application .info {
        background-color: transparent !important;
        border-color: transparent !important;
    }
        ::v-deep .v-dialog { /* 지우면 안됨 */
        box-shadow: none !important;
    }
</style>