<template>
    <div class="black-bg" v-if="show">
        <div class="white-bg">
            <img class = 'background' src= '@/assets/mission/bg_3.png'>
            <button class="close" @click="closeP">
                <img src="@/assets/mission/close.png">
            </button>
            <button class="info" @click="openinfo">
                <v-icon size="25">mdi-information-variant-circle</v-icon>
            </button>
            <div class="content-container">
                <div class="checkboxGroup pl-10">
                    <v-checkbox
                        v-model="userResult"
                        label="파충류"
                        color="primary"
                        value="파충류"
                        hide-details
                        style="color: black; transform: scale(1.5); padding-left: 30%;"
                    ></v-checkbox>
                    <v-checkbox
                        v-model="userResult"
                        label="양서류"
                        color="success"
                        value="양서류"
                        hide-details
                        style="color: black; transform: scale(1.5); padding-left: 30%;"
                    ></v-checkbox>
                    <v-checkbox
                        v-model="userResult"
                        label="조류"
                        color="primary"
                        value="조류"
                        hide-details
                        style="color: black; transform: scale(1.5); padding-left: 30%;"
                    ></v-checkbox>
                </div>
                <br>
                <br>
                <div justify="center" align="center" >
                    <v-btn class="custom-submit-button mt-3 pl-10 pr-10" color="#EF8200" @click="submitSoundRes">제출하기</v-btn>
                </div>
            </div>
        </div>
        <v-dialog v-model="dialog" max-width="500">
            <v-card>
                <v-card-text>
                    <v-row align="center" justify="center">
                        <v-col align="center">
                            <div style="height:100%; width:100%; display: flex; align-items: center; justify-items: center;">
                                <v-img v-if="userResult === '양서류'" src="@/assets/O.png"></v-img>
                                <v-img v-else src="@/assets/X.png"></v-img>
                            </div>
                            <br>
                            <div v-if="userResult === '양서류'" class="text-center">
                                <h3>정답입니다!</h3> 
                                <h4>확인 버튼을 눌러주세요.</h4>
                            </div>
                            <div v-else class="text-center">
                                <h3>다시 한번 풀어볼까요?</h3>
                                <br>
                                <p>표지판의 QR을 한번 확인해보세요!</p>
                                <br>
                                <p>초성힌트 : ㅇ ㅅ ㄹ</p>
                            </div>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions class="card">
                <v-btn @click="handleDialogConfirmation(userResult === '양서류')" class="ok-btn mt-3 pl-10 pr-10" color="#EF8200">확인</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="infodialog" class="infodialog">
            <v-card-text class="title">
                <h3>치악산 깃대종 물두꺼비</h3>
                <img @click="infodialog = false" src="@/assets/mission/close.png" class="closeinfo">
            </v-card-text>
                <img src="@/assets/mission/missionInfo/info4.jpeg" class="pic">
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
        result3: {
            type: Boolean,
        }
    },
    data(){
      return {
          userResult: '', //사용자 응답 저장하는 데이터
          showPopup: false, //팝업 상태
          dialog: false,
          infodialog: false,
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
            if(this.userResult.trim() == ''){
                alert("답변을 입력해주세요!")
            } else {
                if(this.userResult === '양서류'){
                    // 정답 다이얼로그 표시
                    this.dialog = true;
                } else {
                    //오답 다이얼로그 표시
                    this.dialog = true;
                }
            }
        },
        handleDialogConfirmation(correct){
            this.dialog = false;
            if(correct){
                if (this.result3 === false){
                    //result3가 false인 경우만 'answerCorrect' 이벤트를 트리거(마커를 정답 이미지로 바꾸기 위하여)
                    this.$emit('answerCorrect');
                }
                this.userResult = ''; // 사용자 응답 리셋
                this.closeP();        // 다이얼로그 닫기
            }
        }

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
        bottom: 7%
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