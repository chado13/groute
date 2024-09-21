
<template>
    <div class="header-container">
      <svg width="114" height="24" viewBox="0 0 114 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_23_91)">
        <path d="M40.4377 6.5549C40.4228 2.90798 37.3474 0.381348 32.8636 0.381348H23.688V20.5408H27.7202V13.1396H31.7196L36.459 20.5408H41.0349L35.9152 12.7016C38.6786 11.8286 40.4228 9.32883 40.4377 6.5549ZM33.0835 9.75192H27.7231V4.06999H33.0835C35.1397 4.06999 36.3669 5.06813 36.3788 6.71878C36.3639 8.37241 35.1397 9.76384 33.0835 9.75192Z" fill="white"/>
        <path d="M75.3485 11.9628C75.3336 15.1717 73.7677 17.0995 71.1796 17.0995C68.5916 17.0995 67.0257 15.1747 67.0405 11.9628V0.765747H63.0084V11.9657C62.9935 17.3468 66.265 20.9252 71.1796 20.9252C76.0943 20.9252 79.3658 17.3468 79.3777 11.9657V0.765747H75.3455V11.9657L75.3485 11.9628Z" fill="white"/>
        <path d="M82.2656 4.56165H88.1757V20.5408H92.2079V4.56165H98.0645V0.765747H82.2656V4.56165Z" fill="white"/>
        <path d="M105.092 16.7449V12.1296H113.019V8.65848H105.092V4.56165H113.78V0.765747H101.06V20.5408H114V16.7449H105.092Z" fill="white"/>
        <path d="M10.3256 4.39778C10.4652 4.39778 10.599 4.40076 10.7356 4.4097H19.7805V0.584001H10.7356C10.599 0.578042 10.4652 0.572083 10.3256 0.572083C4.42739 0.575062 -0.0148197 4.99964 3.71562e-05 10.8455C-0.0148197 16.6913 4.43928 21.1158 10.3523 21.1158C15.3324 21.1158 19.0793 17.9993 19.6884 13.3036C19.7449 12.8626 19.7775 12.4067 19.7775 11.9389V9.94564H10.7327V13.3065H15.6622C15.1303 15.7527 13.1692 17.2931 10.3494 17.2931C6.64405 17.2931 4.04409 14.6294 4.05597 10.8455C4.04112 7.06147 6.62919 4.39778 10.3196 4.39778H10.3256Z" fill="white"/>
        <path d="M51.3189 0C47.26 0 43.2041 3.47412 43.2041 9.2365C43.2041 14.9989 51.3189 24.003 51.3189 24.003C51.3189 24.003 59.4338 14.9989 59.4338 9.2365C59.4338 3.47412 55.3779 0 51.3189 0ZM51.3189 13.2708C48.7962 13.2708 46.7519 11.2209 46.7519 8.69125C46.7519 6.16164 48.7962 4.11173 51.3189 4.11173C53.8416 4.11173 55.886 6.16164 55.886 8.69125C55.886 11.2209 53.8416 13.2708 51.3189 13.2708Z" fill="white"/>
        </g>
        <defs>
        <clipPath id="clip0_23_91">
        <rect width="114" height="24" fill="white"/>
        </clipPath>
        </defs>
        </svg>
    </div>
    <div class="p-fluid p-formgrid p-grid">
      <!-- <div id="map" style="width: 100%; height: 350px"></div> -->
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
          @keyup.enter="searchSpot"
          placeholder="장소를 입력후 엔터를 해주세요. 지점이 여러개일 경우 정확히 입력해주세요."
        />
        <Chip
          v-for="spot in formData.spots"
          :key="spot.name"
          :label="spot.name"
          removable
          @remove="removeSpot(spot)"
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
        <InputText
          v-model="arrival"
          id="arrival"
          @keyup.enter="searchArrival"
          rows="1"
          placeholder="여행을 어디에서부터 계획할지 정해주세요. ex) 서울역, 인청공항 등"
        />
      </div>

      <!-- 여행 끝점 입력 -->
      <div class="p-field p-col-12">
        <label for="depart">여행 끝</label>
        <InputText
          v-model="depart"
          id="depart"
          @keyup.enter="searchDepart"
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
        <InputText
          id="hotel"
          v-model="hotel"
          @keyup.enter="searchHotel"
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
  <ProgressSpinner class="progress-spinner" v-if="isLoading" />
  <!-- <ClientOnly>
    <TravelResult v-model:visible="visible" :data="resultData" v-if="visible" />
  </ClientOnly> -->
</template>
<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useDebounceFn } from "@vueuse/core";
import axios from "axios";

const router = useRouter();

const placeholderText = "콤마(,)로 구분하여 방문하고 싶은 여행지 내 장소를 작성해 주세요.\n예제: 경복궁, 명동, 롯데타워";

const formData = ref<{
  destination: string;
  spots: placeItem[];
  schedule: string[];
  transport: string;
  arrival: placeItem | null;
  depart: placeItem | null;
  hotel: placeItem | null;
}>({
  destination: "",
  spots: [],
  schedule: [],
  transport: "",
  arrival: null,
  depart: null,
  hotel: null,
});
const spot = ref("");
const depart = ref("");
const arrival = ref("");
const hotel = ref("");

const resultData = ref({});
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
    console.log("get result")
    console.log(resultData.value);
    return (
      Array.isArray(resultData.value.spots) && resultData.value.spots.length > 0
    );
  },
  set: () => {
    resultData.value = [];
  },
});
watch (visible, (newVal) => {
  if (newVal) {
    // Navigate to result.vue when visible is true
    router.push({
      name: 'result',
      query: {
        result_data: resultData.value,
        visible: true
      }
    });
  }
});
type placeItem = {
  name: "";
  address: "";
  lat: 0;
  lng: 0;
  category: "";
};

const submitForm = async () => {
  try {
    isLoading.value = true;
    const response = await axios.post(
      "http://localhost:8000/groute/route",
      formData.value
    );
    console.log("폼 데이터가 성공적으로 전송되었습니다:", response.data);
    resultData.value = response.data;
  } catch (error) {
    window.alert("폼 데이터 전송 중 오류 발생");
    throw error;
  } finally {
    isLoading.value = false;
  }
};

const searchPlaceAndAssign = useDebounceFn(async (keywordSource, field) => {
  const keyword = keywordSource.value;
  if (!keyword) return;

  const placeItem = await searchPlace(formData.value.destination + keyword);
  if (placeItem) {
    if (field == "spots") {
      formData.value.spots.push(placeItem);
      spot.value = "";
    } else {
      formData.value[field] = placeItem;
    }
  }
}, 100);

const searchSpot = () => searchPlaceAndAssign(spot, "spots");
const searchArrival = () => searchPlaceAndAssign(arrival, "arrival");
const searchDepart = () => searchPlaceAndAssign(depart, "depart");
const searchHotel = () => searchPlaceAndAssign(hotel, "hotel");

const searchPlace = (keyword) => {
  return new Promise((resolve, reject) => {
    const ps = new kakao.maps.services.Places();
    ps.keywordSearch(keyword, (data, status) => {
      if (status === kakao.maps.services.Status.OK) {
        const placeItem = {
          name: data[0].place_name,
          address: data[0].address_name,
          lat: data[0].y,
          lng: data[0].x,
          category: data[0].category_name,
        };
        resolve(placeItem);
      } else {
        reject("Search failed");
      }
    });
  });
};

function removeSpot(spot: string) {
  const index = formData.value.spots.findIndex(
    (item) => item.name == spot.name
  );
  console.log(index);
  if (index !== -1) {
    formData.value.spots.splice(index, 1);
  }
}
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
.header-container {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  background-color: #3DAC68;
  height: 100px;
  padding: 20px;
  width: 100vw;
  box-sizing: border-box; /* 패딩과 테두리를 포함한 전체 너비 및 높이 계산 */
}


</style>
