
<script setup>
import { ref,onMounted ,reactive,computed} from "vue";
import { useRouter } from "vue-router";
import { useMainStore } from '../../store';

  const store = useMainStore();

  const router = useRouter();

  const quizzes = ref([]);
  const showModal = ref(false);
  const selectedQuiz = reactive({ 
        name: '',
        chapter_id:null,
        date_of_quiz:'',
        time_duration:'',
        quiz_id: null,
        active:false,
        no_of_questions:0,
        remarks:'',
        subject:''
      });
  
  const viewQuiz = (quiz) => {
    selectedQuiz.name = quiz.name;
    selectedQuiz.quiz_id = quiz.quiz_id;
    selectedQuiz.chapter_id = quiz.chapter_id;
    selectedQuiz.date_of_quiz = quiz.date_of_quiz;
    selectedQuiz.time_duration = quiz.time_duration;
    selectedQuiz.active = quiz.active;
    selectedQuiz.no_of_questions = quiz.no_of_questions;
    selectedQuiz.remarks = quiz.remarks;
    selectedQuiz.subject = quiz.subject;
    showModal.value = true;
    console.log(quiz.quiz_id)
  };

  const closeModal = () => {
    showModal.value = false;
  };

  const activeQuizzes = computed(() => quizzes.value.filter((quiz) => quiz.active));

  function updateToken() {
    store.setMainToken(1); // Update the token
  }

  const startQuiz = (quizId) => {
    updateToken();
    router.push("/user/uquizstarted");
    router.push({ 
      name: "uquizstarted", 
      params: { quizId } 
    });
    
    
  };

  onMounted(() => {
          fetch('http://127.0.0.1:5000/api/getQuizzes')
          .then(response=>response.json())
          .then(data=>{
              quizzes.value = data;
          })
      });

      // Function to format the date
  function formatQuizDate(dateString) {
    const options = {
      weekday: "short", // Optional: Remove if you don't want the weekday
      day: "2-digit",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true, // Ensures 12-hour format with AM/PM
    };

    const date = new Date(dateString);
    return date.toLocaleString("en-US", options);
  }
</script>



<template>
    <div class="p-6 bg-gray-100">
      <h2 class="text-2xl font-bold text-center mb-6">Upcoming Quizzes</h2>
      <div class="overflow-x-auto">
        <table class="table-auto w-full border-collapse border border-gray-300 shadow-lg rounded-lg">
          <thead class="bg-gray-700 text-white">
            <tr>
              <th class="px-4 py-2 border border-gray-300">ID</th>
              <th class="px-4 py-2 border border-gray-300">No. of Questions</th>
              <th class="px-4 py-2 border border-gray-300">Date</th>
              <th class="px-4 py-2 border border-gray-300">Duration (hh:mm)</th>
              <th class="px-4 py-2 border border-gray-300">Action</th>
            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="quiz in activeQuizzes" :key="quiz.quiz_id" :value="quiz.quiz_id" class="hover:bg-gray-100">
              <td class="px-4 py-2 border border-gray-300 text-center">{{ quiz.quiz_id }}</td>
              <td class="px-4 py-2 border border-gray-300 text-center">{{ quiz.no_of_questions }}</td>
              <td class="px-4 py-2 border border-gray-300 text-center">{{ formatQuizDate(quiz.date_of_quiz) }}</td>
              <td class="px-4 py-2 border border-gray-300 text-center">{{ quiz.time_duration }}</td>
              <td class="px-4 py-2 border border-gray-300 text-center">
                <button
                  @click="viewQuiz(quiz)"
                  class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition duration-200 mr-2"
                >
                  View
                </button>
                <button
                  @click="startQuiz(quiz.quiz_id)"
                  class="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition duration-200"
                >
                  Start
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <!-- Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center"
    >
      <div class="bg-white rounded-lg p-6 w-96">
        <h2 class="text-xl font-semibold mb-4">Quiz Details</h2>
        <ul class="space-y-2">
          <li><strong>ID:</strong> {{ selectedQuiz.quiz_id }}</li>
          <li><strong>Name:</strong> {{ selectedQuiz.name }}</li>
          <li><strong>Subject:</strong> {{ selectedQuiz.subject }}</li>
          <li><strong>Chapter:</strong> {{ selectedQuiz.chapter_id }}</li>
          <li><strong>Number of Questions:</strong> {{ selectedQuiz.no_of_questions }}</li>
          <li><strong>Scheduled Date:</strong> {{ formatQuizDate(selectedQuiz.date_of_quiz) }}</li>
          <li><strong>Duration:</strong> {{ selectedQuiz.time_duration }} (HH:MM)</li>
        </ul>
        <div class="mt-6 text-right">
          <button
            @click="closeModal"
            class="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600"
          >
            Close
          </button>
        </div>
      </div>
    </div>
      </div>
    </div>
  </template>
  