<script setup>
import { reactive, ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRoute,useRouter } from "vue-router";
import axios from "axios";
import { useMainStore } from '../../store';

const store = useMainStore();
const router = useRouter();
const route = useRoute();

const state = reactive({
  quiz: null,
  questions: [],
  currentQuestionIndex: 0,
  selectedOption: "",
  loading: true,
  error: null,
  optionsSelected: [],
});

const quiz__id = ref(null);

const timer = ref("00:00:00");
let remainingTimeInSeconds = 0;
let timerInterval = null;

const currentQuestion = computed(() => state.questions[state.currentQuestionIndex]);

const totalQuestions = computed(() => state.questions.length);

const selectOption = (option) => {
  state.selectedOption = option;
  state.optionsSelected[state.currentQuestionIndex] = option;
};

const saveAndNext = () => {
  if (!state.selectedOption) {
    alert("Please select an option before proceeding.");
    return;
  }
  if (state.currentQuestionIndex < totalQuestions.value - 1) {
    state.currentQuestionIndex++;
    state.selectedOption = "";
  } else {
    alert("This is the last question!");
  }
};

const submitQuiz = () => {
  clearInterval(timerInterval);
  fetch('http://127.0.0.1:5000/api/submitQuiz',{
    method:'POST',
    body:JSON.stringify({
      quiz_id:quiz__id.value,
      remainingTimeInSeconds:remainingTimeInSeconds,
      selectedOptions:state.optionsSelected,
      userEmail:localStorage.getItem('User_email')
    }),
    headers:{
        'Content-Type':'application/json',
        'Authentication-Token':localStorage.getItem('token')
    }
  })
  .then(response=>response.json())
  .then(data=>{
      if(data.success){
          alert(data.message);
      }
  })
  updateToken()
  router.push("/user/uhome");
  alert('Quiz Submitted Successfully!');
};

  function updateToken() {
    store.setMainToken(0);
  }

const startTimer = (duration) => {
  remainingTimeInSeconds = duration;

  timerInterval = setInterval(() => {
    if (remainingTimeInSeconds > 0) {
      remainingTimeInSeconds--;

      const hours = Math.floor(remainingTimeInSeconds / 3600);
      const minutes = Math.floor((remainingTimeInSeconds % 3600) / 60);
      const seconds = remainingTimeInSeconds % 60;

      timer.value = `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    } else {
      clearInterval(timerInterval);
      alert("Time's up! The quiz will be submitted automatically.");
      submitQuiz();
    }
  }, 1000);
};

const fetchQuizQuestions = async (quizId) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/getQuizQuestions/${quizId}`, {
      headers: {
        "Authentication-Token": localStorage.getItem("token"),
      },
    });
    if (response.data.success) {
      state.quiz = {
        id: response.data.quiz_id,
        name: response.data.quiz_name,
        date: response.data.date_of_quiz,
        duration: response.data.time_duration,
      };
      state.questions = response.data.questions;

      const [hours, minutes, seconds] = state.quiz.duration.split(":").map(Number);
      const totalSeconds = hours * 3600 + minutes * 60 + seconds;
      startTimer(totalSeconds);
    } else {
      state.error = response.data.message;
    }
  } catch (err) {
    state.error = "Failed to fetch quiz questions.";
    console.error(err);
  } finally {
    state.loading = false;
  }
};

onMounted(() => {
  const quizId = route.params.quizId;
  quiz__id.value = quizId;
  if (quizId) {
    fetchQuizQuestions(quizId);
  } else {
    state.error = "No quiz ID provided in the route.";
    state.loading = false;
  }
});

onBeforeUnmount(() => {
  clearInterval(timerInterval); // Cleanup timer when the component is unmounted
});
</script>

<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Quiz in Progress</h1>
      <div class="flex items-center space-x-4">
        <p class="text-lg font-semibold">
          Time Remaining: <span class="text-green-600">{{ timer }}</span>
        </p>
        <p class="text-lg font-semibold">
          Question {{ state.currentQuestionIndex + 1 }} of {{ totalQuestions }}
        </p>
      </div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-md mb-6">
      <div class="flex flex-col items-center">
        <div v-if="currentQuestion?.statement?.includes('.jpg') || currentQuestion?.statement?.includes('.png')">
          <img
            :src="`http://127.0.0.1:5000/uploads/${currentQuestion.statement.slice(currentQuestion.statement.indexOf('/uploads') + 9)}`"
            alt="Question Image"
            class="w-full h-auto rounded-lg mb-4"
          />
        </div>
        <div v-else>
          <p class="text-lg font-medium mb-4">{{ currentQuestion?.statement }}</p>
        </div>

        <div class="grid grid-cols-2 gap-4 w-full">
          <button
            v-for="(option, index) in currentQuestion?.options"
            :key="index"
            :class="[ 
              'p-4 text-center rounded-lg border',
              state.selectedOption === option ? 'bg-blue-100 border-blue-600' : 'bg-gray-100 border-gray-300',
            ]"
            @click="selectOption(option)"
          >
            {{ option }}
          </button>
        </div>
      </div>
    </div>

    <div class="flex justify-between">
      <button
        @click="submitQuiz"
        class="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 transition"
      >
        Submit Quiz
      </button>
      <button
        @click="saveAndNext"
        class="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600 transition"
      >
        Save & Next
      </button>
    </div>
  </div>
</template>

