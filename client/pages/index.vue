<template>
  <div>
    <h2>여행 정보 입력</h2>
    <div class="p-fluid p-formgrid p-grid">
      <div id="map" style="width: 100%; height: 350px"></div>
      <!-- 여행 예정지 입력 -->
      <div class="p-field p-col-12">
        <label for="destination">여행 예정 도시</label>
        <InputText id="destination" v-model="formData.destination" />
      </div>

      <!-- 관광 스팟 입력 -->
      <div class="p-field p-col-12">
        <label for="spots">여행 예정 장소</label>
        <InputText
          v-model="spot"
          id="spot"
          @keyup.enter="searchMap"
          placeholder="장소를 입력후 엔터를 해주세요. 지점이 여러개일 경우 정확히 입력해주세요."
        />
        <Chip
          v-for="spot in formData.spots"
          :key="spot.name"
          :label="spot.name"
        />
      </div>

      <!-- 일정 입력 -->
      <div class="p-field p-col-12">
        <label for="schedule">일정</label>
        <Calendar
          id="schedule"
          v-model="formData.schedule"
          selectionMode="range"
          :manualInput="false"
          dateFormat="yy/mm/dd"
          type="date"
        />
      </div>

      <!-- 여행 시작점 입력 -->
      <div class="p-field p-col-12">
        <label for="arrival">여행 시작점</label>
        <Textarea
          id="arrival"
          v-model="formData.arrival"
          rows="1"
          placeholder="여행을 어디에서부터 계획할지 정해주세요. ex) 서울역, 인청공항 등"
        />
      </div>

      <!-- 여행 끝점 입력 -->
      <div class="p-field p-col-12">
        <label for="depart">여행 끝</label>
        <Textarea
          id="depart"
          v-model="formData.depart"
          rows="1"
          placeholder="여행의 마지막을 어디에서 끝낼지 정해주세요. 예) 서울역, 인천공항 등"
        />
      </div>

      <!-- 여행 중 식사 장소 입력 -->
      <!-- <div class="p-field p-col-12">
        <label for="restorants">식사</label>
        <Textarea
          id="restorants"
          v-model="formData.restorants"
          rows="4"
          placeholder="여행 중 식사 장소들"
        />
      </div> -->

      <!-- 여행 중 숙박 장소 입력 -->
      <div class="p-field p-col-12">
        <label for="hotel">숙박</label>
        <Textarea
          id="hotel"
          v-model="formData.hotel"
          rows="1"
          placeholder="여행 중 정해진 숙박장소가 있다면 입력해주세요. 지점이 여러개일 경우 정확히 입력해주세요."
        />
      </div>

      <!-- 이용 교통 입력 -->
      <div class="p-field p-col-12">
        <label for="transport">이용 교통</label>
        <Dropdown
          id="transport"
          :options="transportOptions"
          v-model="formData.transport"
          optionLabel="label"
          optionValue="value"
          placeholder="여행지 내 주요 이용수단"
        />
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
    <TravelResult v-model:visible="visible" :text="resultText" v-if="visible" />
  </ClientOnly>
</template>
<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

const router = useRouter();
type placeItem = {
  name: "";
  address: "";
  lat: 0;
  lng: 0;
  category: "";
};
const placeholderText =
  "콤마(,)로 구분하여 방문하고 싶은 여행지 내 장소를 작성해 주세요.\n예제: 경복궁, 명동, 롯데타워";
const formData = ref<{
  destination: string;
  spots: placeItem[];
  schedule: string;
  transport: string;
  arrival: string;
  depart: string;
  hotel: string;
  restorants: string;
}>({
  destination: "",
  spots: [],
  schedule: "",
  transport: "",
  arrival: "",
  depart: "",
  hotel: "",
  restorants: "",
});
const spot = ref("");

const resultText = ref("");
const isLoading = ref(false);
const transportOptions = [
  { label: "자동차", value: "자동차" },
  { label: "지하철", value: "지하철" },
  { label: "버스", value: "버스" },
  { label: "도보", value: "도보" },
  { label: "자전거", value: "자전거" },
];
const visible = computed({
  get: () => {
    return !!resultText.value;
  },
  set: () => {
    resultText.value = "";
  },
});

const submitForm = async () => {
  try {
    isLoading.value = true;
    const response = await axios.post(
      "http://localhost:8000/groute",
      formData.value
    );
    console.log("폼 데이터가 성공적으로 전송되었습니다:", response.data);
    resultText.value = response.data;
  } catch (error) {
    window.alert("폼 데이터 전송 중 오류 발생");
    throw error;
  } finally {
    isLoading.value = false;
  }
};

function searchMap() {
  console.log(spot.value);
  const keyword = spot.value;
  if (!keyword) return;
  const ps = new kakao.maps.services.Places();
  ps.keywordSearch(formData.value.destination + keyword, placesSearchCB);
}
const placesSearchCB = (
  data: kakao.maps.services.PlacesSearchResult,
  status: kakao.maps.services.Status
): void => {
  if (status === kakao.maps.services.Status.OK) {
    console.log(data);
    const placeItem: placeItem = {
      name: data[0].place_name,
      address: data[0].address_name,
      lat: data[0].y,
      lng: data[0].x,
      category: data[0].category_name,
    };
    console.log(placeItem);
    formData.value.spots.push(placeItem);
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
