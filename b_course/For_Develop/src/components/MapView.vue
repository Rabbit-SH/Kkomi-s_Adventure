<template>
  <!-- :maxBounds="maxBounds" -->
  <div class="main">    
    <l-map
      style="height: 100%; width: 100%"
      :center="center"
      :zoom="zoom"
      :zoomAnimation=true
      :options="mapOptions"
      
      class="map" 
      ref="map"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @update:bounds="boundsUpdated"
      @moveend="handlemoveend" 
      @movestart="handlemovestart"
    >

    <div class="logo">
      <img :src="require('@/assets/Icons/logo.png')">
      <div class="mission-current">
        {{ completedMissionsCount }}/{{ totalMissions }}
      </div>
    </div>
    <v-btn
      elevation="2"
      icon
      :color="isZoom ? 'red' : 'blue'"
      class="my-location-button"
      @click="ZoomInToCurrentPosition"
      height = "33px"
      width = "33px"
      style="border-radius: 50%; background-color: white;"
    >
      <v-icon size = "28">mdi-crosshairs-gps</v-icon>
    </v-btn>

      <m1 :show="popVal1" @close="closeP(1)" @answerCorrect="updateResult(1)" class="popup" :class="{'show':popVal1}" />
      <m2 :show="popVal2" @close="closeP(2)" @answerCorrect="updateResult(2)" class="popup" :class="{'show':popVal2}" />
      <m3 :show="popVal3" @close="closeP(3)" @answerCorrect="updateResult(3)" class="popup" :class="{'show':popVal3}" />
      <m4 :show="popVal4" @close="closeP(4)" @answerCorrect="updateResult(4)" class="popup" :class="{'show':popVal4}" />
      <m5 :show="popVal5" @close="closeP(5)" @answerCorrect="updateResult(5)" class="popup" :class="{'show':popVal5}" />
      <m6 :show="popVal6" @close="closeP(6)" @answerCorrect="updateResult(6)" class="popup" :class="{'show':popVal6}" />
      <m7 :show="popVal7" @close="closeP(7)" @answerCorrect="updateResult(7)" class="popup" :class="{'show':popVal7}" />
      <m8 :show="popVal8" @close="closeP(8)" @answerCorrect="updateResult(8)" class="popup" :class="{'show':popVal8}" />
      <m9 :show="popVal9" @close="closeP(9)" @answerCorrect="updateResult(9)" class="popup" :class="{'show':popVal9}" />
      <m10 :show="popVal10" @close="closeP(10)" @answerCorrect="updateResult(10)" class="popup" :class="{'show':popVal10}" />

      <GiftView :show="allResValue" :class="{'show': allRes}" @closeGift="closeLast" ref="GiftView"/>
      
      <LMarker v-for="m in mainplacemarkers" :key="m.id+10" :lat-lng="m.coordinates" :icon="getplaceIcon(m.id)" />

      <LMarker
        :key="markers[0].id"
        :lat-lng="markers[0].coordinates"
        @click="openP(0)"
        :icon="duduIcon" />

      <LMarker
        :key="markers[1].id"
        :lat-lng="markers[1].coordinates"
        @click="openP(1)"
        :icon="result2 ? customIcon: defaultIcon" />

      <LMarker
        :key="markers[2].id"
        :lat-lng="markers[2].coordinates"
        @click="openP(2)"
        :icon="result3 ? customIcon: defaultIcon" 
        v-if="result2 === true" />

      <LMarker
        :key="markers[3].id"
        :lat-lng="markers[3].coordinates"
        @click="openP(3)"
        :icon="result4 ? customIcon: defaultIcon"
        v-if="result3 === true" />

      <LMarker
        :key="markers[4].id"
        :lat-lng="markers[4].coordinates"
        @click="openP(4)"
        :icon="result5 ? customIcon: defaultIcon" 
        v-if="result4 === true" />
      
      <LMarker
        :key="markers[5].id"
        :lat-lng="markers[5].coordinates"
        @click="openP(5)"
        :icon="result6 ? customIcon: defaultIcon" 
        v-if="result5 === true" />

      <LMarker
        :key="markers[6].id"
        :lat-lng="markers[6].coordinates"
        @click="openP(6)"
        :icon="result7 ? customIcon: defaultIcon" 
        v-if="result6 === true" />

      <LMarker
        :key="markers[7].id"
        :lat-lng="markers[7].coordinates"
        @click="openP(7)"
        :icon="result8 ? customIcon: defaultIcon" 
        v-if="result7 === true" />

      <LMarker
        :key="markers[8].id"
        :lat-lng="markers[8].coordinates"
        @click="openP(8)"
        :icon="result9 ? customIcon: defaultIcon" 
        v-if="result8 === true" />

      <LMarker
        :key="markers[9].id"
        :lat-lng="markers[9].coordinates"
        @click="openP(9)"
        :icon="result10 ? customIcon: defaultIcon" 
        v-if="result9 === true" />

      <l-circle :lat-lng="currentPos" :radius=circle.radius :color=circle.color :fillColor=circle.fillColor :weight=5 :fillOpacity=1 />

      <div class="navi-bar">
        <div class="navi">
          <img 
          :src="require('@/assets/Icons/navi1.png')" 
          style="width: 28%; margin-left: 5%;" 
          @click="showTutorialPopup"
          class="story"
        >
        <img 
          :src="require('@/assets/Icons/navi2.png')" 
          style="width: 28%;" 
          @click="InfoChiak" 
          class="story"
        >
        <img 
          :src="require('@/assets/Icons/navi3.png')" 
          style="width: 28%;" 
          @click="getSafe" 
          class="safe"
        >
      </div>
      <div class="ai">
        <img 
          :src="require('@/assets/Icons/navi4.png')" 
          @click="$router.push({name: 'AIView'})" 
          class="uploadImg"
        >
      </div>      
      </div>
        
      <l-tile-layer :url="url" />

        <TutorialView :show="showtutorial" 
            @closeTutorial="closeTutorial"
            @openTutorial="showTutorialPopup" />
        <SafeView :show="showSafe" @close="closeSafe" />
        <InfoChiakView :show="showInfoChiak" class="infoChiak" :class="{'show': showInfoChiak}" @closeTutorial="closedChiak"/>

      <div  class="animated-marker" v-show="isGift">
        <img :src="require('@/assets/present.png')" 
        @click="$router.push({name: 'FinalView'})">
      </div>

    </l-map>
  </div>
</template>
   
<script>
import { LMap, LTileLayer, LMarker, LCircle } from 'vue2-leaflet';
import L from 'leaflet';
import { Icon } from 'leaflet';

import m1 from '../components/mission/m1View.vue';
import m2 from '../components/mission/m2View.vue';
import m3 from '../components/mission/m3View.vue';
import m4 from '../components/mission/m4View.vue';
import m5 from '../components/mission/m5View.vue';
import m6 from '../components/mission/m6View.vue';
import m7 from '../components/mission/m7View.vue';
import m8 from '../components/mission/m8View.vue';
import m9 from '../components/mission/m9View.vue';
import m10 from '../components/mission/m10View.vue';

import GiftView from '../components/GiftView.vue';

import 'leaflet/dist/leaflet.css';
import 'leaflet-gpx';

import markerImg from 'leaflet/dist/images/marker-icon.png';
import markerShadowImg from 'leaflet/dist/images/marker-shadow.png';
import markerRetinaImg from 'leaflet/dist/images/marker-icon-2x.png';

import SafeView from './NaviView/SafeView.vue';
import TutorialView from './NaviView/TutorialView.vue';
import InfoChiakView from './NaviView/InfoChiakView.vue';


// 결과를 세션 스토리지에 저장하는 함수
function saveResultsToLocalStorage(results) {
  sessionStorage.setItem('missionResults', JSON.stringify(results));
}

// 세션 스토리지에서 결과를 가져오는 함수
function getResultsFromSessionStorage() {
  const resultsJSON = sessionStorage.getItem('missionResults');
  return resultsJSON ? JSON.parse(resultsJSON) : {};
}

export default {

  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> '
                    + '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
      // center: [37.4148974953341, 128.050171136856],
      center: [37.4098407388340, 128.048754930496],
      zoom: 15, // 초기 확대 레벨
      previousZoom : null, //현재의 확대 레벨
      bounds: null, //지도 경계가 변경될 때 발생하는 이벤트(드래그되거나 확대/축소 시 발생)
      maxBounds:[
        [37.3721675168233, 128.0170751794774], //남서쪽 경계
        [37.46310508072958, 128.0814481958348] //북동쪽 경계
      ],

      popVal1 : false, //pop1이 열려있나 닫혀있나 여부 저장(default=false)
      popVal2 : false,
      popVal3 : false,
      popVal4 : false,
      popVal5 : false,
      popVal6 : false,
      popVal7 : false,
      popVal8 : false,
      popVal9 : false,
      popVal10 : false,

      result1: false,
      result2: false,
      result3: false,
      result4: false,
      result5: false,
      result6: false,
      result7: false,
      result8: false,
      result9: false,
      result10: false,

      allResValue: false,

      isZoomIn: false, //줌인이 된 상태인지 아닌지 확인(팝업창 띄우기 위한 변수)
      isZoom : false, //내 위치 버튼을 위한 줌인 상태 확인 변수
      isGift: false, //마지막 모든 미션 수행 후 선물 버튼(한국화 변환 + 세그멘테이션)을 나타낼 변수
      currentPos: [0,0], // 실시간 내 위치 변화 저장 변수
      showInfoChiak: false,

      isCredit: false,
      showSafe: false,
      showtutorial: false,

      ismoving: false,
      ismoveend: false,
      positionObj: {
        latitude: 0,
        longitude: 0
      },
      geooptions: {
        enableHighAccuracy: true,
        maximumAge: 0,
        timeout: Infinity
      },
      mapOptions: {
        minZoom: 13, //최소 줌 레벨 설정
        maxZoom: 18,  //최대 줌 레벨 설정
        zoomControl: false, // 줌 컨트롤러 위치를 바꿔줄 예정(왼쪽 상단 -> 왼쪽 하단)
      },

      markers: [
        {id:1, coordinates: [37.4148974953341, 128.050171136856], name:'치악산 체험학습관 맛보기 미션'},
        {id:2, coordinates: [37.4047839823339, 128.047338724136], name:'황장금표'},
        {id:3, coordinates: [37.40485112, 128.04897584], name:'황장목숲길 안내판'},
        {id:4, coordinates: [37.403465098361, 128.048915863037], name:'데크길1: 가족사진'},
        {id:5, coordinates: [37.402270, 128.050203], name:'데크길 2 : 꺾인 후 지점'},
        {id:6, coordinates: [37.3992934, 128.0498706], name:'구룡사'},
        {id:7, coordinates: [37.39793653, 128.05143569], name:'돌탑 미션'},
        {id:8, coordinates: [37.3972176621091, 128.051402270794], name:'범람로 시작 전 표지판'},
        {id:9, coordinates: [37.3962118870025, 128.051946759224], name:'탄소중립 미션'},
        {id:10, coordinates: [37.3943772, 128.05353051], name:'솔비로길(야생화원)'},
      ],
      //주요 위치 마커 위치정보와, 이름
      mainplacemarkers: [
        {id:1, coordinates: [37.415178702643,128.050192594528], name:"치악산체험학습관"},
        {id:2, coordinates: [37.408346344485,128.044876456261], name:"구룡자동차야영장"},
        {id:3, coordinates: [37.4050247453998,128.047234117985], name:"황장금표"},
        {id:4, coordinates: [37.405188804745, 128.049248456955], name:"황장목숲길"},
        {id:5, coordinates: [37.3996361550487, 128.049114346504], name:"구룡사"},
        {id:6,coordinates: [37.3949972677172, 128.053389787674], name:"금강솔빛생태학습원"},
        {id:7, coordinates: [37.3943686412347,128.053818941116], name:"솔비로길(야생화원)"},
      ],
      placeICON1: new Icon({
        iconUrl: require('@/assets/mainplace/치악산체험학습관.png'),
        iconSize: [80, 80],
        iconAnchor: [70,40]
      }),
      placeICON2: new Icon({
        iconUrl: require('@/assets/mainplace/구룡자동차야영장.png'),
        iconSize: [80, 80],
        iconAnchor: [16,32]
      }),
      placeICON3: new Icon({
        iconUrl: require('@/assets/mainplace/황장금표.png'),
        iconSize: [80, 80],
        iconAnchor: [40,70]
      }),
      placeICON4: new Icon({
        iconUrl: require('@/assets/mainplace/황장목숲길.png'),
        iconSize: [80, 80],
        iconAnchor: [0,20]
      }),
      placeICON5: new Icon({
        iconUrl: require('@/assets/mainplace/구룡사.png'),
        iconSize: [80, 80],
        iconAnchor: [40,40]
      }),
      placeICON6: new Icon({
        iconUrl: require('@/assets/mainplace/금강솔빛생태학습원.png'),
        iconSize: [80, 80],
        iconAnchor: [40,80]
      }),
      placeICON7: new Icon({
        iconUrl: require('@/assets/mainplace/솔비로길(야생화원).png'),
        iconSize: [80, 70],
        iconAnchor: [0,35]
      }),
      defaultIcon: new Icon({  // 지도의 마커 사용자 지정 아이콘(기본 디폴트 아이콘)
        iconUrl: require('@/assets/Icons/qa.png'),
        iconSize: [50, 65],
        iconAnchor: [16,32]
      }),
      customIcon: new Icon({  // 정답 시 바뀔 아이콘
        iconUrl: require('@/assets/Icons/marker.png'),
        iconSize: [45, 45],
        iconAnchor: [16,32]
      }),
      duduIcon: new Icon({  // 정답 시 바뀔 아이콘
        iconUrl: require('@/assets/Icons/맛보기_꺼비.png'),
        iconSize: [70, 60],
        iconAnchor: [16,32]
      }),
      circle: { radius: 23, color: 'white', fillColor: 'red', weight: 3}
    };
  },
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LCircle,
    m1,
    m2,
    m3,
    m4,
    m5,
    m6,
    m7,
    m8,
    m9,
    m10,
    InfoChiakView,
    GiftView,
    SafeView,
    TutorialView,
  },
  mounted(){
    delete Icon.Default.prototype._getIconUrl;
    Icon.Default.mergeOptions({ //marker-icon-2x.png 이미지 파일을 못찾는 에러 제거 코드
      iconRetinaUrl: markerRetinaImg,
      iconUrl: markerImg,
      shadowUrl: markerShadowImg,
    });

    this.$refs.map.mapObject.attributionControl.setPrefix(''); // attribution을 제거하는 코드

    // gpx 파일을 위한 코드
    this.loadGPX();

    // 현재 위치 불러오는 코드
    this.getCurrentPosition();
  },
  methods: {
    //튜토리얼 팝업창
    showTutorialPopup(){
      this.showtutorial = true;
      this.showSafe = false;
      this.showInfoChiak = false;
      if (this.$refs.map && this.$refs.map.mapObject) {
          this.$refs.map.mapObject.dragging.disable(); //사용자가 마우스나 터치로 지도를 드래그하는 것을 방지
          this.$refs.map.mapObject.scrollWheelZoom.disable(); //사용자가 마우스 휠로 지도를 확대/축소하는 것을 방지
        }
    },
    closeTutorial(){
      this.showSafe = false;
      this.showtutorial = false;
      this.showInfoChiak = false;
      if (this.$refs.map && this.$refs.map.mapObject) {
      this.$refs.map.mapObject.dragging.enable();
      this.$refs.map.mapObject.scrollWheelZoom.enable();
      }
    },
    //치악산 설명 팝업창
    InfoChiak(){
      this.showInfoChiak = true;
      this.showSafe = false;
      this.showtutorial = false;
      if (this.$refs.map && this.$refs.map.mapObject) {
          this.$refs.map.mapObject.dragging.disable(); //사용자가 마우스나 터치로 지도를 드래그하는 것을 방지
          this.$refs.map.mapObject.scrollWheelZoom.disable(); //사용자가 마우스 휠로 지도를 확대/축소하는 것을 방지
        }
    },
    
    closedChiak(){
      this.showInfoChiak = false;
      this.showSafe = false;
      this.showtutorial = false;
      if (this.$refs.map && this.$refs.map.mapObject) {
      this.$refs.map.mapObject.dragging.enable();
      this.$refs.map.mapObject.scrollWheelZoom.enable();
      }
    },

    //안전수칙 팝업창
    getSafe(){
      this.showSafe = true;
      this.showtutorial = false;
      this.showInfoChiak = false;
      if (this.$refs.map && this.$refs.map.mapObject) {
          this.$refs.map.mapObject.dragging.disable(); //사용자가 마우스나 터치로 지도를 드래그하는 것을 방지
          this.$refs.map.mapObject.scrollWheelZoom.disable(); //사용자가 마우스 휠로 지도를 확대/축소하는 것을 방지
        }
    },
    closeSafe(){
      this.showSafe = false;
      this.showtutorial = false;
      this.showInfoChiak = false;
      if (this.$refs.map && this.$refs.map.mapObject) {
        this.$refs.map.mapObject.dragging.enable();
        this.$refs.map.mapObject.scrollWheelZoom.enable();
      }
    },
    
    closeModal(){
      this.showModal = false;
    },

    zoomUpdated (zoom) {
      this.zoom = zoom;
    },
    centerUpdated (center) {
      this.center = center;
    },
    boundsUpdated(bounds) {
      this.bounds = bounds;
    },
    openP(index){
      if(! this.isZoomIn){
        this.previousZoom = this.zoom;
        // 먼저 줌인 액션 실행
        const marker = this.markers[index];
        this.$refs.map.mapObject.setZoomAround(marker.coordinates, 36);
        this.isZoomIn = true;
      }
      // 0.8초 뒤 팝업 열기
      setTimeout(()=>{this['popVal' + (index+1)] = true;}, 800);

      // 지도의 드래그와 스크롤 줌 비활성화
      if (this.$refs.map && this.$refs.map.mapObject) {
      this.$refs.map.mapObject.dragging.disable(); //사용자가 마우스나 터치로 지도를 드래그하는 것을 방지
      this.$refs.map.mapObject.scrollWheelZoom.disable(); //사용자가 마우스 휠로 지도를 확대/축소하는 것을 방지
    }

    },
    closeP(idx){
      this.popVal1 = false;
      this.popVal2 = false;
      this.popVal3 = false;
      this.popVal4 = false;
      this.popVal5 = false;
      this.popVal6 = false;
      this.popVal7 = false;
      this.popVal8 = false;
      this.popVal9 = false;
      this.popVal10 = false;
      
      // 지도의 드래그와 스크롤 줌 활성화
      if (this.$refs.map && this.$refs.map.mapObject) {
      this.$refs.map.mapObject.dragging.enable();
      this.$refs.map.mapObject.scrollWheelZoom.enable();
      }

    setTimeout(() => {
      if (this.isZoomIn && idx < 10 && idx > 1) {
        // 팝업이 닫힌 후 줌 아웃(원래 줌 레벨로 돌아가기)
        const lat_ = (this.markers[idx-1].coordinates[0] + this.markers[idx].coordinates[0])/2;
        const lng_ = (this.markers[idx-1].coordinates[1] + this.markers[idx].coordinates[1])/2;
        this.$refs.map.mapObject.panTo([lat_, lng_], { duration: 0.3 });
        this.$refs.map.mapObject.setView([lat_, lng_], this.previousZoom);
        this.isZoomIn = false;
      } else if (this.isZoomIn && idx === 1){
        this.$refs.map.mapObject.panTo(this.markers[idx].coordinates, { duration: 0.3 });
        this.$refs.map.mapObject.setView(this.markers[idx].coordinates, 15);
        this.isZoomIn = false;
      }}, 300);

      if (idx === 10){
        this.allRes();
        this.$refs.map.mapObject.setView(this.markers[4].coordinates, 15);
      }
    }, 

    getPositionValue(pos) {
      this.positionObj.latitude = pos.coords.latitude;
      this.positionObj.longitude = pos.coords.longitude;
      //현재 위치 값을 currentPost에 저장함.
      this.currentPos = [this.positionObj.latitude, this.positionObj.longitude];

      // 이전 마커가 있다면 삭제 (안하면 위치 변동될때마다 계속 마커가 찍힘)
      if (this.$refs.map && this.$refs.map.mapObject) {
        if(this.marker){
          this.$refs.map.mapObject.removeLayer(this.marker)
        }
      }
      //현위치 마크가 클릭 되있다면, 중심을 계속 잡아줌.
      if(this.isZoom){
        this.Zoom =17;
        this.$refs.map.mapObject.setView(this.currentPos, this.Zoom); 
      }
    },
    getCurrentPosition(){
      if(!navigator.geolocation){
        alert('위치 정보를 찾을 수 없습니다.')
      } else {
        //위치 업데이트 시 호출되는 함수 getPositionValue, 오류 발생 시 경고메세지 표시, 추가 옵션 : 높은퀄리티의 위치정보 => 전력소모량 높음.
        navigator.geolocation.watchPosition(this.getPositionValue,
        ()=>alert('위치 정보를 찾을 수 없습니다.(watchpPsition)'),this.geooptions)
      }
    },
    //움직일때만 발생
    handlemovestart() {
      this.ismoving = true;
      if(this.isZoom){
        this.isZoom = false;
      }
    },
    //맵이동이 끝나면 발생.
    handlemoveend() {
      this.ismoveend = true;
      if(this.ismoving){
        this.ismoving = false;
      }
    },
    //현재 위치로 줌인 하는 기능.
    ZoomInToCurrentPosition(){
      //마우스에서 클릭이 떼졌을때, 작동.
      if(!this.isZoom){
        this.Zoom = 17;
        this.$refs.map.mapObject.setView(this.currentPos, this.Zoom);
        //현위치로 이동이 끝나면, true로 바꿔줌. moveend를 사용.
        if(this.ismoveend){
          this.isZoom = true;
          this.ismoveend = false;
        }
      }else{
        this.isZoom = false;
      }
    },

    goToCenter(){
      this.$refs.map.mapObject.setView([37.408473, 128.045787],14);
    },
    loadGPX(){
      //.gpx 파일 로드 및 지도에 표시
      const gpxUrl = process.env.BASE_URL + '1108 치악산 GPS탐방로.gpx'
      fetch(gpxUrl)
      .then(response => response.text())
      .then(data => {
          // GPX 트랙 파싱
        const gpx = new DOMParser().parseFromString(data, 'text/xml');
        const trackCoords = [];
        
        // 트랙 세그먼트 추출
        const trkseg = gpx.getElementsByTagName('trkpt');
        for (let i = 0; i < trkseg.length; i++) {
          const lat = parseFloat(trkseg[i].getAttribute('lat'));
          const lon = parseFloat(trkseg[i].getAttribute('lon'));
          trackCoords.push([lat, lon]);
        }
        
        // 새로운 폴리선(선) 생성
        const polyline = L.polyline(trackCoords, { color: '#C4DEFF', weight: 15, opacity: 0.8 });

        // 맵에 폴리선 추가
        polyline.addTo(this.$refs.map.mapObject);

        // 지도 중심과 확대 설정 (트랙에 맞게 조절)
        // this.$refs.map.mapObject.fitBounds(polyline.getBounds());
        this.$refs.map.mapObject.setView(this.center, this.zoom);
      })
      .catch(error => {
        console.error('Error loading GPX:', error);
      });
    },

    updateResult(id){
      this['result' + (id)]= true;
      const results = {
        result1: this.result1,
        result2: this.result2,
        result3: this.result3,
        result4: this.result4,
        result5: this.result5,
        result6: this.result6,
        result7: this.result7,
        result8: this.result8,
        result9: this.result9,
        result10: this.result10,
      };
      saveResultsToLocalStorage(results);
    },
    closeLast(){
      this.allResValue = false;

      this.isGift = true;
    },

    allRes(){
      if(this.result2 && this.result3 && this.result4 && this.result5 && this.result6 && this.result7 && this.result8 && this.result9 && this.result10){
        this.allResValue = true;
      }
      return this.allResValue;
    },
    getplaceIcon(id){
      return this['placeICON' + (id)]  // 안내아이콘을 반환하는 함수
    }
  },
  computed:{
    completedMissionsCount() {
      return [this.result2, this.result3, this.result4, this.result5, this.result6, this.result7, this.result8, this.result9, this.result10].filter(Boolean).length;
    },
    totalMissions() {
      return 9; // 전체 미션의 수
    }
  },
  created(){
    const storedResults = getResultsFromSessionStorage();
    for (const key in storedResults) {
      if (Object.hasOwnProperty.call(storedResults, key)) {
        this[key] = storedResults[key];
      }
    }
  }
}
</script>

<style scoped>

  .animated-marker {
    animation: bounce 1s infinite;
    z-index: 1001;
    position: absolute;
    left: 25%;
    top: 35%;
  }
  .animated-marker img{
    width: 70%;
    height: 80%;
  }
  .map {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow :hidden
  }
  .popup{
    /* 트랜지션 속성을 추가하여 부드러운 나타남 및 사라짐 만들기 */
    transition: opacity 0.5s; 
    opacity: 0; /*초기에 투명상태로 설정*/
  }
  .popup.show{
    opacity: 1; /*나타날 때 투명도를 1로 설정하여 부드럽게 나타나게 함*/
  } 
  
  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-30px);
    }
    60% {
      transform: translateY(-15px);
    }
  }
  .navi-bar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}
.navi {

  align-items: center;
  justify-content: center;
  flex: 0 0 70%; /* flex-grow: 0, flex-shrink: 0, flex-basis: 70% */
  align-self: flex-end; /* 하단 정렬 */
  margin-bottom: 5%;
  margin-left: 2%;
}
.ai {
  flex: 0 0 30%;
  margin-bottom: 5%;
  margin-right: 2%;

}
.navi-bar img {
  width: 75%; /* 이미지가 부모 컨테이너의 너비에 맞게 조정 */
  margin: 0 5px;
}
  .logo {
    position: absolute; /* 절대 위치 */
    top: 1%; /* 상단에 위치 */
    left: 50%; /* 화면의 가로 중앙에 위치 */
    transform: translateX(-50%); /* X축으로 -50% 이동하여 정확한 중앙 정렬 */
    z-index: 1000; /* 다른 요소들 위에 표시 */
    text-align: center; /* 텍스트 중앙 정렬 */
    width: 100%;
  }
  .logo img{
    width: 100%;
    height: auto;
  }
  .mission-current {
    position: absolute; /* mission 요소 내에서 절대 위치 설정 */
    top: 49%; 
    left: 16%;
    transform: translate(-50%, -50%); /* 정확한 중앙 정렬을 위해 */
    z-index: 1000; /* 이미지 위에 오도록 z-index 설정 */
    font-size: 20px; /* 폰트 크기 */
    color: black; /* 폰트 색상 */
  }
  .my-location-button {
    z-index: 1001;
    position: absolute;
    top: 10%;
    left: 5%;
    padding: 0px;
    border-radius: 3px;
    text-align: center;
  }

</style>