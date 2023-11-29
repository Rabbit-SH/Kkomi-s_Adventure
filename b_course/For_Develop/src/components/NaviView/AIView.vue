<template>
    <div class="background" justify="center" align="center">
        <button @click="closeAI" class="close ma-2 pa-2">
            <img src="@/assets/mission/close.png">
        </button>
        <div class="ai-info mt-0" justify="center" align="center">
            <img src="@/assets/AIView/ai_info3.png" width="100%">
        </div>
        <v-overlay :value="loading">
            <v-card-text>
                <template v-if="isImage(currentContent)">
                    <img :src='currentContent' class="tmiImage"/>
                </template>

                <template v-else>
                    그거 알고 계셨나요?
                    <br>
                    {{ currentContent }}
                </template>
                <br>
                수묵화 변환중...
                <v-progress-linear
                    indeterminate
                    color="white"
                    class="mb-0"
                ></v-progress-linear>
            </v-card-text>
        </v-overlay>
        <div class="uploadIMG mt-3" justify="center" align-content="center">
            <img v-if="imageUrl" :src="imageUrl" alt="preview Image" class="preview_img">
        </div>
  
        <div v-if="!imageUrl && !istranslated" class="button_container my-16 mt-5">
            <input type = "file" @change="uploadImg" class='input' ref="fileInput" style="display: none;" />
            <v-btn class="chooseIMG py-6 text-h5 white--text" color="#EF8200" @click="triggeruploadImg"> 사진 선택 </v-btn>
        </div> 
        <div v-if="imageUrl && !istranslated" class="button_container2 my-16 mt-5 d-flex">
            <input type = "file" @change="uploadImg" class='input' ref="fileInput" style="display: none;" />
            <v-btn class="againChooseImg py-6 white--text" color="#EF8200" @click="triggeruploadImg"><v-icon size="30">mdi mdi-camera-outline</v-icon></v-btn>
            <v-btn class="translateImg py-6 text-h6 white--text" color="#EF8200" @click="paintC = true">화풍 고르기</v-btn>
        </div>
        <div v-if="istranslated" class="button_container my-16 mt-5">
            <v-btn class="chooseIMG py-6 text-h5 white--text" color="#EF8200" @click="downloadImage"> 저장하기 </v-btn>
        </div> 
        <div class="galley_container d-flex">
            <v-row justify="center" align-content="center" class="pa-0 ma-0">
                <v-col cols="12" class="mb-0 pb-0">
                    <v-icon color="white" size="25" @click="openGallery">mdi mdi-image-album</v-icon>
                </v-col>
                <v-col cols="12" class="white--text mt-0 pt-0 font-kkomi" style="font-size: 16px;">
                    갤러리
                </v-col>
            </v-row>
            
        </div>
        <v-dialog v-model="paintC" justify="center" align-items="center">
            <v-card class="text-center" justify="center" align-items="center">
                    <div class="choosePaint_container pa-3 pb-0">
                        <v-row>
                            <v-col cols="1">
                                <button align="center" justify="center" @click="paintC = false">X</button>
                            </v-col>
                            <v-col cols="11" justify="center" align="center">
                                <p class=" mt-1 paint-title font-kkomi">원하는 그림 스타일을 선택해주세요!       </p>
                            </v-col>
                        </v-row>
                        <v-carousel cycle hide-delimiters>
                            <template v-slot:prev="{ on, attrs }">
                                <v-icon v-bind="attrs" v-on="on" color="gray" size="30">mdi mdi-menu-left</v-icon>
                            </template>
                            <template v-slot:next="{ on, attrs }">
                                <v-icon v-bind="attrs" v-on="on" color="gray" size="30">mdi mdi-menu-right</v-icon>
                            </template>
                            <v-carousel-item justify="center" align="center">
                                <div class="font-kkomi">
                                    <h3> 한국화 </h3>
                                    <br>
                                    <p> 한국화는 한국의 전통 그림이에요! </p>
                                    <p>붓과 먹을 사용해서 부드러운 선으로 그림을 그려요 ! </p>
                                    <p>치악산의 멋진 자연을 그림으로 바꿔보아요 ~</p>
                                    <br>
                                    <img :src="require('@/assets/AIView/koreaPaint.png')" width="60%" class="mb-5"><!--예시 사진-->
                                    <br>
                                </div>
                                <v-btn @click="transformImg(1)" color="#EF8200" class="white--text"> 한국화로 그리기 </v-btn>
                            </v-carousel-item>
                            <v-carousel-item justify="center" align="center">
                                <div class="font-kkomi">
                                    <h3> 만화 </h3>
                                    <br>
                                    <p> 치악산의 배경과 함께 </p>
                                    <p> 자유롭게 찍어서 그림을 그려봐요 !  </p>
                                    <p> 찍은 사진을 만화처럼 그려줄거에요 !! </p>
                                    <br>
                                    <img :src="require('@/assets/AIView/cartoon.jpg')" width="80%" class="mb-5"><!--예시 사진-->
                                    <br>
                                </div>
                                <v-btn @click="transformImg(2)" color="#EF8200" class="white--text"> 만화로 그리기 </v-btn>
                            </v-carousel-item>
                            <v-carousel-item justify="center" align="center">
                                <div class="font-kkomi">
                                    <h3> 캐리커쳐 </h3>
                                    <br>
                                    <p>  얼굴 사진을 찍어서 그림을 그려봐요 !  </p>
                                    <p> AI 화가가 얼굴을 캐릭터처럼 그려줄거에요 ! </p>
                                    <p class="chracter-text"> 가까이 찍을수록 멋있게 그릴 수 있어요 </p>
                                    <br>
                                    <img :src="require('@/assets/AIView/character.png')" width="60%" class="mb-5"> <!--예시 사진-->
                                    <br>
                                </div>
                                <v-btn @click="transformImg(3)" color="#EF8200" class="white--text"> 캐릭터로 그리기 </v-btn>
                            </v-carousel-item>
                        </v-carousel>
                    </div>
            </v-card>
        </v-dialog>

        <GalleryView :show="gallery" @close="closeGallery" />
    </div>
</template>
  
<script>
import GalleryView from './GalleryView.vue';
import axios from 'axios';

export default {
    components:{GalleryView},
    data(){
        return{
            loading: false,
            imageUrl: null,
            preimage: null,
            istranslated: false, // false로 바꿔야 함
            response: null,
            paintC : false, // 화풍 선택 팝업창 열고 닫기 / false로 바꿔야
            contentIndex: 0,
            contents: ['/watertoad/030.png', '/watertoad/031.png', '/watertoad/032.png', '/watertoad/따봉꺼비.png'],
            gallery: false,

        }
    },
    mounted() {
        //5초마다 updateContent 메서드를 호출.
        setInterval(() => {
            this.contentIndex = (this.contentIndex + 1) % this.contents.length;
        }, 5000);
        this.check_m6();
    },
    computed: {
        currentContent(){
            return this.contents[this.contentIndex]
        },
        bg_photo(){
            return this.$store.getters.getBGPhoto;
        }
    },
    methods:{
        isImage(content) {
            return /\.(jpg|jpeg|png|gif)$/.test(content);
        },
        downloadImage() {
            if (this.imageUrl){
                const link = document.createElement('a');
                link.href = this.imageUrl;
                link.download = 'stylized_image.jpg';  // 다운로드될 파일명 설정
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                this.istranslated = false
            } else {
                alert('사진을 업로드 후 이용해주세요.')
            }

            this.imageUrl = '';
            this.istranslated = false;
            
        },
        async uploadImg(event) {
            // 이미지 업로드 로직
            //만약 사진을 고르지 않았다면?
            this.imageUrl = null;
            this.preimage = event.target.files[0];
            if (!this.preimage) {
                console.log("파일을 선택해주세요.");
                return;
            }
            const fileReader = new FileReader();
            fileReader.readAsDataURL(this.preimage)
            fileReader.onload = () => {
                    this.imageUrl = fileReader.result;
                    this.$store.commit('addPhoto', this.imageUrl);
            }
            this.istranslated = false
  
        },
        triggeruploadImg(){
            this.$refs.fileInput.click();
        },
        beforeUnload(event) {
            // 이벤트 취소 메시지 설정
            event.preventDefault();
            event.returnValue = ''; // 대부분의 브라우저에서는 이 메시지가 표시되지 않습니다.
        },
        async transformImg(convertOpt) {
            this.paintC = false;

            // 서버로 전송 하는 로직.
            const formData = new FormData();
            formData.append("file", this.preimage);
            formData.append("convertoption", convertOpt);

            this.loading = true;
            this.error = false;
            this.errorMessage = '';

            // 팝업창 닫는 로직
            this.paintC = false;

            try {
                // this.response = await axios.post('https://6984-1-244-138-205.ngrok-free.app/aipainter', formData,{responseType: 'blob'});
                this.response = await axios.post('http://localhost:8000/aipainter', formData,{responseType: 'blob'});
                
                this.imageUrl = URL.createObjectURL(this.response.data);
                // console.log("변환된 이미지 URL:", this.imageUrl);
                this.loading = false;
            } catch (error) {
                console.error("Error during image processing:", error);
                this.error = true;
                this.errorMessage = 'Error processing image. Please try again.';
                this.loading = false;
            }
            this.istranslated = true;

            },
        openGallery(){
            this.gallery = true;
        },
        closeGallery(){
            this.gallery = false;
        },
        check_m6(){
            if(this.bg_photo != null){
                this.imageUrl = null;
                this.preimage = this.bg_photo;
                this.imageUrl = this.preimage;
                this.istranslated = false;
            }
        },
        closeAI(){
            this.$store.commit('delBGPhoto');
            this.imageUrl = null;
            this.$router.push('./map');
        }
    }
}
</script>
  
<style scoped>
.background{
    background-image: url('~@/assets/background.png');
    width: 100%;
    height: 100%;
    background-position: center;
    background-size: cover;
}
.uploadIMG{
    width: 70%;
    height: 40%;
    background-color: rgba(255, 255, 255, 0.8);
    justify-content: center;
    align-items: center;
    display: flex;
}
.button_container{
    width: 70%;
}
.button_container2{
    width: 70%;
    justify-content: space-between;
}
.chooseIMG{
    width: 100%;
    height: 100%;
}
.preview_img{
    max-height: 95%;
    max-width: 95%;
}
.galley_container{
    position:absolute;
    bottom: 0%;
    right: 0%;
}
.close img{
    width: 22px;
    height: 22px;
    cursor: pointer;
    position: absolute;
    top: 3%;
    right: 5%;
  }
  .paint-title{
    color:gray;
    font-size: 14px;
  }
  .tmiImage{
    width: 85%;
  }
  .againChooseImg{
    width: 33%;
    height: 100%;
    }
    .translateImg{
        width: 63%;
        height: 100%;
    }
    .chracter-text{
        font-size: 15px;
        color: gray;
    }
    .ai-info{
        width: 80%;
    }
.font-kkomi{
    font-family: 'knps_kkomiregular' !important;
}
.v-responsive__content {
    flex: 100px;
    max-width: 100%;
    overflow: scroll;
}
</style>