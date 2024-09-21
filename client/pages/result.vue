<template>
    <div v-if="visible" >
    <div class="header-container">
      <svg width="114" height="24" viewBox="0 0 114 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_23_91)">
        <path d="M40.4377 6.5549C40.4228 2.90798 37.3474 0.381348 32.8636 0.381348H23.688V20.5408H27.7202V13.1396H31.7196L36.459 20.5408H41.0349L35.9152 12.7016C38.6786 11.8286 40.4228 9.32883 40.4377 6.5549ZM33.0835 9.75192H27.7231V4.06999H33.0835C35.1397 4.06999 36.3669 5.06813 36.3788 6.71878C36.3639 8.37241 35.1397 9.76384 33.0835 9.75192Z" fill="white"/>
        <path d="M75.3485 11.9628C75.3336 15.1717 73.7677 17.0995 71.1796 17.0995C68.5916 17.0995 67.0257 15.1747 67.0405 11.9628V0.765747H63.0084V11.9657C62.9935 17.3468 66.265 20.9252 71.1796 20.9252C76.0943 20.9252 79.3658 17.3468 79.3777 11.9657V0.765747H75.3455V11.9657L75.3485 11.9628Z" fill="white"/>
        <path d="M82.2656 4.56165H88.1757V20.5408H92.2079V4.56165H98.0645V0.765747H82.2656V4.56165Z" fill="white"/>
        <path d="M105.092 16.7449V12.1296H113.019V8.65848H105.092V4.56165H113.78V0.765747H101.06V20.5408H114V16.7449H105.092Z" fill="white"/>
        <path d="M10.3256 4.39778C10.4652 4.39778 10.599 4.40076 10.7356 4.4097H19.7805V0.584001H10.7356C10.599 0.578042 10.4652 0.572083 10.3256 0.572083C4.42739 0.575062 -0.0148197 4.99964 3.71562e-05 10.8455C-0.0148197 16.6913 4.43928 21.1158 10.3523 21.1158C15.3324 21.1158 19.0793 17.9993 19.6884 13.3036C19.7449 12.8626 19.7775 12.4067 19.7775 11.9389V9.94564H10.7327V13.3065H15.6622C15.1303 15.7527 13.1692 17.2931 10.3494 17.2931C6.64405 17.2931 4.04409 14.6294 4.05597 10.8455C4.04112 7.06147 6.62919 4.39778 10.3196 4.39778H10.3256Z" fill="white"/>
        <path d="M51.3189 0C47.26 0 43.2041 3.47412 43.2041 9.2365C43.2041 14.9989 51.3189 24.003 51.3189 24.003C51.3189 24.003 59.4338 14.9989 59.4338 9.2365C59.4338 3.47412 55.3779 0 51.3189 0ZM51.3189 13.2708C48.7962 13.2708 46.7519 11.2209 46.7519 8.69125C46.7519 6.16164 48.7962 4.11173 51.3189 4.11173C53.8416 4.11173 55.886 6.16164 55.886 8.69125C55.886 11.2209 53.8416 13.2708 51.3189 13.2708Z" fill="white"/>
        </g>
        <defs>
        <clipPath id="clip0_23_91">
        <rect width="114" height="24" fill="white"/>
        </clipPath>
        </defs>
        </svg>
    </div>
    <div ref="mapContainer" style="width: 100%; height: 400px"></div>
    <div class="flex-container" id="result-header-table">
    <!-- 여행 정보 영역 (헤더 역할) -->
    <!-- <div id="result-table-info" class="result-table-head"> -->
        <div class="result-head"> 여행 시작: {{ start_date }}</div>
        <div class="result-head" >여행 종료: {{ end_date }}</div>
        <div class="result-head">여행 기간: {{ period }}일</div>
    <!-- </div> -->
    </div>
    <div>
    <!-- 드래그 가능한 영역 -->
    <!-- <div
        v-for="(clusterItems, clusterId) in groupedPositions"
        :key="clusterId"
        class="cluster-container"
    >
        <p class="cluster-title">Day {{ clusterId }}</p> -->
    <draggable
        v-model="positions"
        class="draggable-list"
        @end="updateOrder"
    >
        <template #item="{ element, index, isDragging }">
        <div class="draggable-item" :class="{ 'is-dragging': isDragging }">
            <p>{{ index + 1 }}. {{ element.name }}</p>
            <span class="drag-handle">≡</span>
        </div>
        </template>
    </draggable>
    <!-- </div> -->
    </div>
</div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, watch } from "vue";
  import draggable from "vuedraggable";
  import { useRoute } from 'vue-router';
  const route = useRoute()
  const visible = ref(route.query.visible === 'true');  // Initialize visible based on query parameter
console.log(route.query)
  watch(() => visible.value, async (newVisible) => {
  if (newVisible) {
    await initializeMap();  // Initialize the map or other code when visible is true
  }
});
  console.log(route.query.result_data)
//   const props = defineProps<{
//     data: { start_date: Date; end_date: Date; period: number; spots: [] };
//   }>();

  const mapContainer = ref(null);
  let map = ref(null);
  // let markers = ref<{ [key: string]: any[] }>({}); // 클러스터별 마커를 저장
  const positions = ref([]);
  
  const start_date = ref("");
  const end_date = ref("");
  const period = ref("");
  // const overlays = ref([]);
  let markers = ref([]);
  let overlays = ref([]); // Custom overlays 추가
  
  // const position_obj = ref<{ [key: string]: any[] }>({}); // 클러스터별 아이템을 저장
  // // 데이터를 클러스터별로 분류
  // props.data.spots.forEach((item) => {
  //   if (!position_obj.value[item.cluster]) {
  //     position_obj.value[item.cluster] = [];
  //   }
  //   position_obj.value[item.cluster].push({
  //     name: item.name,
  //     address: item.address,
  //     order: item.order,
  //     cluster: item.cluster,
  //     lat: item.lat,
  //     lng: item.lng,
  //   });
  // });
  
  // const groupedPositions = ref({ ...position_obj.value }); // 클러스터별 그룹화된 아이템

  watch(
  () => visible.value,
  (newVisible) => {
    console.log(route.query.result_data)
//     if (newSpots && Array.isArray(newSpots)) {
//       processSpots(newSpots);
//     }
//   },
  },
  { immediate: true }
);
// Process spots data to populate positions and clusters
const processSpots = (spotsData) => {
    start_date = route.query.result_data.start_date;
  end_date = route.query.result_data.end_date;
  period = route.query.result_data.period;
  positions.value = [];  // Clear previous data

    // Populate positions array
    positions.value.push({
      name: item.name,
      address: item.address,
      order: item.order,
      cluster: item.cluster,
      lat: item.lat,
      lng: item.lng,
    });
  };

//   const result = route.query.result_data.spots
//   result.forEach((item, index) => {
//     positions.value.push({
//       name: item.name,
//       address: item.address,
//       order: item.order,
//       cluster: item.cluster,
//       lat: item.lat,
//       lng: item.lng,
//     });
//   });
  const loadKakaoMapsScript = () => {
    return new Promise((resolve, reject) => {
      if (window.kakao && window.kakao.maps) {
        resolve(true);
      } else {
        reject("failed load kakao map");
      }
    });
  };
  
  const initializeMap = async () => {
    try {
      await loadKakaoMapsScript();
      map = new window.kakao.maps.Map(mapContainer.value, {
        center: new window.kakao.maps.LatLng(37.566826, 126.9786567),
        level: 3,
      });
      await addMarkers();
    } catch (error) {
      console.error("Failed to initialize map:", error);
    }
  };
  const addMarkers = async () => {
    clearMarkers(); // 마커 초기화
    const bounds = new kakao.maps.LatLngBounds();
    for (const [index, marker] of props.data.spots.entries()) {
      const position = new window.kakao.maps.LatLng(marker.lat, marker.lng);
      const newMarker = new window.kakao.maps.Marker({
        position: position,
      });
      newMarker.setMap(map);
      markers.value.push(newMarker);
      const order = marker.order === undefined ? index : marker.order;
      const content = `<div style="width:100%;padding:5px;">${order}</div>`;
      const customOverlay = new window.kakao.maps.CustomOverlay({
        position: position,
        content: content,
      });
      customOverlay.setMap(map);
      // const infowindow = new window.kakao.maps.InfoWindow({
      //   position: position,
      //   content: content,
      // });
      // infowindow.open(map, newMarker);
  
      // 각 마커 생성 사이에 약간의 지연을 줍니다.
      await new Promise((resolve) => setTimeout(resolve, 30));
      // 범위 재설정
      bounds.extend(position);
  
      // 약간의 지연을 추가하여 마커 생성
      await new Promise((resolve) => setTimeout(resolve, 30));
    }
    map.setBounds(bounds); // 모든 마커가 보이도록 범위 설정
      // await new Promise((resolve) => setTimeout(resolve, 50));
    }
  
  
    const clearMarkers = () => {
      markers.value.forEach((marker) => marker.setMap(null)); // 모든 마커 제거
      markers.value = [];
  
      overlays.value.forEach((overlay) => overlay.setMap(null)); // 모든 오버레이 제거
      overlays.value = [];
  };
  const updateOrder = () => {
    positions.value.forEach((item, index) => {
      item.order = index + 1; // 드래그 후 순서를 업데이트
    });
    console.log(positions.value)
    addMarkers(); // 마커 업데이트
  };
  // 마커와 오버레이 제거
  // const clearMarkers = () => {
  //   Object.values(markers.value)
  //     .flat()
  //     .forEach((marker) => marker.setMap(null)); // 모든 마커 제거
  //   markers.value = {};
  
  //   overlays.value.forEach((overlay) => overlay.setMap(null)); // 모든 오버레이 제거
  //   overlays.value = [];
  // };
  
//   onMounted(async () => {
//     await initializeMap();
//   });
  
  const oldCluster = ref("");
  const newCluster = ref("");
  const changeSpot = ref("")
  
  // // 드래그가 끝나면 순서에 맞게 order 필드를 업데이트
  // const updateOrder = () => {
  //   console.log()
  //   console.log("updateOrder");
  //   console.log(groupedPositions)
  //   console.log(changeSpot.value)
  //   console.log("before")
  //   console.log(groupedPositions.value[oldCluster.value])
  //   groupedPositions.value[oldCluster.value] = groupedPositions.value[oldCluster.value].filter(item => item.name !== changeSpot)
  //   console.log("after")
  //   console.log(groupedPositions.value[oldCluster.value])
  //   console.log(groupedPositions.value[oldCluster.value])
  //   Object.keys(groupedPositions.value).forEach((clusterId) => {
  //     groupedPositions.value[clusterId].forEach((item, index) => {
  //       console.log(item, index)
  //       item.order = index + 1;
  //     });
  //   });
  //   oldCluster.value = ""
  //   newCluster.value = ""
  //   changeSpot.value = ""
  //   // 마커를 업데이트합니다.
  //   addMarkers();
  // };
  
  
  
  const onChange = (clusterId: string, event: any) => {
    console.log("onChange");
    console.log(event);
    console.log(event.element);
    // 드래그 중에 어떤 클러스터에서 이동했는지 확인
    oldCluster.value = event.moved.oldIndex;
    newCluster.value = event.moved.newIndex;
    changeSpot.value = event.moved.element.name
  
    console.log("이전 클러스터:", oldCluster.value);
    console.log("새 클러스터:", newCluster.value);
    console.log("변경 장소:", changeSpot.value);
  };
  </script>
  
  <style scoped>
  .result-modal {
    width: 100%;
    max-width: 768px !important;
  }
  .flex-container {
    display: inline-block;
    width: 100%;
  }
  
  .flex-item {
    width: 50%;
    padding: 10px;
  }
  
  .result-header-table{
    display: inline-block;
    background-color: #f1f1f1;
    padding: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
    width: 100%;
  }
  /* 헤더 스타일 */
  .result-head {
    display: inline-block;
    background-color: #f1f1f1;
    padding: 10px;
    border-bottom: 1px solid #ccc;
    margin-bottom: 10px;
    width: 100%;
  }
  
  /* 드래그 가능한 리스트 스타일 */
  .draggable-list {
    padding: 5px;
  }
  
  .cluster-container {
    margin-bottom: 20px;
    flex-direction: column; /* 세로로 정렬 */
    width: 100%; /* 전체 넓이를 사용하여 draggable-list와 동일하게 설정 */
  }
  /* 클러스터 제목 스타일 */
  .cluster-title {
    font-weight: bold;
    margin-bottom: 10px;
    padding: 10px;
    background-color: #f9f9f9;
    width: 100%;
  }
  .draggable-list {
    display: flex;
    flex-direction: column; /* 아이템들을 세로로 쌓음 */
  }
  /* 드래그 가능한 아이템 스타일 */
  .draggable-item {
    position: relative; /* 핸들이 아이템 내에서 절대 위치를 갖도록 설정 */
    display: flex;
    align-items: center;
    padding: 15px;
    margin-bottom: 12px;
    border: 1px solid #ccc;
    background-color: #fff;
    cursor: grab;
    width: 100%;
    height: 60px;
  }
  
  /* 드래그 가능 아이콘 스타일 */
  .drag-handle {
    position: absolute; /* 절대 위치로 설정 */
    right: 10px; /* 오른쪽 경계에서 10px 떨어진 위치 */
    font-size: 20px;
    cursor: grab;
  }
  /* 드래그 중인 아이템에 대한 스타일 */
  .is-dragging {
    background-color: #e0e0e0;
    border: 2px dashed #999;
  }
  </style>
  