<template>
  <Dialog
    v-model:visible="visible"
    modal
    header="여행결과"
    class="result-modal"
  >
    <div ref="mapContainer" style="width: 100%; height: 400px"></div>
    <div id="items">
      <p v-for="(value, index) in positions">{{ index + 1 }}. {{ value }}</p>
    </div>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";

const props = defineProps<{
  data: [];
}>();
const visible = defineModel<boolean>("visible", { required: true });
const mapContainer = ref(null);
let map = ref(null);
let markers = ref([]);
const positions = ref([]);
props.data.forEach((item, index) => {
  positions.value.push({ name: item.name, address: item.address });
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
  // const bounds = new kakao.maps.LatLngBounds();
  for (const [index, marker] of props.data.entries()) {
    const position = new window.kakao.maps.LatLng(marker.lat, marker.lng);
    const newMarker = new window.kakao.maps.Marker({
      position: position,
      clickable: true,
    });
    newMarker.setMap(map);
    markers.value.push(newMarker);

    const order = marker.order === undefined ? index : marker.order;
    const content = `<div style=width:100%;padding:5px;">${order}</div>`;
    const customOverlay = new window.kakao.maps.CustomOverlay({
      position: position,
      content: content,
    });

    customOverlay.setMap(map);
    // 각 마커 생성 사이에 약간의 지연을 줍니다.
    await new Promise((resolve) => setTimeout(resolve, 30));
    // 범위 재설정
    // bounds.extend(
    //   new kakao.maps.LatLng(Number(marker.lat), Number(marker.lng))
    // );

    // map.setBounds(bounds);
    // await new Promise((resolve) => setTimeout(resolve, 50));
  }
};

onMounted(async () => {
  await initializeMap();
});
</script>

<style>
.result-modal {
  max-width: 768px !important;
}
</style>
