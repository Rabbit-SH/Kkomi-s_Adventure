<template>
    <div class="black-bg" v-if="show">
        <div class="white-bg">
            <img class = 'background' src= '@/assets/mission/bg_6.png'>
            <button class="close" @click="closeP">
                <img src="@/assets/mission/close.png">
            </button>
            <button class="info" @click="openinfo">
                <v-icon size="25">mdi-information-variant-circle</v-icon>
            </button>
            <div class="pic">
                <img src="@/assets/photo-ggomi.png">
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
                        <p>이미지 다운로드를 원하면 아래의 <strong>다운로드</strong> 버튼을 눌러주세요.</p>
                        <p>내가 찍은 사진을 수묵화 그림으로 바꿔보고 싶다면 <strong>AI 화가</strong> 버튼을 눌러주세요.</p>
                    </div>
                    <div>
                        <div class="btn_container">
                            <v-btn @click="downloadImage(uploadedPhoto)" class="btn mt-3 pl-10 pr-10" color="#EF8200">다운로드</v-btn>
                            <v-btn @click="goToAiPainter" class="btn mt-3 pl-10 pr-10" color="#EF8200">AI 화가</v-btn>
                        </div>
                        <div class="card">
                            <v-btn @click="handleDialogConfirmation" class="ok-btn mt-3 pl-10 pr-10" color="#EF8200">다음 미션으로 >></v-btn>
                        </div>
                    </div>
                    </v-col>
                </v-row>
                </v-card-text>
            </v-card>
        </v-dialog>

        <v-dialog v-model="infodialog" class="infodialog">
            <v-card-text class="title">
                <h3>구룡사</h3>
                <img @click="infodialog = false" src="@/assets/mission/close.png" class="closeinfo">
            </v-card-text>
                <img src="@/assets/mission/missionInfo/info6.jpeg" class="pic-info">
        </v-dialog>

    </div>
</template>

<script >
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
    components:{
      
    },
    data(){
      return {
        userResult: '', //사용자 응답 저장하는 데이터
        dialog: false,  //이미지 업로드 후 팝업창 여는 데이터
        infodialog: false, 

        userResponse:'',
        uploadedPhoto: null, // 업로드된 사진 데이터를 위한 변수
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

              // 파일데이터를 갤러리 리스트에 추가합니다.
            const fileReader = new FileReader();
            fileReader.readAsDataURL(event.target.files[0]);
            fileReader.onload = () => {
                const photoDataUrl = fileReader.result;
                this.uploadedPhoto = photoDataUrl;
                // 갤러리를 위한 코드 (vuex에 정의된 리스트photos에 photoDataUrl 추가)
                this.$store.commit('addPhoto', photoDataUrl);
            }
            this.dialog = true; //팝업창 열기
        },
        handleDialogConfirmation(){
            this.dialog = false;

            if (this.result4 === false){
                this.$emit('answerCorrect');
            }
            this.userResult = ''; // 사용자 응답 리셋
            this.closeP();        // 다이얼로그 닫기
        },
        goToAiPainter(){
            this.$router.push({name:'AIView'});
            if (this.result4 === false){
                this.$emit('answerCorrect');
            }
            this.userResult = '';
            this.$store.commit('setBGPhoto', this.uploadedPhoto);
        },

        downloadImage(uploadedPhoto) {
            if (uploadedPhoto) {
                // 이미지를 다운로드하는 링크를 생성
                const a = document.createElement('a');
                a.href = uploadedPhoto;

                // 다운로드되는 파일의 이름 설정 (예: downloaded-image.jpg)
                const filename = `family_img`;
                a.download = filename;

                // 링크를 추가하고 클릭하여 다운로드 시작
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
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
      .white-bg{
        width: 90%; height: 90%;
        position: fixed; 
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
        max-height: 50%;
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
    .img-container{
        justify-content: center;
        display: flex;
        align-items: center;
    }
    #photoimg {
        display: none;
        width: 70%;
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
    .custom-submit-button {
        color: white !important; /* 텍스트 색상을 흰색으로 */
        font-weight: bold; /* 글씨 두께를 굵게 */
        font-size: 18px; /* 글씨 크기를 18px로 설정 */
    }
    .card {
    justify-content: center; /* 내부 요소를 중앙 정렬 */
    }
    .ok-btn{
        color: white !important; 
        font-weight: bold; 
        font-size: 18px;
        width: 180px;
    }
    .btn{
        color: white !important; 
        font-weight: bold; 
        font-size: 18px;
        margin: 3px;
        width: 85px;
    }
    .pic{
        width: 60%;
        height:auto;
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