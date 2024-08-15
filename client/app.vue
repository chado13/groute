<template>
  <NuxtPage />
</template>

<script setup lang="ts">
import { useKakao } from "vue3-kakao-maps/@utils";
const runtimeConfig = useRuntimeConfig();
const appkey = runtimeConfig.public.kakaomapApi;

onMounted(() => {
  useKakao(appkey, ["clusterer", "services", "drawing"]);
});
</script>
