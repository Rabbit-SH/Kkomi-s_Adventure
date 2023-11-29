<template>
    <div class="black-bg" v-if="show">
      <div class="white-bg">
        <v-carousel hide-delimiters height="auto" class="tutorial-image" :cycle="false" :continuous="false">
          <v-carousel-item v-for="(item, i) in items" :key="i" class="tutorial-img-ca">
            <button @click="goToMain" class="skipButton">
              <img src="@/assets/tutorialView/skip.png">
            </button>
            <img :src="item.src" alt="tutorial image" width="100%" height="100%">
          </v-carousel-item>
          <!-- 마지막 페이지에만 컨트롤 버튼을 표시X -->
          <v-carousel-item v-if="!hasNext">
            <img :src="require('@/assets/tutorialView/게임시작 페이지 예시.png')" alt="last tutorial image" width="100%" height="100%">
            <div class="goToMainPage" @click="goToMain"></div>
          </v-carousel-item>
        </v-carousel>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      show: {
        type: Boolean,
      },
    },
    methods: {
      goToMain() {
        this.currentSlideIndex = 0;
        this.$emit('closeTutorial');
      },
    },
    data() {
      return {
        items: [
          { src: require('@/assets/tutorialView/캐릭터 소개 예시.jpg') },
          { src: require('@/assets/tutorialView/튜토리얼1.png') },
          { src: require('@/assets/tutorialView/튜토리얼2.jpg') },
          { src: require('@/assets/tutorialView/튜토리얼3.jpg') },
          { src: require('@/assets/tutorialView/튜토리얼4.png') },
        ],
      };
    },
    computed: {
      // 현재 페이지가 마지막 페이지인지 확인
      hasNext() {
        return this.$refs.carousel ? this.$refs.carousel.hasNext() : false;
      },
    },
  };
  </script>
  
  <style scoped>
  .black-bg {
    width: 100%;
    height: 100%;
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
  
.white-bg {
    width: 80%;
    height: auto; /* 자동으로 내용에 맞게 높이가 조절됩니다. */
    max-height: 90%; /* 최대 높이 제한을 둘 수 있습니다. */
    position: fixed;
    z-index: 1600;
    display: flex;
    flex-direction: column;
}
.tutorial-image{
  border-radius: 5px;
}  
.tutorial-img-ca {
  width: 100%;
  position: relative;
  border-radius: 5px;
}
.tutorial-image img {
    width: 100%;
    height: 100%;
    border-radius: 5px;
}
.v-window.tutorial-image.v-item-group.theme--dark.v-carousel {
  overflow: overlay; /* 혹은 다른 원하는 스타일 적용 */
}
  
.closetutorial {
    position: absolute;
    top: 15px;
    right: 25px;
    display: flex;
    width: auto;
    padding: 5px 10px;
    margin-top: 5px;
    background-color: #ccc;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-left: auto;
}
  
.goToMainPage {
    position: absolute;
    bottom: 15%;
    left: 10%;
    width: 80%;
    height: 10%;
}
  
.skipButton img{
    width: 20%;
    height: auto;
    cursor: pointer;
    position: absolute;
    top: 1%;
    right: 1%;
  }
  </style>
  