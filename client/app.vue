<template>
  <NuxtPage />
</template>
<script setup lang="ts">
  const runtimeConfig = useRuntimeConfig();
  const appkey = runtimeConfig.public.kakaomapApi;
  useHead({
    script: [
      {
        src: `//dapi.kakao.com/v2/maps/sdk.js?appkey=${appkey}&libraries=services`,
        async: true,
        type: "text/javascript",
      },
    ],
  });
</script>