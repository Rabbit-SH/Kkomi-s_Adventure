import Vue from 'vue'
import Vuex from 'vuex'
// import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        photos: [],
        bg_photo: '',
        family: '',
    },
    getters: {
        getBGPhoto: state => state.bg_photo,
    },
    mutations: {
        addPhoto: (state, photoUrl) => {
            state.photos.push(photoUrl);
        },
        setBGPhoto: (state, photoUrl) => {
            state.bg_photo = photoUrl;
        },
        delBGPhoto: (state) => {
            state.bg_photo = null;
        },
        setFamily: (state, photoUrl) => {
            state.family = photoUrl;
        }

    },
    actions: {},
    modules: {},
    // plugins: [createPersistedState({
    //     key: 'photos', // 로컬 스토리지에 저장될 데이터의 키
    //     paths: ['photos'], // 저장할 데이터의 경로
    //     // storage: window.sessionStorage, // 세션 스토리지 사용시 이 코드 사용
    // })]

})