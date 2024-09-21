<template>
  <Dialog
    v-model:visible="visible"
    modal
    header="여행 경로 추천"
    class="result-modal"
  >
    <div ref="mapContainer" style="width: 100%; height: 400px"></div>
    <div class="flex-container" id="result-table">
      <!-- 여행 정보 영역 (헤더 역할) -->
      <div id="result-table-info" class="result-table-head">
        <p>여행 시작: {{ start_date }}</p>
        <p>여행 종료: {{ end_date }}</p>
        <p>여행 기간: {{ period }}일</p>
      </div>
      <!-- 드래그 가능한 영역 -->
      <div
        v-for="(clusterItems, clusterId) in groupedPositions"
        :key="clusterId"
        class="cluster-container"
      >
        <p class="cluster-title">Day {{ clusterId }}</p>
        <draggable
          :list="clusterItems"
          class="draggable-list"
          @end="updateOrder(clusterId, $event)"
          @change="onChange(clusterId, $event)"
        >
          <template #item="{ element, index, isDragging }">
            <div class="draggable-item" :class="{ 'is-dragging': isDragging }">
              <p>{{ element.order }}. {{ element.name }}</p>
              <span class="drag-handle">≡</span>
            </div>
          </template>
        </draggable>
      </div>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import draggable from "vuedraggable";
const props = defineProps<{
  data: { start_date: Date; end_date: Date; period: number; spots: [] };
}>();
const visible = defineModel<boolean>("visible", { required: true });
const mapContainer = ref(null);
let map = ref(null);
let markers = ref<{ [key: string]: any[] }>({}); // 클러스터별 마커를 저장
const positions = ref([]);
const start_date = props.data.start_date;
const end_date = props.data.end_date;
const period = props.data.period;
const overlays = ref([]);

const position_obj = ref<{ [key: string]: any[] }>({}); // 클러스터별 아이템을 저장
// 데이터를 클러스터별로 분류
props.data.spots.forEach((item) => {
  if (!position_obj.value[item.cluster]) {
    position_obj.value[item.cluster] = [];
  }
  position_obj.value[item.cluster].push({
    name: item.name,
    address: item.address,
    order: item.order,
    cluster: item.cluster,
    lat: item.lat,
    lng: item.lng,
  });
});
console.log(position_obj.value);
const groupedPositions = ref({ ...position_obj.value }); // 클러스터별 그룹화된 아이템
console.log(groupedPositions.value);
props.data.spots.forEach((item, index) => {
  positions.value.push({
    name: item.name,
    address: item.address,
    order: item.order,
    cluster: item.cluster,
    lat: item.lat,
    lng: item.lng,
  });
});
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
  clearMarkers(); // 기존 마커 및 오버레이 제거
  for (const [clusterId, items] of Object.entries(groupedPositions.value)) {
    const clusterMarkers = [];
    const clusterOverlays = [];
    for (const [index, marker] of positions.value.entries()) {
      const position = new window.kakao.maps.LatLng(marker.lat, marker.lng);
      const newMarker = new window.kakao.maps.Marker({
        position: position,
      });
      for (const item of items) {
        const position = new window.kakao.maps.LatLng(item.lat, item.lng);
        const newMarker = new window.kakao.maps.Marker({
          position: position,
        });
        newMarker.setMap(map);
        clusterMarkers.push(newMarker);
      }
      const order = marker.order === undefined ? index : marker.order;
      const content = `<div style=width:100%;padding:5px;">${order}</div>`;
      const customOverlay = new window.kakao.maps.CustomOverlay({
        position: position,
        content: content,
      });
      customOverlay.setMap(map);
      clusterOverlays.push(customOverlay);

      // 각 마커 생성 사이에 약간의 지연을 줍니다.
      await new Promise((resolve) => setTimeout(resolve, 30));
    }
    markers.value[clusterId] = clusterMarkers;
    overlays.value = overlays.value.concat(clusterOverlays); // 기존 오버레이에 추가
  }
  // 범위 재설정
  const bounds = new kakao.maps.LatLngBounds();
  // bounds.extend(
  //   new kakao.maps.LatLng(Number(marker.lat), Number(marker.lng))
  // );

  // map.setBounds(bounds);
  // await new Promise((resolve) => setTimeout(resolve, 50));
  Object.values(markers.value)
    .flat()
    .forEach((marker) => bounds.extend(marker.getPosition()));
  map.setBounds(bounds);
};

// 마커와 오버레이 제거
const clearMarkers = () => {
  Object.values(markers.value)
    .flat()
    .forEach((marker) => marker.setMap(null)); // 모든 마커 제거
  markers.value = {};

  overlays.value.forEach((overlay) => overlay.setMap(null)); // 모든 오버레이 제거
  overlays.value = [];
};

onMounted(async () => {
  await initializeMap();
});

// 드래그가 끝나면 순서에 맞게 order 필드를 업데이트
const updateOrder = () => {
  console.log("updateOrder");
  Object.keys(groupedPositions.value).forEach((clusterId) => {
    groupedPositions.value[clusterId].forEach((item, index) => {
      item.order = index + 1;
    });
  });

  // 마커를 업데이트합니다.
  addMarkers();
};

const oldCluster = ref("");
const newCluster = ref("");

const onChange = (clusterId: string, event: any) => {
  console.log("onChange");
  console.log(event);
  console.log(event.element);
  // 드래그 중에 어떤 클러스터에서 이동했는지 확인
  oldCluster.value = event.moved.oldIndex;
  newCluster.value = event.moved.newIndex;

  console.log("이전 클러스터:", oldCluster.value);
  console.log("새 클러스터:", newCluster.value);
};
</script>

<style>
.result-modal {
  width: 100%;
  max-width: 768px !important;
}
.flex-container {
  display: flex;
  width: 100%;
}

.flex-item {
  width: 50%;
  padding: 10px;
}
/* 헤더 스타일 */
.result-table-head {
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
