<template>
  <Dialog v-model:visible="visible" modal header="여행결과" class="result-modal">
    <div v-html="marked(text)"></div>
    <div ref="mapEl" :style="{
      width: '100%',
      height: '400px'
    }"></div>
  </Dialog>
</template>

<script setup lang="ts">
import { marked } from 'marked';
import { Loader } from '@googlemaps/js-api-loader';
import { until } from '@vueuse/core'

const runtimeConfig = useRuntimeConfig();
const mapApi = runtimeConfig.public.mapApi;
const props = defineProps<{
  text: string;
}>()

const visible = defineModel<boolean>("visible", { required: true })

const mapEl = ref<HTMLElement | null>(null);

const loader = new Loader({
  apiKey: mapApi, // 환경 변수에서 API 키를 가져옵니다.
  version: 'weekly',
  libraries: ['maps'] // 필요한 라이브러리 옵션을 설정합니다.
});

const googleMaps = await loader.importLibrary("maps");
const { Map } = googleMaps;
// 맵을 초기화합니다.

onMounted(async () => {
  await until(mapEl).not.toBeNull();

  const map = new Map(mapEl.value!, {
    center: { lat: 37.55467224121094, lng: 126.97088623046875 },
    zoom: 8,
  });


})
</script>

<style>
.result-modal {
  max-width: 768px !important;
}
</style>