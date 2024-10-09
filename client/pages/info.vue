<template>
  <div style="margin-top: 30px">
    <!-- 드래그 가능한 영역 -->
    <draggable v-model="positions" @end="updateOrder">
      <template #item="{ element, index, isDragging }">
        <div style="display: flex; flex-direction: column">
          <div v-if="element.type === 'spot'" class="place-item">
            <p>
              {{ element.order }}
            </p>
            <p>
              {{ element.name }}
            </p>
          </div>
          <div v-else>
            {{ element.name }}
          </div>
          <span v-if="element.type === 'spot'" class="drag-handle">≡</span>
        </div>
      </template>
    </draggable>
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from "vue-router";
import { ref, onMounted } from "vue";
import draggable from "vuedraggable";

const positions = ref([]);
positions.value = [
  { id: 0, type: "spliter", order: 0, name: "1" },
  { id: 1, type: "spot", order: 1, name: "안목해변", day: "1" },
  { id: 2, type: "spot", order: 2, name: "중앙시장", day: "1" },
  { id: 3, type: "spliter", order: 0, name: "2" },
  { id: 4, type: "spot", order: 3, name: "동화가든", day: 2 },
];
const groupedPositions = ref({});
// positions.value.forEach(item){
//   if (groupedPositions[item.day])

// }
console.log(groupedPositions);
function updateOrder(event) {
  const places = positions.value.filter((spot) => spot.type === "spot");

  // 필터링된 항목들에 대해 순서 업데이트
  places.forEach((item, index) => {
    item.order = index + 1; // 드래그 후 순서를 업데이트
  });
  console.log(places);
  // 전체 positions 배열에 필터링된 항목들 업데이트
  positions.value.forEach((item) => {
    if (item.type === "spot") {
      const updatedItem = places.find((place) => place.id === item.id);
      if (updatedItem) {
        item.order = updatedItem.order;
      }
    }
  });
  console.log(positions.value);
}
</script>

<style scoped>
.place-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
</style>
