<template>
  <div>
    <h2>여행 정보 입력</h2>
    <div class="p-fluid p-formgrid p-grid">
      <!-- 여행 예정지 입력 -->
      <div class="p-field p-col-12">
        <label for="destination">여행 예정지</label>
        <InputText id="destination" v-model="formData.destination" />
      </div>

      <!-- 관광 스팟 입력 -->
      <div class="p-field p-col-12">
        <label for="spots">관광 스팟</label>
        <Textarea id="spots" v-model="formData.spots" rows="4" :placeholder="placeholderText"/>
      </div>

      <!-- 일정 입력 -->
      <div class="p-field p-col-12">
        <label for="schedule">일정</label>
        <Calendar id="schedule" v-model="formData.schedule" selectionMode="range" :manualInput="false"/>
      </div>

      <!-- 이용 교통 입력 -->
      <div class="p-field p-col-12">
        <label for="transport">이용 교통</label>
        <Dropdown id="transport" :options="transportOptions" v-model="formData.transport" optionLabel="label" optionValue="value" placeholder="여행지 내 이용수단"/>
      </div>

      <!-- 폼 제출 버튼 -->
      <div class="p-field p-col-12">
        <p></p>
        <Button label="제출" @click="submitForm" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
const placeholderText = '콤마(,)로 구분하여 방문하고 싶은 여행지 내 장소를 작성해 주세요.\n예제: 경복궁, 명동, 롯데타워'
const formData = ref({
  label: '',
  value: '',
})
const transportOptions= [
        { label: '자동차', value: 'Car' },
        { label: '지하철', value: 'Subway' },
        { label: '버스', value: 'Bus' }
      ]

function submitForm() {
  console.log('폼 데이터:', this.formData);
}
</script>
