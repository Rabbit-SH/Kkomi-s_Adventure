<template>
  <div class="final-page">
    <button @click="$router.push({name:'MainView'})" class="close ma-2 pa-2">
      <img src="@/assets/mission/close.png">
    </button>

    <div  class="photo">
        <canvas id="canvas" style="display:none;"></canvas>
         <img v-if="mergedImage" :src="mergedImage"/>
       <!-- <img :src="familyphoto" alt="familyphoto"/> 이건 잘됨. -->

    </div>
    <div class="present">
      <img :src="require('@/assets/open.png')">
    </div>
    <div class="button-container">
      <v-btn @click="downloadImage" class="ok-btn mt-3 pl-10 pr-10" color="#EF8200">선물 받기</v-btn>
    </div>
    <v-dialog v-model="dialog" class="dialog">
            <v-card class="pa-3">
                <v-card-text>
                <v-row align="center" justify="center">
                    <v-col align="center">
                    <br>
                    <div class="text-center">
                        <h3>우리가 함께한 <strong>물두꺼비 모험</strong>은 어땠나요? 재미있었나요?</h3>
                        <br>
                        <p>여러분이 어떻게 느꼈는지 알려주면, 다음에 더 신나고 멋진 모험을 준비할 수 있어요!</p>
                        <p>아래 버튼을 눌러 간단한 <strong>설문조사</strong>에 참여해 주세요</p>
                        <p>여러분의 소중한 의견이 큰 도움이 될 거예요!</p>
                    </div>
                    <div class="final-img" id="dudu">
                      <img :src="require('@/assets/final-dudu.jpg')">
                    </div>
                    <div>
                        <v-btn @click="openGoogleForm" class="google-form-button mt-3 pl-10 pr-10" color="#EF8200">만족도 설문조사 하기</v-btn>
                    </div>
                    </v-col>
                </v-row>
                </v-card-text>
            </v-card>
        </v-dialog>
  </div>
  
</template>

<script>
import { mapState } from 'vuex';

export default {
name: 'FinalView',
data(){
  return {
    dialog: false,
    mergedImage: null,
  };
},
mounted() { 
  this.combineImage();
 },
computed: {
  ...mapState({familyphoto:"family"})
},
methods: {
  combineImage() {
    const canvas = document.querySelector("#canvas");

    const ctx = canvas.getContext('2d')

    const img2 = new Image();
    img2.src = require('@/assets/final-temp.png');

      // 두 번째 이미지 로드
    img2.onload = () => {
      // Canvas 크기 설정
      canvas.width = img2.width;
      canvas.height = img2.height;

      //첫번째 이미지 로드
      const img1 = new Image();
      img1.src = this.familyphoto;

      img1.onload = () => {
        // 첫 번째 이미지 그리기 (액자 틀에 맞추기)
        ctx.drawImage(img1, 40, 40, img2.width-83, img2.height-230);
        // 두 번째 이미지 그리기 (최대크기)
        ctx.drawImage(img2, 0, 0, img2.width, img2.height); 

        // Canvas의 내용을 이미지로 추출
        this.mergedImage = canvas.toDataURL('image/png');
      };

    }
  },
  downloadImage() {
    // 다운로드를 위한 임시 링크 요소를 생성합니다.
    const link = document.createElement('a');
    link.href = this.mergedImage;

    // 다운로드될 파일의 이름을 설정합니다.
    link.download = 'familyphoto';

    // 링크를 문서에 추가하고 클릭합니다.
    document.body.appendChild(link);
    link.click();

    // 링크를 다시 제거합니다.
    document.body.removeChild(link);

    // 다운로드 후 대화 상자를 표시합니다.
    this.dialog = true;
    },

  openGoogleForm(){
    const url = "https://docs.google.com/forms/d/e/1FAIpQLSdBCQgSi7xSaxSddm6OTSFwxXKcOjrNvLxfllJq-o0S7_09OQ/viewform?usp=sf_link";
    const options = "width = 700, height=600, left=200, top=200";
    window.open(url, "_blank", options);
    },
},
}

</script>

<style scoped>
.final-page{
  background-image: url('@/assets/background.png');
  background-size: cover; /* 이미지가 div를 전체적으로 커버하도록 설정 */
  height: 100vh; /* 또는 다른 고정된 높이 */
  display: flex;
  justify-content: center; /* 가로 중앙 정렬 */
  align-items: center; /* 세로 중앙 정렬 */
  position: relative;
}
.close img{
  width: 22px;
  height: 22px;
  cursor: pointer;
  position: absolute;
  top: 3%;
  right: 5%;
}

.photo {
  position: absolute;
  width: 75%;
  max-width: 80%;
  max-height: auto;
  height: auto;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  justify-content: center;
  align-items: center;
}
#canvas{
  max-width: 100%;
  max-height: 100%;
}
.photo img{
  width: 100%;

}

.present{
  position: absolute;
  bottom: 8%;
  width: 50%;
  height: auto;
}
.present img{
  width: 100%;
  height: 100%;
  /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.5); */
}
.button-container{
  position: absolute;
  bottom: 5%;
  display: flex; /* Flexbox 레이아웃 사용 */
  flex-direction: column; /* 요소들을 세로로 정렬 */
  align-items: center; /* 가로 중앙 정렬 */
}

.ok-btn{
  color: white !important;
  font-weight: bold;
  font-size: 18px;
  width: 100%;
}
.google-form-button{
  color: white !important;
  font-weight: bold;
  font-size: 18px;
  width: 100%;
}
.dialog{
  width: 90%;
}
.final-img {
  width: 45%;
  height: auto;
  bottom: 5%;

}
.final-img img{
  width: 100%;
  height: 100%;
}
.original_img {
    max-height: 95%;
    max-width: 95%;
}
</style>