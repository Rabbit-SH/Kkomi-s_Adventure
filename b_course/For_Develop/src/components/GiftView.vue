<template>
  <div class="black-bg" v-if="show">
    <v-carousel v-model="currentSlideIndex" hide-delimiters class="gift-img"
    :continuous="false"
    :cycle="false"
    height="auto" >
      <v-carousel-item
        v-for="slide in slides"
        :key="slide.id"
        :src="slide.image"
        class="gift-slide"
        :style="{ backgroundColor: slide.backgroundColor }"
        >
        <button class="close" @click="closeGiftView" v-if="currentSlideIndex === slides.length - 1">
      </button>
      </v-carousel-item>
    </v-carousel>
    
  </div>
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {
      currentSlideIndex: 0,
      slides: [
        { id: 1, image: require('@/assets/giftView/gift1.png'), backgroundColor: '#white' },
        { id: 2, image: require('@/assets/giftView/gift2.png'), backgroundColor: '#white' },
        { id: 3, image: require('@/assets/giftView/gift3.png'), backgroundColor: '#white' },
      ],
    };
  },
  methods: {
    closeGiftView() {
      this.currentSlideIndex = 0;
      this.$emit('closeGift');
    },
  },
};
</script>

<style scoped>
.black-bg {
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

.gift-img {
  width: 100%;
  height: 100%;
}

.gift-slide {
  display: flex;
  align-items: center;
  justify-content: center;
}

.close {
  position: absolute;
  left: 50%; /* 중앙 정렬을 위해 왼쪽에서 50% 위치에 배치 */
  transform: translateX(-50%); /* 버튼의 너비의 절반만큼 왼쪽으로 이동 */
  bottom: 10%; /* 아래쪽에서 10% 위치 */
  border: none;
  width: 90%;
  height: 10%;
}
</style>
