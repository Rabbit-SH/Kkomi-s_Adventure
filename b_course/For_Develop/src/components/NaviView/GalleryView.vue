<template>
  <div class="black-bg" v-if="show">
    <div class="white-bg"> 
      <v-btn icon class="close" @click="closeP">
        <v-icon>mdi-close</v-icon>
      </v-btn>
      <div class="gallery-container">
        <v-card
          class="image-container"
          v-for="(photo, index) in photos"
          :key="index"
        >
          <v-container fluid>
            <v-row dense>
              <v-col cols="12">
                <v-card>
                  <v-img
                    :src="photo"
                    height="300px"
                    cover
                  ></v-img>

                  <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn size="small" color="surface-variant" variant="text" @click="downloadPhoto(photo, index)">
                      <v-icon>mdi-download</v-icon>
                    </v-btn>
                    
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script>
// import {EventBus} from '@/EventBus.js';
import { mapState } from 'vuex';

export default {
  name: 'AppGallery',
  mounted() {
      // EventBus.$on('add-photo',this.addPhoto)
      // this.photos = JSON.parse(localStorage.getItem('photos')) || [];
  },
  props: {
      show: {
              type: Boolean,
              required: true,
          },
  },
  data(){
      return {
          // photos: [],
      };
  },
  computed:{
    ...mapState(["photos"]), // Users라는 변수명을 사용
    ...mapState({ photos: "photos" }), // 키 Users는 해당 컴포넌트에서 사용할 변수명 값은 State 값
  },
  methods: {
    closeP(){
      this.$emit('close');
    },
    downloadPhoto(photo, index) {
      const a = document.createElement('a');
      a.href = photo;
      a.download = `photo_${index}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    },
  },
  beforeDestroy() {
  // EventBus.$off('add-photo', this.photoUrl);
  // this.photos.forEach(URL.revokeObjectURL);
  },
};
</script>
<style scoped>
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
  background-color: white;
  position: absolute;
  border-radius: 8px;
  position: fixed; 
  padding: 20px;
  overflow-y: auto;
    }
.gallery-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px; /* Adjust the gap as needed */
}

.image-container {
  width: 100%; /* Set fixed width */
  height: auto; /* Set fixed height */
  overflow: hidden;
  position: relative;
  border: 1px solid gray; /* 검은색 테두리 추가 */
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* This will cover the area without stretching the image */
  cursor: pointer; /* Indicates that the image is clickable */
}
.close{

  display: flex;
  width: 5%;
  padding: 5px 5px;
  margin-top: 5px;
  background-color: #ccc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: auto; /* 왼쪽 마진을 오토로 설정해서 오른쪽으로 밀어냄 */
  justify-content: center;
  margin-bottom: 5px;
      
}
</style>