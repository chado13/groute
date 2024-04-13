export default defineNuxtConfig({
  modules: [
      'nuxt-primevue'
  ],
  primevue: {
    cssLayerOrder: 'reset,primevue'
},
  css: ['primevue/resources/themes/aura-light-green/theme.css']
})