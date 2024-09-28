<template>
  <div class="header-container">
    <svg
      width="114"
      height="24"
      viewBox="0 0 114 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g clip-path="url(#clip0_23_91)">
        <path
          d="M40.4377 6.5549C40.4228 2.90798 37.3474 0.381348 32.8636 0.381348H23.688V20.5408H27.7202V13.1396H31.7196L36.459 20.5408H41.0349L35.9152 12.7016C38.6786 11.8286 40.4228 9.32883 40.4377 6.5549ZM33.0835 9.75192H27.7231V4.06999H33.0835C35.1397 4.06999 36.3669 5.06813 36.3788 6.71878C36.3639 8.37241 35.1397 9.76384 33.0835 9.75192Z"
          fill="white"
        />
        <path
          d="M75.3485 11.9628C75.3336 15.1717 73.7677 17.0995 71.1796 17.0995C68.5916 17.0995 67.0257 15.1747 67.0405 11.9628V0.765747H63.0084V11.9657C62.9935 17.3468 66.265 20.9252 71.1796 20.9252C76.0943 20.9252 79.3658 17.3468 79.3777 11.9657V0.765747H75.3455V11.9657L75.3485 11.9628Z"
          fill="white"
        />
        <path
          d="M82.2656 4.56165H88.1757V20.5408H92.2079V4.56165H98.0645V0.765747H82.2656V4.56165Z"
          fill="white"
        />
        <path
          d="M105.092 16.7449V12.1296H113.019V8.65848H105.092V4.56165H113.78V0.765747H101.06V20.5408H114V16.7449H105.092Z"
          fill="white"
        />
        <path
          d="M10.3256 4.39778C10.4652 4.39778 10.599 4.40076 10.7356 4.4097H19.7805V0.584001H10.7356C10.599 0.578042 10.4652 0.572083 10.3256 0.572083C4.42739 0.575062 -0.0148197 4.99964 3.71562e-05 10.8455C-0.0148197 16.6913 4.43928 21.1158 10.3523 21.1158C15.3324 21.1158 19.0793 17.9993 19.6884 13.3036C19.7449 12.8626 19.7775 12.4067 19.7775 11.9389V9.94564H10.7327V13.3065H15.6622C15.1303 15.7527 13.1692 17.2931 10.3494 17.2931C6.64405 17.2931 4.04409 14.6294 4.05597 10.8455C4.04112 7.06147 6.62919 4.39778 10.3196 4.39778H10.3256Z"
          fill="white"
        />
        <path
          d="M51.3189 0C47.26 0 43.2041 3.47412 43.2041 9.2365C43.2041 14.9989 51.3189 24.003 51.3189 24.003C51.3189 24.003 59.4338 14.9989 59.4338 9.2365C59.4338 3.47412 55.3779 0 51.3189 0ZM51.3189 13.2708C48.7962 13.2708 46.7519 11.2209 46.7519 8.69125C46.7519 6.16164 48.7962 4.11173 51.3189 4.11173C53.8416 4.11173 55.886 6.16164 55.886 8.69125C55.886 11.2209 53.8416 13.2708 51.3189 13.2708Z"
          fill="white"
        />
      </g>
      <defs>
        <clipPath id="clip0_23_91">
          <rect width="114" height="24" fill="white" />
        </clipPath>
      </defs>
    </svg>
  </div>
  <div class="header-item">
    <h2>{{ destination }} 여행</h2>
    <a>
      <div class="tooltip-container">
        <img
          src="@/assets/img/share.png"
          style="margin-right: 10px"
          class="icon"
        />
        <span v-if="tooltip" class="tooltip">공유기능을 준비중이에요.</span>
      </div>
      <div class="tooltip-container">
        <img src="@/assets/img/map.png" class="icon" />
        <span v-if="tooltip" class="tooltip"
          >일자별 지도기능을 준비중이에요.</span
        >
      </div>
    </a>
  </div>
  <span style="margin-left: 20px">{{ start_date }} - {{ end_date }}</span>
  <div
    ref="mapContainer"
    style="width: 100%; height: 400px; margin-top: 10px; margin-bottom: 10px"
  ></div>
  <div style="margin-top: 30px">
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
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from "vue-router";
import { ref, onMounted } from "vue";
import draggable from "vuedraggable";
const props = defineProps<{
  data: {
    destination: String;
    start_date: Date;
    end_date: Date;
    period: number;
    spots: Spot[];
  };
}>();
// const route = useRoute();
const router = useRouter();
// const receivedData = JSON.parse(decodeURIComponent(route.query.data));
const receivedData = props.data;
const start_date = formatDate(receivedData.start_date);
const end_date = formatDate(receivedData.end_date);
const destination = receivedData.destination;

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
const mapContainer = ref(null);
let map = ref(null);

const positions = ref<Spot[]>([]);

let markers = ref([]);
let overlays = ref([]); // Custom overlays 추가

const tooltip = ref("");

const showTooltip = (text) => {
  tooltip.value = text;
};

const hideTooltip = () => {
  tooltip.value = "";
};

receivedData.spots.forEach((item, index) => {
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

// 날짜 형식화 함수
function formatDate(strDate) {
  const date = new Date(strDate);
  const year = date.getUTCFullYear().toString().slice(-2); // 연도
  const month = String(date.getUTCMonth() + 1).padStart(2, "0"); // 월
  const day = String(date.getUTCDate()).padStart(2, "0"); // 일
  return `${year}.${month}.${day}`;
}

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

const returnPage = () => {
  router.push("/");
};
</script>

<style scoped>
.header-container {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  background-color: #3dac68;
  height: 100px;
  padding: 20px;
  width: 100vw;
  box-sizing: border-box;
  /* 패딩과 테두리를 포함한 전체 너비 및 높이 계산 */
}
.header-item {
  display: flex;
  justify-content: space-between;
  margin-left: 20px;
  margin-right: 20px;
  align-items: center;
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
.date-and-icons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5px;
}

.header-icon {
  width: 24px;
  height: 24px;
  cursor: pointer;
}
.tooltip-container {
  position: relative;
  display: inline-block;
  margin-right: 10px; /* 아이콘 사이의 간격 조절 */
}

.icon {
  cursor: pointer;
}

.tooltip {
  visibility: hidden;
  position: absolute;
  background-color: #555;
  color: #fff;
  text-align: center;
  border-radius: 5px;
  padding: 5px;
  z-index: 1;
  bottom: 125%; /* 아이콘 위쪽에 위치 */
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s;
  width: 100px; /* 툴팁 너비 조정 */
}

.tooltip-container:hover .tooltip {
  visibility: visible;
  opacity: 1;
}

.custom-button {
  position: absolute;
  /* 버튼을 부모 컨테이너의 맨 아래에 위치 */
  bottom: 20px;
  /* 창의 아래쪽에서 20px 위에 고정 */
  left: 50%;
  transform: translateX(-50%);
  /* 중앙 정렬 */
  padding: 12px, 10px, 12px, 10px;
  background-color: #a8a8a880;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 90%;
  gap: 10px;
  height: 40px;
  transform: translateX(-50%);
  /* 중앙 정렬 */

  /* 글자 및 내용 중앙 정렬 */
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
</style>
