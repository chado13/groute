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
        <Textarea id="spots" v-model="formData.spots" rows="4" :placeholder="placeholderText" />
      </div>

      <!-- 일정 입력 -->
      <div class="p-field p-col-12">
        <label for="schedule">일정</label>
        <Calendar id="schedule" v-model="formData.schedule" selectionMode="range" :manualInput="false"
          dateFormat="yy/mm/dd" type="date" />
      </div>

      <!-- 여행 시작점 입력 -->
      <div class="p-field p-col-12">
        <label for="arrival">여행 시작점</label>
        <Textarea id="arrival" v-model="formData.arrival" rows="1" placeholder="여행지 도착 역 ex) 서울역, 인청공항 등" />
      </div>

      <!-- 여행 끝점 입력 -->
      <div class="p-field p-col-12">
        <label for="depart">여행 끝</label>
        <Textarea id="depart" v-model="formData.depart" rows="1" placeholder="여행지 끝" />
      </div>

      <!-- 여행 중 식사 장소 입력 -->
      <div class="p-field p-col-12">
        <label for="restorants">식사</label>
        <Textarea id="restorants" v-model="formData.restorants" rows="4" placeholder="여행 중 식사 장소들" />
      </div>

      <!-- 여행 중 숙박 장소 입력 -->
      <div class="p-field p-col-12">
        <label for="hotel">숙박</label>
        <Textarea id="hotel" v-model="formData.hotel" rows="1" placeholder="여행 중 숙박장소" />
      </div>

      <!-- 이용 교통 입력 -->
      <div class="p-field p-col-12">
        <label for="transport">이용 교통</label>
        <Dropdown id="transport" :options="transportOptions" v-model="formData.transport" optionLabel="label"
          optionValue="value" placeholder="여행지 내 이용수단" />
      </div>

      <!-- 폼 제출 버튼 -->
      <div class="p-field p-col-12">
        <p></p>
        <Button label="제출" @click="submitForm" />
      </div>
    </div>

  </div>
  <ProgressSpinner class="progress-spinner" v-if="isLoading" />
  <ClientOnly>
    <TravelResult v-model:visible="visible" :text="resultText" v-if="visible"/>
    </ClientOnly>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

const router = useRouter();
const placeholderText = '콤마(,)로 구분하여 방문하고 싶은 여행지 내 장소를 작성해 주세요.\n예제: 경복궁, 명동, 롯데타워'
const formData = ref({
  destination: '',
  spots: '',
  schedule: '',
  transport: '',
  arrival: '',
  depart: '',
  hotel: '',
  restorants:''
})
const resultText = ref('');
const isLoading = ref(false);
const transportOptions = [
  { label: '자동차', value: '자동차' },
  { label: '지하철', value: '지하철' },
  { label: '버스', value: '버스' }
]
const visible = computed({
  get: () => {
    return !!resultText.value
  }, set: () => {
    resultText.value = ''
  }
})


const submitForm = async () => {
  try {
    isLoading.value = true;
    const response = await axios.post('http://localhost:8000/groute', formData.value);
    console.log('폼 데이터가 성공적으로 전송되었습니다:', response.data);
    resultText.value = response.data;
  } catch (error) {
    window.alert('폼 데이터 전송 중 오류 발생');
    throw error
  } finally {
    isLoading.value = false;
  }
};

</script>

<style scoped>
.progress-spinner {
  width: 50px;
  height: 50px;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>