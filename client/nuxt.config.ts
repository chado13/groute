import { defineNuxtConfig } from "nuxt/config";
export default defineNuxtConfig({
  modules: ['nuxt-primevue'],
  primevue: {
    cssLayerOrder: 'reset,primevue'
  },
  runtimeConfig: {
    public: {
      kakaomapApi: process.env.NUXT_ENV_KAKAO_API_KEY,
      apiUrl: process.env.NUXT_SERVER_URL
    },
  },
  css: ['primevue/resources/themes/aura-light-green/theme.css', '~/assets/css/main.css']
})