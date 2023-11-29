<template>
    <div class="black-bg" v-if="show">
        <div class="white-bg">
            <img class = 'background' src= '@/assets/mission/bg_1.png'>
            <button class="close" @click="closeP">
                <img src="@/assets/mission/close.png">
            </button>
            <button class="info" @click="openinfo">
                <v-icon size="25">mdi-information-variant-circle</v-icon>
            </button>
            <div class="content-container" justify="center" align="center">
                <v-row class="sound-item d-flex">
                    <v-col cols="4">
                        <v-btn @click="toggleAudio(sounds[0])" fab>
                            <v-icon large  :style="{ color: sounds[0].isActive ? 'green' : 'gray' }">mdi mdi-volume-high</v-icon>
                        </v-btn>
                    </v-col>
                    <v-col cols="4">
                        <v-btn @click="toggleAudio(sounds[1])" fab>
                            <v-icon large  :style="{ color: sounds[1].isActive ? 'green' : 'gray' }">mdi mdi-volume-high</v-icon>
                        </v-btn>
                    </v-col>
                    <v-col cols="4">
                        <v-btn @click="toggleAudio(sounds[2])" fab>
                            <v-icon large  :style="{ color: sounds[2].isActive ? 'green' : 'gray' }">mdi mdi-volume-high</v-icon>
                        </v-btn>
                    </v-col>
                </v-row>
                <v-row class="sound-item">
                    <v-col cols="auto" >
                        <v-checkbox hide-details class="shrink ml-4 mr-2" style="transform: scale(1.5);" v-model="userResult" :value="sounds[0].value"></v-checkbox>
                    </v-col>
                    <v-col cols="auto" >
                        <v-checkbox hide-details class="shrink ml-4 mr-2" style="transform: scale(1.5);" v-model="userResult" :value="sounds[1].value"></v-checkbox>
                    </v-col>
                    <v-col cols="auto" >
                        <v-checkbox hide-details class="shrink ml-4 mr-2" style="transform: scale(1.5);" v-model="userResult" :value="sounds[2].value"></v-checkbox>
                    </v-col>
                </v-row>
                <br>
                <br>
                <br>
                <v-btn class="custom-submit-button" color="#EF8200" @click="submitSoundRes">제출하기</v-btn>
            </div>

        </div>
        <v-dialog v-model="dialog" max-width="500">
            <v-card>
                <v-card-text>
                    <v-row align="center" justify="center">
                        <v-col align="center">
                            <div style="height:100%; width:100%; display: flex; align-items: center; justify-items: center;">
                                <v-img v-if="userResult === '꿩'" src="@/assets/O.png"></v-img>
                                <v-img v-else src="@/assets/X.png"></v-img>
                            </div>
                            <br>
                            <div v-if="userResult === '꿩'" class="text-center">
                                <h3>정답입니다!</h3> 
                                <br>
                                <br>
                                <h4> 이제 본격적으로 미션을 시작하러 가볼까요? </h4>
                                <br>
                                <h4> 지도 위의 물음표가 있는 위치로 </h4>
                                <h4> 따라와주세요! </h4>
                                <br>
                            </div>
                            <div v-else class="text-center">
                                <h3>다시 한번 풀어볼까요?</h3>
                            </div>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions class="card">
                <v-btn @click="handleDialogConfirmation(userResult === '꿩')" class="ok-btn" color="#EF8200">{{ userResult === '꿩' ? '시작하기 >>' : '확인' }}</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="infodialog" class="infodialog">
            <v-card-text class="title">
                <h3>치악산체험학습관</h3>
                <img @click="infodialog = false" src="@/assets/mission/close.png" class="closeinfo">
            </v-card-text>
                <img src="@/assets/mission/missionInfo/info1.jpeg" class="pic">
        </v-dialog>

    </div>
</template>

<script scoped>
import { Howl } from 'howler';

export default {
    props: {
        show: {
            type: Boolean,
            required: true,
        },
        result1: {
            type: Boolean,
        }
    },
    data(){
      return {
            userResult: '', //사용자 응답 저장하는 데이터
            showPopup: false, //팝업 상태
            dialog: false,
            infodialog: false,

            sounds: [
                { id: 1, src: "/watertoad/꿩.mp3", isActive: false, howl: null, value: '꿩' },
                { id: 2, src: "/watertoad/멧비둘기.mp3", isActive: false, howl: null, value: '멧비둘기' },
                { id: 3, src: "/watertoad/검은등뻐꾸기.mp3", isActive: false, howl: null, value: '검은등뻐꾸기' },
            ],
      }
    },
    methods: {
        closeP(){
            this.$emit('close');
        },
        openinfo(){
            this.infodialog = true;
        },
        submitResponse(){
          console.log(this.userResponse); //콘솔에 출력, 서버에 제출하거나 다른 제출을 추가해도됨
          this.userResponse = ''; //답변이 제출되면 리셋하기
        },
        //팝업 여는 메소드
        showHint(){
          this.showPopup=true;
        },
        //팝업 닫는 메소드
        closePopup(){
          this.showPopup=false;
        },
        submitSoundRes(){
            this.stopAllSounds();
            if(this.userResult.trim() == ''){
                alert("답변을 입력해주세요!")
            } else {
                if(this.userResult === '꿩'){
                    // 정답 다이얼로그 표시
                    this.dialog = true;
                } else {
                    //오답 다이얼로그 표시
                    this.dialog = true;
                }
            }
        },
        stopAllSounds() {
            this.sounds.forEach((sound) => {
                if (sound.playing) {
                    sound.howl.stop();
                    sound.playing = false;
                    sound.isActive = false;
                }
            });
        },
        handleDialogConfirmation(correct){
            this.dialog = false;
            if(correct){
                if (this.result1 === false){
                    //result1가 false인 경우만 'answerCorrect' 이벤트를 트리거(마커를 정답 이미지로 바꾸기 위하여)
                    this.$emit('answerCorrect');
                }
                this.userResult = ''; // 사용자 응답 리셋
                this.closeP();        // 다이얼로그 닫기
            }
        },
        toggleAudio(sound) {
            this.stopAllSoundsExcept(sound.id);

            if (sound.playing) {
                sound.howl.stop();
            } else {
                sound.howl = new Howl({
                src: [sound.src],
                volume: 1,
                onend: () => {
                    sound.playing = false;
                },
                });
                sound.howl.play();
                sound.playing = true;
            }

            // 토글하여 초록색 스타일 변경
            sound.isActive = !sound.isActive;
        },
        stopAllSoundsExcept(exceptId) {
            this.sounds.forEach((sound) => {
                if (sound.playing && sound.id !== exceptId) {
                sound.howl.stop();
                sound.playing = false;
                sound.isActive = false; // 다른 사운드 중지 시에는 isActive를 false로 설정
                }
            });
        },

    }
}
</script>

<style scoped>
    img{
        width: 100%;
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
    .content-container{
        width:100%;
        position: absolute;
        bottom: 15%;
    }
    .close{
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
    .card {
    justify-content: center; /* 내부 요소를 중앙 정렬 */
    }
    .ok-btn{
        color: white !important; 
        font-weight: bold; 
        font-size: 18px;
    }

    div.row.sound-item{
        justify-content: space-evenly;
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
    .pic{
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