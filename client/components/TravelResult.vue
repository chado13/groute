<template>
  <Dialog
    v-model:visible="visible"
    modal
    header="여행 경로 추천"
    class="result-modal"
    style="width: 100%; max-width: 768px"
  >
    <template #header>
      <div
        style="
          display: flex;
          flex-direction: column;
          padding-bottom: 0rem;
          margin-bottom: 10px;
          margin-left: 10px;
        "
      >
        <h2 class="header">{{ destination }} 여행</h2>
        <span>{{ start_date }} - {{ end_date }}</span>
      </div>
    </template>

    <div
      ref="mapContainer"
      style="width: 100%; height: 400px; margin-top: 10px; margin-bottom: 10px"
    ></div>
    <!-- 여행 정보 영역 (헤더 역할) -->

    <div>
      <!-- 드래그 가능한 영역 -->
      <draggable
        v-model="positions"
        class="draggable-list"
        @end="updateOrder"
        :move="checkIfDraggable"
        handle=".drag-handle"
      >
        <template #item="{ element, index, isDragging }">
          <div
            :class="{
              'draggable-item': element.type === 'place',
              'non-draggable-item': element.type !== 'place',
              'is-dragging': isDragging,
            }"
            :style="getNonDraggableItemStyle(element)"
          >
            <div v-if="element.type === 'place'" class="place-item">
              <p class="place-item-order">
                {{ element.order }}
              </p>
              <p>
                {{ element.name }}
              </p>
            </div>
            <div v-else>
              {{ element.name }}
            </div>
            <span v-if="element.type === 'place'" class="drag-handle">≡</span>
          </div>
        </template>
      </draggable>
      <!-- </div> -->
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import draggable from "vuedraggable";

interface Spot {
  name: string;
  address: string;
  lat: string;
  lng: string;
  category: string;
  cluster: number;
  order: number;
  type: string;
  id: number;
}
const props = defineProps<{
  data: {
    destination: String;
    start_date: Date;
    end_date: Date;
    period: number;
    spots: Spot[];
  };
}>();
const visible = defineModel<boolean>("visible", { required: true });
const mapContainer = ref(null);
let map = ref(null);

const positions = ref<Spot[]>([]);
const start_date = props.data.start_date;
const destination = props.data.destination;
const end_date = props.data.end_date;

let markers = ref([]);
let overlays = ref([]); // Custom overlays 추가

props.data.spots.forEach((item, index) => {
  positions.value.push({
    name: item.name,
    category: item.category,
    address: item.address,
    order: item.order,
    cluster: item.cluster,
    lat: item.lat,
    lng: item.lng,
    type: item.type,
    id: item.id,
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
  clearMarkers(); // 마커 초기화
  const bounds = new kakao.maps.LatLngBounds();
  for (const [index, marker] of props.data.spots.entries()) {
    if (marker.type === "spliter") {
      continue;
    }
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
};

const clearMarkers = () => {
  markers.value.forEach((marker) => marker.setMap(null)); // 모든 마커 제거
  markers.value = [];

  overlays.value.forEach((overlay) => overlay.setMap(null)); // 모든 오버레이 제거
  overlays.value = [];
};

const updateOrder = (e) => {
  const places = positions.value.filter((spot) => spot.type === "place");

  // 필터링된 항목들에 대해 순서 업데이트
  places.forEach((item, index) => {
    item.order = index + 1; // 드래그 후 순서를 업데이트
  });

  // 전체 positions 배열에 필터링된 항목들 업데이트
  positions.value.forEach((item) => {
    if (item.type === "place") {
      const updatedItem = places.find((place) => place.id === item.id);
      if (updatedItem) {
        item.order = updatedItem.order;
      }
    }
  });
  addMarkers(); // 마커 업데이트
};

const checkIfDraggable = (event) => {
  return event.relatedContext.element.type === "place";
};

onMounted(async () => {
  await initializeMap();
});

// 각 non-draggable 항목의 색상을 지정하는 함수
const getNonDraggableItemStyle = (element) => {
  if (element.type !== "place") {
    // id에 따라 색상을 지정
    switch (element.id % 5) {
      case 0:
        return { backgroundColor: "#3DAC68" };
      case 1:
        return { backgroundColor: "#FFD027" };
      case 2:
        return { backgroundColor: "#F35B46" };
      case 3:
        return { backgroundColor: "#1581FF" };
      case 4:
        return { backgroundColor: "#B04BFF" };
    }
  }
  return {};
};

const getBackgroundColorForPlace = (element) => {
  const nonPlaceElement = positions.value.find((item) => item.type !== "place");
  return nonPlaceElement
    ? getNonDraggableItemStyle(nonPlaceElement).backgroundColor
    : "white";
};
</script>

<style scoped>
.result-modal {
  max-width: 768px;
  width: 100%;
  min-width: 360px;
}

/* .result-header-table{
  display: inline-block;
  background-color: #f1f1f1;
  padding: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  width: 100%;
} */
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
  width: 100%;
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
  padding: 8px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  background-color: #fff;
  cursor: grab;
  width: 100%;
  height: 60px;
  justify-content: space-between;
  border-radius: 4px;
  box-shadow: 0px 0px 4px 0px #00000029;
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
.drag-handle {
  cursor: move;
}
.non-draggable-item {
  padding: 0 0.5rem;
  margin-bottom: 0.5rem;
  background-color: #f8f8f8;
  width: 74px;
  height: 24px;
  line-height: 22px;
  border-radius: 12px;
  text-align: center;
  font-size: 14px;
  color: #fff;
}
.place-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.place-item-order {
  margin-right: 20px;
  margin-left: 10px;
  border-radius: 10px;
  padding: 5px;
}
</style>
