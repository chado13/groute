<template>
  <div class="container">
    <h1>Draggable Example with Two Columns</h1>
    <div class="draggable-container">
      <!-- 왼쪽 리스트 -->
      <draggable
        v-model="leftItems"
        group="shared"
        item-key="name"
        @end="onEnd"
        @change="onChange"
      >
        <template #item="{ element }">
          <div class="list-item">
            {{ element.name }}
          </div>
        </template>
      </draggable>

      <!-- 구분선 (divider) -->
      <div class="divider"></div>

      <!-- 오른쪽 리스트 -->
      <draggable
        v-model="rightItems"
        group="shared"
        item-key="name"
        @end="onEnd"
      >
        <template #item="{ element }">
          <div class="list-item">
            {{ element.name }}
          </div>
        </template>
      </draggable>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import draggable from "vuedraggable";

// 왼쪽과 오른쪽 리스트에 들어갈 데이터
const leftItems = ref([
  { name: "Item 1" },
  { name: "Item 2" },
  { name: "Item 3" },
]);

const rightItems = ref([
  { name: "Item 4" },
  { name: "Item 5" },
  { name: "Item 6" },
]);

const onEnd = (event) => {
  console.log("Drag ended: ", event);
};

const onChange = (event) => {
  console.log("Drag changed: ", event);
};
</script>

<style>
.container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.draggable-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border: 1px solid #ccc;
  padding: 10px;
}

.draggable-container > * {
  flex: 1;
}

.divider {
  width: 5px;
  background-color: #999;
  margin: 0 10px;
}

.list-item {
  padding: 10px;
  margin: 5px 0;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  cursor: move;
}
</style>
