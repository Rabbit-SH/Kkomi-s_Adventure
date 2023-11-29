<template>
    <div class="black-bg" v-if="show">
        <div class="white-bg">
            <img class = 'background' src= '@/assets/mission/bg_5.png'>
            <button class="close" @click="closeP">
                <img src="@/assets/mission/close.png">
            </button>
            <button class="info" @click="openinfo">
                <v-icon size="25">mdi-information-variant-circle</v-icon>
            </button>
            <div class="content-container" justify="center" align="center">
                <div class="correctSound mb-4">
                    <p>물두꺼비 소리</p>
                    <!-- <audio controls src="@/assets/꿩.wav"></audio> -->
                    <v-btn @click="toggleAudio(sounds[3])" fab>
                        <v-icon large  :style="{ color: sounds[3].isActive ? 'green' : 'black' }">mdi mdi-volume-high</v-icon>
                    </v-btn>
                    
                </div>
                <br>
                <p>다음 중 어떤 소리가 물두꺼비의 소리일까요?</p>
                <div class="soundDiv">
                    <v-row class="sound-item">
                        <v-col cols="4">
                            <v-btn @click="toggleAudio(sounds[0])" fab>
                                <v-icon large  :style="{ color: sounds[0].isActive ? 'green' : 'black' }">mdi mdi-volume-high</v-icon>
                            </v-btn>
                        </v-col>
                        <v-col cols="4">
                            <v-btn @click="toggleAudio(sounds[1])" fab>
                                <v-icon large  :style="{ color: sounds[1].isActive ? 'green' : 'black' }">mdi mdi-volume-high</v-icon>
                            </v-btn>
                        </v-col>
                        <v-col cols="4">
                            <v-btn @click="toggleAudio(sounds[2])" fab>
                                <v-icon large  :style="{ color: sounds[2].isActive ? 'green' : 'black' }">mdi mdi-volume-high</v-icon>
                            </v-btn>
                        </v-col>
                    </v-row>
                    <v-row class="sound-item">
                        <v-col cols="auto">
                            <v-checkbox hide-details class="shrink ml-4 mr-1" style="transform: scale(1.5);" v-model="userResult" :value="sounds[0].value"></v-checkbox>
                        </v-col>
                        <v-col cols="auto">
                            <v-checkbox hide-details class="shrink ml-4 mr-1" style="transform: scale(1.5);" v-model="userResult" :value="sounds[1].value"></v-checkbox>
                        </v-col>
                        <v-col cols="auto">
                            <v-checkbox hide-details class="shrink ml-4 mr-1" style="transform: scale(1.5);" v-model="userResult" :value="sounds[2].value"></v-checkbox>
                        </v-col>
                    </v-row>
                </div>
                <br>
                <v-btn class="custom-submit-button mt-3 pl-7 pr-7" color="#EF8200" @click="submitSoundRes">제출하기</v-btn>
            </div>
        </div>
        <v-dialog v-model="dialog" max-width="500">
            <v-card>
                <v-card-text>
                    <v-row align="center" justify="center">
                        <v-col align="center">
                            <div style="height:70%; width:70%; display: flex; align-items: center; justify-items: center;">
                                <v-img v-if="userResult === '물두꺼비'" src="@/assets/O.png" style="max-height:100%; max-width:100%;"></v-img>
                                <v-img v-else src="@/assets/X.png" style="max-height:100%; max-width:100%;"></v-img>
                            </div>
                            <br>
                            <div v-if="userResult === '물두꺼비'" class="text-center">
                                <h3>정답입니다!</h3> 
                                <h4>확인 버튼을 눌러주세요.</h4>
                            </div>
                            <div v-else class="text-center">
                                <h3>다시 한번 풀어볼까요?</h3>
                            </div>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions class="card">
                <v-btn @click="handleDialogConfirmation(userResult === '물두꺼비')" class="ok-btn mt-3 pl-10 pr-10" color="#EF8200">확인</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="infodialog" class="infodialog">
            <v-card-text class="title">
                <h3>황장목숲길</h3>
                <img @click="infodialog = false" src="@/assets/mission/close.png" class="closeinfo">
            </v-card-text>
                <img src="@/assets/mission/missionInfo/info5.jpeg" class="pic">
        </v-dialog>

    </div>
</template>

<script>
import {Howl} from 'howler';

export default {
    props: {
        show: {
            type: Boolean,
            required: true,
        },
        result5: {
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
                { id: 1, src: "/watertoad/맹꽁이.mp3", isActive: false, howl: null, value: '맹꽁이' },
                { id: 2, src: "/watertoad/물두꺼비.mp3", isActive: false, howl: null, value: '물두꺼비' },
                { id: 3, src: "/watertoad/산개구리.mp3", isActive: false, howl: null, value: '산개구리' },
                { id: 4, src: "/watertoad/물두꺼비.mp3", isActive: false, howl: null, value: '물두꺼비' },
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
                if(this.userResult === '물두꺼비'){
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
                if (this.result5 === false){
                    //result5가 false인 경우만 'answerCorrect' 이벤트를 트리거(마커를 정답 이미지로 바꾸기 위하여)
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
        border-radius: 8px;
    }
    body{
        margin: 0;
    }
    div{
        box-sizing: border-box;
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
        bottom: 7%;
        max-height: 48%;
        overflow-y: auto;
        overflow-x: hidden;
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
    .sound {
        white-space: nowrap; /*줄바꿈 방지해 한 줄에 표시*/
    }
    .sound input[type="radio"],
    .sound audio {
        display:inline-block;
        vertical-align: middle;
        padding-left: 15px;
        padding-right: 0px;
        margin-right: 0;
        /* width: 250px; */
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
    div.col {
        flex-basis: 0;
    }
    div.v-input--selection-controls__input{
        margin-right: 16px;
        margin-left: 14px;
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