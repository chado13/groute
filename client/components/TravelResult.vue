<template>
  <Dialog
    v-model:visible="visible"
    modal
    header="여행결과"
    class="result-modal"
  >
    <!-- <KakaoMap :lat="coordinate.lat" :lng="coordinate.lng" :draggable="true">
      <KakaoMapMarker
        :lat="coordinate.lat"
        :lng="coordinate.lng"
      ></KakaoMapMarker>
    </KakaoMap> -->
    <KakaoMap :lat="37.566826" :lng="126.9786567">
      <KakaoMapMarker
        v-for="(marker, index) in props.data"
        :order="marker.order === undefined ? index : marker.order"
        :lat="marker.lat"
        :lng="marker.lng"
        :clickable="true"
      />
    </KakaoMap>
  </Dialog>
</template>

<script setup lang="ts">
import { marked } from "marked";
import { Loader } from "@googlemaps/js-api-loader";
import { until } from "@vueuse/core";
import { KakaoMap, KakaoMapMarker } from "vue3-kakao-maps";

const runtimeConfig = useRuntimeConfig();
const mapApi = runtimeConfig.public.mapApi;
const props = defineProps<{
  data: [];
}>();
const visible = defineModel<boolean>("visible", { required: true });

const mapEl = ref<HTMLElement | null>(null);

// const loader = new Loader({
//   apiKey: mapApi, // 환경 변수에서 API 키를 가져옵니다.
//   version: "weekly",
//   libraries: ["maps"], // 필요한 라이브러리 옵션을 설정합니다.
// });

// const googleMaps = await loader.importLibrary("maps");
// const { Map } = googleMaps;
// // 맵을 초기화합니다.
console.log(props.data);
onMounted(async () => {
  await until(mapEl).not.toBeNull();
  const mapContainer = document.getElementById("mapEl"), // 지도를 표시할 div
    mapOption = {
      center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
      level: 3, // 지도의 확대 레벨
    };
  // const map = new KakaoMap();
  // const map = new Map(mapEl.value!, {
  //   center: { lat: 37.55467224121094, lng: 126.97088623046875 },
  //   zoom: 8,
  // });
});
console.log(props.data);
</script>

<style>
.result-modal {
  max-width: 768px !important;
}
</style>
