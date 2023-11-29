<template>
    <div class="black-bg" v-if="show">
        <div class="white-bg">
            <img class = 'background' src= '@/assets/mission/bg_9.png'>
            <button class="close" @click="closeP">
                <img src="@/assets/mission/close.png">
            </button>
            <!-- <button class="info" @click="openinfo">
                <v-icon size="25">mdi-information-variant-circle</v-icon>
            </button> -->
            <div class="content-container" justify="center" align="center">

                <v-text-field
                    label="0000은 무엇일까요?"
                    single-line
                    outlined
                    class="textarea"
                    v-model="userResult"
                    justify="center"
                    style="width: 80%;"
                    align-items="center"
                ></v-text-field>
                
                
                <br>
                <v-btn class="custom-submit-button mt-3 pl-10 pr-10" color="#EF8200" @click="submitSoundRes">제출하기</v-btn>
            </div>
        </div>
        <v-dialog v-model="dialog" max-width="500">
            <v-card>
                <v-card-text>
                    <v-row align="center" justify="center">
                        <v-col align="center">
                            <div style="height:70%; width:70%; display: flex; align-items: center; justify-items: center;">
                                <v-img v-if="(userResult === '탄소중립') | (userResult === '탄소 중립')" src="@/assets/O.png" style="max-height:100%; max-width:100%;"></v-img>
                                <v-img v-else src="@/assets/X.png" style="max-height:100%; max-width:100%;"></v-img>
                            </div>
                            <br>
                            <div v-if="(userResult === '탄소중립') | (userResult === '탄소 중립')" class="text-center">
                                <h3>정답입니다!</h3> 
                                <h4>확인 버튼을 눌러주세요.</h4>
                            </div>
                            <div v-else class="text-center">
                                <h3>다시 한번 풀어볼까요?</h3>
                                <br>
                                <p> 탄소 배출량을 0으로 만드는 것을 </p>
                                <p><strong>탄소중립</strong>이라고 해요</p>
                                <br>
                                <p>탄소 배출량을 어떻게 하면 줄일 수 있을지</p>
                                <p>같이 생각해봐요 ~ </p>
                            </div>
                        </v-col>
                    </v-row>
                </v-card-text>
                <v-card-actions class="card">
                <v-btn @click="handleDialogConfirmation((userResult === '탄소중립')|(userResult === '탄소 중립'))" class="ok-btn mt-3 pl-10 pr-10" color="#EF8200">확인</v-btn>
                </v-card-actions>
            </v-card>
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
        result8: {
            type: Boolean,
        }
    },
    data(){
      return {
          userResult: '', //사용자 응답 저장하는 데이터
          showPopup: false, //팝업 상태
          dialog: false,
      }
    },
    methods: {
        closeP(){
            this.$emit('close');
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
                if(this.userResult === '탄소중립' || this.userResult === '탄소 중립'){
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
                if (this.result8 === false){
                    //result8가 false인 경우만 'answerCorrect' 이벤트를 트리거(마커를 정답 이미지로 바꾸기 위하여)
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
    .textarea{
        justify-content: center;
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
    ::v-deep .v-dialog { /* 지우면 안됨 */
        box-shadow: none !important;
    }
</style>