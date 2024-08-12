<template>
  <div class="flex">
    <InputText v-model="value" />
    <Button label="입력" @click="onClick" />
  </div>
  <div>
    <Chip v-for="spot in props.spots" :key="spot" :label="spot" />
  </div>
</template>
<script setup lang="ts">
const emit = defineEmits<{
  "spot-added": [string];
}>();

const props = defineProps<{
  spots: string[];
}>();

const value = ref("");

function onClick() {
  console.log(value.value);
  emit("spot-added", value.value);
  value.value = "";
}
</script>
