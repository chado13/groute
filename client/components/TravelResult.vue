<template>
  <Dialog v-model:visible="visible" modal header="여행결과" class="result-modal">
    <div v-html="marked(text)"></div>
  </Dialog>
</template>

<script setup lang="ts">
import { marked } from 'marked';

const props = defineProps<{
  text: string;
}>()

const visible = defineModel<boolean>("visible", {required: true})
</script>

<style>
.result-modal {
  max-width: 768px !important;
}
</style>