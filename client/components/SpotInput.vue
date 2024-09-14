<template>
  <div class="flex">
    <InputText v-model="value" />
    <Button label="입력" @click="onClick" id="a" />
  </div>
  <div>
    <Chip
      v-for="spot in props.spots"
      :key="spot"
      :label="spot"
      removable
      @remove="onChipRemove(spot)"
    />
  </div>
</template>
<script setup lang="ts">
const emit = defineEmits<{
  "spot-added": [string];
  "spot-removed": [string];
}>();

const props = defineProps<{
  spots: string[];
}>();

const value = ref("");

function onClick() {
  if (!value.value) return;
  emit("spot-added", value.value);
  value.value = "";
}

function onChipRemove(spot: string) {
  console.log("a");
  emit("spot-removed", spot);
}
</script>
