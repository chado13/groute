<template>
  <div>
    <!-- Step 1 -->
    <div v-if="step === 1">
      <div class="header-container">
        <svg
          width="114"
          height="24"
          viewBox="0 0 114 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g clip-path="url(#clip0_23_91)">
            <path
              d="M40.4377 6.5549C40.4228 2.90798 37.3474 0.381348 32.8636 0.381348H23.688V20.5408H27.7202V13.1396H31.7196L36.459 20.5408H41.0349L35.9152 12.7016C38.6786 11.8286 40.4228 9.32883 40.4377 6.5549ZM33.0835 9.75192H27.7231V4.06999H33.0835C35.1397 4.06999 36.3669 5.06813 36.3788 6.71878C36.3639 8.37241 35.1397 9.76384 33.0835 9.75192Z"
              fill="white"
            />
            <path
              d="M75.3485 11.9628C75.3336 15.1717 73.7677 17.0995 71.1796 17.0995C68.5916 17.0995 67.0257 15.1747 67.0405 11.9628V0.765747H63.0084V11.9657C62.9935 17.3468 66.265 20.9252 71.1796 20.9252C76.0943 20.9252 79.3658 17.3468 79.3777 11.9657V0.765747H75.3455V11.9657L75.3485 11.9628Z"
              fill="white"
            />
            <path
              d="M82.2656 4.56165H88.1757V20.5408H92.2079V4.56165H98.0645V0.765747H82.2656V4.56165Z"
              fill="white"
            />
            <path
              d="M105.092 16.7449V12.1296H113.019V8.65848H105.092V4.56165H113.78V0.765747H101.06V20.5408H114V16.7449H105.092Z"
              fill="white"
            />
            <path
              d="M10.3256 4.39778C10.4652 4.39778 10.599 4.40076 10.7356 4.4097H19.7805V0.584001H10.7356C10.599 0.578042 10.4652 0.572083 10.3256 0.572083C4.42739 0.575062 -0.0148197 4.99964 3.71562e-05 10.8455C-0.0148197 16.6913 4.43928 21.1158 10.3523 21.1158C15.3324 21.1158 19.0793 17.9993 19.6884 13.3036C19.7449 12.8626 19.7775 12.4067 19.7775 11.9389V9.94564H10.7327V13.3065H15.6622C15.1303 15.7527 13.1692 17.2931 10.3494 17.2931C6.64405 17.2931 4.04409 14.6294 4.05597 10.8455C4.04112 7.06147 6.62919 4.39778 10.3196 4.39778H10.3256Z"
              fill="white"
            />
            <path
              d="M51.3189 0C47.26 0 43.2041 3.47412 43.2041 9.2365C43.2041 14.9989 51.3189 24.003 51.3189 24.003C51.3189 24.003 59.4338 14.9989 59.4338 9.2365C59.4338 3.47412 55.3779 0 51.3189 0ZM51.3189 13.2708C48.7962 13.2708 46.7519 11.2209 46.7519 8.69125C46.7519 6.16164 48.7962 4.11173 51.3189 4.11173C53.8416 4.11173 55.886 6.16164 55.886 8.69125C55.886 11.2209 53.8416 13.2708 51.3189 13.2708Z"
              fill="white"
            />
          </g>
          <defs>
            <clipPath id="clip0_23_91">
              <rect width="114" height="24" fill="white" />
            </clipPath>
          </defs>
        </svg>
      </div>
      <h2 class="step-title">어떤 도시로 떠나볼까요?</h2>
      <div class="custom-input-container">
        <InputText
          class="custom-input"
          v-model="formData.destination"
          placeholder="도시 이름을 입력해 주세요."
          @keyup.enter="nextStep"
        />
        <Button
          class="custom-button"
          :disabled="!formData.destination"
          @click="nextStep"
          >다음</Button
        >
      </div>
    </div>

    <!-- Step 2 -->
    <div v-if="step === 2">
      <div class="header-area">
        <i
          class="pi pi-angle-left"
          style="font-size: 1.8rem; line-height: 4"
          @click="prevStep"
        ></i>
      </div>
      <h2 class="step-title">여행 일정을 알려주세요.</h2>
      <div class="custom-input-container">
        <Calendar
          class="calendar-input"
          v-model="formData.start"
          showButtonBar
          dateFormat="yy-mm-dd"
          placeholder="출발일"
        />
        <p style="text-align: center; line-height: 3">-</p>
        <Calendar
          class="calendar-input"
          v-model="formData.end"
          showButtonBar
          dateFormat="yy-mm-dd"
          placeholder="도착일"
        />
        <Button
          class="custom-button"
          :disabled="!formData.start || !formData.end"
          @click="nextStep"
          >다음</Button
        >
      </div>
    </div>

    <!-- Step 3 -->
    <div v-if="step === 3">
      <div class="header-area">
        <i
          class="pi pi-angle-left"
          style="font-size: 1.8rem; line-height: 4"
          @click="prevStep"
        ></i>
      </div>
      <h2 class="step-title">꼭 방문하고 싶은 장소를 추가해 주세요.</h2>
      <div class="custom-input-container">
        <div class="input-wrapper">
          <InputText
            v-model="spot"
            class="custom-input"
            @keyup.enter="searchSpot"
            placeholder="장소명을 입력해 주세요."
            @focus="isFocused = true"
            @blur="isFocused = false"
          />
          <i
            class="pi pi-arrow-right search-icon"
            :class="{ 'icon-activate': isFocused }"
            @click="searchSpot"
          ></i>
        </div>
        <div class="input-wrapper">
          <Chip
            v-for="spot in formData.spots"
            :key="spot.name"
            :label="spot.name"
            removable
            @remove="removeSpot(spot)"
            class="chip-item"
          />
        </div>
      </div>
      <Button
        class="custom-button"
        :disabled="formData.spots.length === 0"
        @click="nextStep"
        >다음</Button
      >
    </div>
  </div>
  <!-- Step 4 -->
  <div v-if="step === 4">
    <div class="header-area">
      <i
        class="pi pi-angle-left"
        style="font-size: 1.8rem; line-height: 4"
        @click="prevStep"
      ></i>
    </div>
    <h2 class="step-title">여행 시작 장소를 알려주세요.</h2>
    <InputText
      v-model="arrival"
      class="custom-input"
      :class="{ 'input-activate': arrival || isArrivalFocused }"
      @focus="isArrivalFocused = true"
      @blur="isArrivalFocused = false"
      @keyup.enter="searchArrival"
      placeholder="EX: 강릉역"
    />
    <h2 class="step-title">여행 종료 장소를 알려주세요.</h2>
    <InputText
      v-model="depart"
      class="custom-input"
      :class="{ 'input-activate': depart || isDepartFocused }"
      @focus="isDepartFocused = true"
      @blur="isDepartFocused = false"
      @keyup.enter="searchDepart"
      placeholder="EX: 강릉역"
    />
    <Button
      class="custom-button"
      :disabled="!formData.depart || !formData.arrival"
      @click="submitForm"
      >제출</Button
    >
  </div>
  <ProgressSpinner class="progress-spinner" v-if="isLoading" />
  <ClientOnly>
    <TravelResult v-model:visible="visible" :data="resultData" v-if="visible" />
  </ClientOnly>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import "primeicons/primeicons.css";
import { useDebounceFn } from "@vueuse/core";
import axios from "axios";
// 반응형 상태 변수 정의
const step = ref(1); // 현재 단계 추적
const spot = ref("");
const depart = ref("");
const arrival = ref("");
const isFocused = ref(false); // 포커스 상태 관리
const isArrivalFocused = ref(false); // 첫 번째 InputText 포커스 상태
const isDepartFocused = ref(false); // 두 번째 InputText 포커스 상태
console.log(isFocused);
type placeItem = {
  name: "";
  address: "";
  lat: 0;
  lng: 0;
  category: "";
};

const resultData = ref({});
const isLoading = ref(false);
const formData = ref<{
  destination: string;
  spots: placeItem[];
  start: string;
  end: string;
  transport: string;
  arrival: placeItem | null;
  depart: placeItem | null;
  hotel: placeItem | null;
}>({
  destination: "",
  spots: [],
  start: "",
  end: "",
  transport: "",
  arrival: null,
  depart: null,
  hotel: null,
});

// 다음 단계로 이동하는 함수
const nextStep = () => {
  if (step.value < 4) {
    step.value++;
  }
};

// 이전 단계로 이동하는 함수
const prevStep = () => {
  if (step.value > 1) {
    step.value--;
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
// const searchHotel = () => searchPlaceAndAssign(hotel, "hotel");

const searchPlace = (keyword) => {
  console.log(keyword);
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

const visible = computed({
  get: () => {
    console.log(resultData.value);
    return (
      Array.isArray(resultData.value.spots) && resultData.value.spots.length > 0
    );
  },
  set: () => {
    resultData.value = [];
  },
});
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
  background-color: #3dac68;
  height: 100px;
  padding: 20px;
  width: 100vw;
  box-sizing: border-box; /* 패딩과 테두리를 포함한 전체 너비 및 높이 계산 */
}
.step-title {
  font-size: 20px;
  line-height: 32px;
  font-weight: 500;
  columns: #121212;
  padding-left: 10px;
  margin-top: 10px;
}

/* 2. 커스텀 스타일 추가 */
.custom-input {
  border: none; /* 기본 보더 제거 */
  border-bottom: 2px solid #ccc; /* 아래쪽에만 직선 표시 */
  outline: none; /* 포커스 시 외곽선 제거 */
  transition: border-color 0.3s ease; /* 포커스 시 색상 변화 애니메이션 */
  width: 90%;
  padding: 10px;
  border-radius: 0;
  margin-left: 10px;
}

.custom-input:focus {
  border-bottom: 2px solid #42b883; /* 포커스 시 색상 */
}

.custom-input-container {
  width: 100%;
  display: flex;
  gap: 1px;
  justify-content: space-between; /* 요소들 간의 공간을 균등하게 분배 */
  flex-wrap: wrap; /* 화면이 좁을 때 컴포넌트들이 자동으로 다음 줄로 내려가도록 */
}

.calendar-input {
  flex-grow: 1; /* 각 Calendar가 동일한 비율로 크기를 차지 */
  max-width: 48%; /* Calendar의 최대 너비 설정 */
  height: 44px;
  box-sizing: border-box; /* 요소가 부모 요소의 크기를 초과하지 않도록 */
  padding-inline: 20px;
  text-align: center;
}
/* 버튼 스타일 */
.custom-button {
  position: absolute; /* 버튼을 부모 컨테이너의 맨 아래에 위치 */
  bottom: 20px; /* 창의 아래쪽에서 20px 위에 고정 */
  left: 50%;
  transform: translateX(-50%); /* 중앙 정렬 */
  padding: 12px, 10px, 12px, 10px;
  background-color: #a8a8a880;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 90%;
  gap: 10px;
  height: 40px;
  transform: translateX(-50%); /* 중앙 정렬 */

  /* 글자 및 내용 중앙 정렬 */
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.custom-button:disabled {
  background-color: #ccc; /* 비활성화 상태일 때 버튼 색상 */
  cursor: not-allowed; /* 비활성화 시 커서 변경 */
}

.custom-button:not(:disabled) {
  background-color: #369c6b; /* 버튼 활성화 상태일 때 호버 색상 */
}

.chip-item {
  background: #2f834f;
  margin-top: 10px;
  margin-left: 10px;
  color: white;
  padding: 6px, 10px, 6px, 10px;
}

.input-activate {
  border-bottom: 2px solid #42b883; /* 포커스 시 색상 */
}

.header-area {
  width: 100%;
  height: 78px;
  top: 20px;
}
.search-icon {
  position: absolute;
  right: 1.8rem; /* 입력 필드의 오른쪽에 배치 */
  top: 50%;
  transform: translateY(-50%); /* 수직 중앙 정렬 */
  font-size: 1.2rem;
  color: #888;
  cursor: pointer;
  transition: color 0.3s;
}
/* 부모 컨테이너에 relative 위치 설정 */
.input-wrapper {
  position: relative;
  width: 100%;
}

/* 포커스된 상태에서 아이콘 색상 활성화 */
.icon-activate {
  color: #4caf50; /* 활성화된 상태에서의 색상 */
}
</style>
