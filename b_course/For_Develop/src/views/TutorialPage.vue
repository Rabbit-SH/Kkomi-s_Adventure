<template>
  <v-carousel hide-delimiters height="auto" 
  :cycle="false"
  :continuous="false"
  @input="handleSliderChange">
    <v-carousel-item v-for="(item, i) in items" 
    :key="i" 
    :src="item.src">
    <v-btn 
    v-show="i === 1"
    @click="startsound"
    :color="buttonPressed ? 'blue' : 'defaultColor'"
    fab
    small
    style="top: 2%; left: 2%;"
    >
    <v-icon>{{ buttonPressed ? 'mdi-volume-high' : 'mdi-volume-off' }}</v-icon> 
    </v-btn>
    <div v-show="i===1" class="source-credit">
      " 본 음성은 KT AI 보이스 스튜디오에서 제작되었습니다."
    </div>
      <v-btn x-small color="teal" dark 
      @click="goToMain" class="skipButton">Skip</v-btn>
      <v-btn x-small color="primary" dark
      class="beforeButton"
      v-if="i==0" @click="$router.push({name:'CourseChoose'})">이전으로</v-btn><!--코스 선택으로 되돌아가는 버튼-->
    </v-carousel-item>
    <!-- 마지막 페이지에만 컨트롤 버튼을 표시X -->
    <v-carousel-item v-if="!hasNext" :src="require('@/assets/tutorialView/게임시작 페이지 예시.png')">
      <div class="goToMainPage" @click="goToMain"></div>
    </v-carousel-item>

  </v-carousel>
  
</template>

<script>
export default {
  data() {
    return {
      items: [
        { src: require('@/assets/tutorialView/캐릭터 소개 예시.jpg')},
        { src: require('@/assets/tutorialView/튜토리얼1.png'),audio: require('@/assets/test1.mp3') },
        { src: require('@/assets/tutorialView/튜토리얼2.jpg')},
        { src: require('@/assets/tutorialView/튜토리얼3.jpg')},
        { src: require('@/assets/tutorialView/튜토리얼4.png') },
      ],
      currentAudio: null, // 현재 재생 중인 오디오
      started: false,
      buttonPressed: false,

    };
  },
  computed: {
    // 현재 페이지가 마지막 페이지인지 확인
    hasNext() {
      return this.$refs.carousel ? this.$refs.carousel.hasNext() : false;
    },
  },
  methods:{
    playAudio(audioSrc) {
      if (this.currentAudio) {
        this.currentAudio.pause(); // 이전 오디오 정지
      }
      this.currentAudio = new Audio(audioSrc);
      this.currentAudio.play();
    },
    goToMain() {
      if (this.currentAudio) {
        this.currentAudio.pause(); // 오디오 정지
      }
      this.$router.push({ name: 'MainView' });
    },
    startsound() {
      this.buttonPressed = !this.buttonPressed; // 버튼 상태 토글
      if (this.buttonPressed) {
        // 버튼이 활성화되면 오디오 재생
        this.playAudio(this.items[1].audio);
      } else {
        // 버튼이 비활성화되면 오디오 정지
        if (this.currentAudio) {
          this.currentAudio.pause();
        }
      }
    },
    handleSliderChange(index){
      //인덱스가 유효한지 확인
      if(index !== undefined && index >= 0){
        this.playAudio(this.items[index].audio);
      }
    }
  }
};
</script>

<style scoped>
.beforeButton{
position: absolute;
top:10px;
left: 10px;
}
.skipButton {
position: absolute;
top: 10px;
right: 10px;
}
.goToMainPage {
position: absolute;
bottom: 15%;
left: 10%;
width: 80%;
height: 10%;
}
.source-credit {
  position: absolute;
  top: 0;
  left: 0;
  font-size: 10px; /* 작은 글씨 크기 */
  color: #666; /* 글씨 색상 */
  text-align: center;
  padding: 5px;
}
</style>