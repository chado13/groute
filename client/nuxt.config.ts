import { defineNuxtConfig } from "nuxt/config";
export default defineNuxtConfig({
  modules: ['nuxt-primevue'],
  primevue: {
    cssLayerOrder: 'reset,primevue'
  },
  runtimeConfig: {
    public: {
      kakaomapApi: process.env.NUXT_ENV_KAKAO_API_KEY,
    },
  },
  css: ['primevue/resources/themes/aura-light-green/theme.css', '~/assets/css/main.css']
})