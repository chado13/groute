import { defineNuxtConfig } from "nuxt/config";
export default defineNuxtConfig({
  modules: ['nuxt-primevue'],
  primevue: {
    cssLayerOrder: 'reset,primevue'
  },
  runtimeConfig: {
    public: {
      mapApi: process.env.MAP_API,
      kakaomapApi: process.env.KAKAO_API_KEY,
    },
  },
  css: ['primevue/resources/themes/aura-light-green/theme.css']
})