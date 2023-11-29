<template>
    <div class="black-bg" v-if="show">
        <div class="white-bg">  
            <v-carousel hide-delimiters class="tutorial-img" height="auto" :cycle="false" :continuous="false">
                <v-carousel-item
                    v-for="slide in slides"
                    class="tutorial-img-ca"
                    :key="slide.id">
                    <button class="closetutorial text-center" @click="closetutorial">X</button> 
                    <img :src="slide.image" alt="tutorial image" width="100%" height="100%">
                </v-carousel-item>
            </v-carousel>
        </div>
    </div>
</template>


<script>
export default {
    props:{
        show: {
                type: Boolean,
                required: true,
            },

    },
    data(){
        return{
            currentSlideIndex: 0,

            slides: [
                {id:1, image : require('@/assets/safeView/safe1.png'), backgroundColor: 'white'},
                {id:2, image : require('@/assets/safeView/safe2.png'), backgroundColor: 'white'},
            ],

            checkedExercise: false,
            checkedEquipment: false,
        }
    },
    methods: {
        closetutorial(){
            this.currentSlideIndex = 0;
            this.$emit('close');
        },

    },
}
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
        width: 80%;
        height: auto;
        max-height: 90%;
        position: fixed;
        z-index: 1600;
        display: flex;
        flex-direction: column;
    }
    .tutorial-img{
        border-radius: 5px;
    }
    .tutorial-img-ca img{
        width:100%;
        height: 100%;
        border-radius: 5px;
    }
    .v-window.tutorial-img.v-item-group.theme--dark.v-carousel {
        overflow: overlay;
    }
    .tutorial-img-ca {
        width: 100%;
        position: relative;
        border-radius: 5px;
    }
    .closetutorial{
        width: 20px;
        height: 20px;

        background-color: #ccc;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;

        justify-content: center;
        align-items: center;
        position:absolute;
        top:10px;
        right:10px;
    }

</style>