
<template>
  <template>
    <div class="hore__secton">
      <Button label="Click To Get Started" icon="pi pi-check" iconPos="right" />
      <i class="pi pi-check"></i>
      <i class="pi pi-times"></i>
      <span class="pi pi-search"></span>
      <span class="pi pi-user"></span>
    </div>
  </template>
</template>


<script setup>
import { ref } from "vue";
import draggable from "vuedraggable";
import "primeicons/primeicons.css";




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
