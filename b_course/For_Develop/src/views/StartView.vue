<template>
  <div>
    <v-img :src="require('@/assets/tutorialView/표지 예시.png')"
    @click="$router.push({name:'ChooseCourse'})"></v-img>
    <div justify="center" align="center" class="text-container">
      <p class="text"> 화면을 클릭해주세요 ! </p>
    </div>
  </div>
</template>

<script>
export default {
}
</script>

<style>
.text-container {
  position: absolute;
  bottom: 3%; /* 세로 가운데 정렬을 위해 50%로 설정 */
  left: 50%; /* 가로 가운데 정렬을 위해 50%로 설정 */
  transform: translate(-50%, -50%); /* 정확한 중앙 정렬을 위한 transform */
  text-align: center; /* 가운데 정렬을 위해 텍스트를 가운데 정렬 */
  color: gray; /* 글씨 색상을 회색으로 설정 */
  opacity: 0.6;
}
.v-application{
  font-family: 'knps_kkomiregular' !important;
  font-size: 20px;
}
</style>