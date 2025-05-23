<template>
  <!------------------------------------- Id Details Modal ----------------------------------------->
  <div v-if="showIdModal" 
      class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50"
      >
      <div 
          class="bg-gray-800 p-6 rounded-lg shadow-2xl w-full max-w-md text-gray-300"
      >
          <!-- Header -->
          <div class="text-center mb-6">
          <h2 class="text-2xl font-bold text-white">Question Id:{{ viewQuestionDetail.question_id }}</h2>
          <p class="text-gray-400">Detailed information about the question of the quiz with id :{{ viewQuestionDetail.quiz_id }}</p>
          </div>

          <!-- Question Info -->
          <div class="space-y-4">
          <div class="flex items-center">
              <span class="text-pink-500 font-bold w-32">Option 1:</span>
              <span>{{ viewQuestionDetail.option1 }}</span>
          </div>
          <div class="flex items-center">
              <span class="text-pink-500 font-bold w-32">Option 2:</span>
              <span>{{ viewQuestionDetail.option2 }}</span>
          </div>
          <div class="flex items-center">
              <span class="text-pink-500 font-bold w-32">Option 3:</span>
              <span>{{ viewQuestionDetail.option3 }}</span>
          </div>
          <div class="flex items-center">
              <span class="text-pink-500 font-bold w-32">Option 4:</span>
              <span>{{ viewQuestionDetail.option4 }}</span>
          </div>
          <div class="flex items-center">
              <span class="text-pink-500 font-bold w-32">Correct Option:</span>
              <span>{{ viewQuestionDetail.correct_option }}</span>
          </div>
          </div>

          <!-- Footer with Close Button -->
          <div class="text-center mt-6">
          <button 
              @click="closeViewIdProfile" 
              class="bg-red-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-red-500 transition duration-300 shadow-md"
          >
              Close
          </button>
          </div>
      </div>
  </div>
  <!------------------------------------- Iframe Modal ----------------------------------------->
  <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50">
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg w-full max-w-md">
            <div class="text-center mb-6">
                <h5 class="text-pink-500 text-xl font-semibold mb-2">Statement Image</h5>
                <p class="text-gray-400">Question Details</p>
            </div>
            <div class="mb-6">
                <iframe sandbox="allow-scripts allow-same-origin"
                    v-if="viewQuestionDetail" 
                    :src="`http://127.0.0.1:5000/uploads/${viewQuestionDetail.question_statement.slice(viewQuestionDetail.question_statement.indexOf('/uploads') + 9)}`" 
                    class="w-full h-96 border-none rounded">
                </iframe>

            </div>
            <div class="text-center">
                <button 
                    @click="closeViewProfile" 
                    class="bg-red-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-red-500 transition"
                >
                    Close
                </button>
            </div>
        </div>
  </div>
  <!------------------------------------- Add Quiz Modal ----------------------------------------->
  <div v-if="showAddQuizModal" 
  class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50">
    <div 
      class="bg-gray-800 p-6 rounded-lg shadow-2xl w-full max-w-md text-gray-300"
    >
      <!-- Header -->
      <div class="text-center mb-6">
        <h2 class="text-2xl font-bold text-white">Add New Quiz</h2>
        <p class="text-gray-400">Fill in the details below to create a new quiz</p>
      </div>

      <!-- Form -->
      <form class="space-y-6">
        <!-- Quiz Name -->
        <div>
          <label for="name" class="block text-sm font-medium text-gray-400 mb-1">Quiz Name</label>
          <input 
            id="name"
            v-model="newQuiz.name"
            type="text"
            placeholder="Enter quiz name"
            class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            required
          />
        </div>

        <!-- Chapter Selection -->
        <div>
          <label for="chapter" class="block text-sm font-medium text-gray-400 mb-1">Select Chapter</label>
          <select 
            id="chapter"
            v-model="newQuiz.chapter_name"
            class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            required
          >
            <option disabled value="">-- Select a Chapter --</option>
            <option v-for="chapter in chapters" :key="chapter.chapter_id" :value="chapter.chapter_id">
              {{ chapter.name }}
            </option>
          </select>
        </div>

        <!-- Date and Time of Quiz -->
        <div>
          <label for="datetime" class="block text-sm font-medium text-gray-400 mb-1">Date and Time of Quiz</label>
          <input 
            id="datetime"
            v-model="newQuiz.date_of_quiz"
            type="datetime-local"
            class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            required
          />
        </div>

        <!-- Time Duration (HH:MM) -->
        <div>
          <label for="time_duration" class="block text-sm font-medium text-gray-400 mb-1">Time Duration (HH:MM)</label>
          <input 
            id="time_duration"
            v-model="newQuiz.time_duration"
            type="time"
            class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            required
          />
        </div>

        <!-- Submit Button -->
        <div class="text-center">
          <button @click="addQuiz"
            type="submit"
            class="bg-green-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-green-500 transition duration-300 shadow-md"
          >
            Add Quiz
          </button>
        </div>
      </form>


      <!-- Footer with Close Button -->
      <div class="text-center mt-4">
        <button 
          @click="closeViewQuizModal" 
          class="bg-red-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-red-500 transition duration-300 shadow-md"
        >
          Close
        </button>
      </div>
    </div>
  </div>
  <!------------------------------------- Add Question Modal ----------------------------------------->
  <div v-if="showAddQuestionModal" 
    class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50">
      <div 
        class="bg-gray-800 p-6 rounded-lg shadow-2xl w-full max-w-md text-gray-300"
      >
        <!-- Header -->
        <div class="text-center mb-6">
          <h2 class="text-2xl font-bold text-white">Add New Question</h2>
          <p class="text-gray-400">Fill in the details below to create a new question for {{ selected_quiz.name }}</p>
        </div>

        <!-- Form -->
        <form class="space-y-4">
          <!-- Question Statement (Image Upload) -->
          <div>
            <label for="question_statement" class="block text-sm font-medium text-gray-400 mb-1">
              Upload Question Image
            </label>
            <input 
              id="question_statement"
              type="file"
              @change="handleFileUpload"
              accept="image/*"
              class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
              required
            />
          </div>

          <!-- Option 1 -->
          <div>
            <label for="option1" class="block text-sm font-medium text-gray-400 mb-1">Option 1</label>
            <input 
              id="option1"
              v-model="newQuestion.option1"
              type="text"
              placeholder="Enter option 1"
              class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
              required
            />
          </div>

          <!-- Option 2 -->
          <div>
            <label for="option2" class="block text-sm font-medium text-gray-400 mb-1">Option 2</label>
            <input 
              id="option2"
              v-model="newQuestion.option2"
              type="text"
              placeholder="Enter option 2"
              class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
              required
            />
          </div>

          <!-- Option 3 -->
          <div>
            <label for="option3" class="block text-sm font-medium text-gray-400 mb-1">Option 3</label>
            <input 
              id="option3"
              v-model="newQuestion.option3"
              type="text"
              placeholder="Enter option 3"
              class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            />
          </div>

          <!-- Option 4 -->
          <div>
            <label for="option4" class="block text-sm font-medium text-gray-400 mb-1">Option 4</label>
            <input 
              id="option4"
              v-model="newQuestion.option4"
              type="text"
              placeholder="Enter option 4"
              class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            />
          </div>

          <!-- Correct Option -->
          <div>
            <label for="correct_option" class="block text-sm font-medium text-gray-400 mb-1">Correct Option</label>
            <select 
              id="correct_option"
              v-model="newQuestion.correct_option"
              class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
              required
            >
              <option disabled value="">-- Select the Correct Option --</option>
              <option value="option1">Option 1</option>
              <option value="option2">Option 2</option>
              <option value="option3">Option 3</option>
              <option value="option4">Option 4</option>
            </select>
          </div>

          <!-- Submit Button -->
          <div class="text-center">
            <button 
              @click="addingQuestion"
              type="submit"
              class="bg-green-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-green-500 transition duration-300 shadow-md"
            >
              Add Question
            </button>
          </div>
        </form>

        <!-- Footer with Close Button -->
        <div class="text-center mt-4">
          <button 
            @click="closeAddQuestionModal" 
            class="bg-red-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-red-500 transition duration-300 shadow-md"
          >
            Close
          </button>
        </div>
      </div>
  </div>
  <!------------------------------------- Else Modal ----------------------------------------->
  <div v-else class="min-h-screen bg-[#242424] p-8">
    <div class="text-center text-white text-2xl font-bold mb-6">
      Quizzes
    </div>
    <!-- Add Quiz Button -->
    <div class="mt-8 text-center">
        <button @click="viewQuizModal" class="bg-orange-500 text-white font-bold px-6 py-3 rounded-lg hover:bg-orange-400 transition">
          + Add Quiz
        </button>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 justify-items-center">
      <div
        v-for="quiz in quizzes"
        :key="quiz.quiz_id"
        class="bg-gray-800 w-full max-w-[500px] rounded-lg shadow-lg p-4">
        <h2 class="text-white text-xl font-bold mb-4 text-center">
          {{ quiz.name }}
          <button
            v-if="quiz.active"
            @click="makeInActive(quiz)"
            class="bg-white text-green-600 font-bold text-sm px-1 py-1 rounded-lg hover:bg-slate-200 transition"
          >
           Make In Active
          </button>
          <button
            v-else
            @click="makeActive(quiz)"
            class="bg-green-600 text-white text-sm font-bold px-1 py-1 rounded-lg hover:bg-green-500 transition"
          >
            Make Active
          </button>
        </h2>
        <table class="w-full border-collapse text-left">
          <thead>
            <tr class="bg-gray-700 text-white">
              <th class="px-4 py-2 border-b border-gray-600">Question Id</th>
              <th class="px-4 py-2 border-b border-gray-600">Correct Option</th>
              <th class="px-4 py-2 border-b border-gray-600">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="question in quiz.questions"
              :key="question.name"
              class="bg-gray-600 text-gray-300 hover:bg-gray-500 transition"
            >
              <td class="border-b border-gray-600 px-4 py-2">
                    <button 
                        @click="viewQuesDetailFunction(question)" 
                        class="w-10 h-10 bg-pink-600 text-white rounded-full flex items-center justify-center shadow-lg hover:bg-pink-500 transition">
                        <span class="text-sm font-bold">i</span>
                    </button>
                </td>
              <td class="px-4 py-2 border-b border-gray-600">{{ question.correct_option }}</td>
              <td class="px-4 py-2 border-b border-gray-600">
                <button
                  class="text-green-400 hover:text-green-200 transition"
                  @click="viewProfile(question)"
                >
                  View
                </button>
                /
                <button
                  class="text-blue-400 hover:text-blue-200 transition"
                  @click="editQuestion(question,quiz)"
                >
                  Edit
                </button>
                /
                <button
                  class="text-red-400 hover:text-red-200 transition"
                  @click="deleteQuestion(question.question_id)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="text-center mt-4">
          <button
            @click="addQuestion(quiz)"
            class="bg-pink-600 text-white font-bold px-6 py-2 rounded-lg hover:bg-pink-500 transition"
          >
            + Question
          </button>
        </div>
        <div class="flex justify-center gap-4 mt-4">
          <button
            @click="editQuiz(quiz)"
            class="bg-blue-600 text-white font-bold px-6 py-2 rounded-lg hover:bg-blue-500 transition"
          >
            Edit Quiz
          </button>
          <button
            @click="deleteQuiz(quiz.quiz_id,quiz.name)"
            class="bg-red-600 text-white font-bold px-6 py-2 rounded-lg hover:bg-red-500 transition"
          >
            Delete Quiz
          </button>
        </div>
      </div>
    </div>
    <!-- Edit Quiz Modal -->
    <div
      v-if="showEditQuizModal"
      class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50"
    >
      <div class="bg-gray-800 p-6 rounded-lg shadow-2xl w-full max-w-md text-gray-300">
        <!-- Header -->
        <div class="text-center mb-6">
          <h2 class="text-2xl font-bold text-white">Edit Quiz</h2>
          <p class="text-gray-400">Modify the details of the quiz</p>
        </div>

        <!-- Edit Form -->
        <form>
          <div class="space-y-4">
            <!-- Quiz Name -->
            <div>
              <label for="quizName" class="block font-bold text-gray-400 mb-1">Quiz Name</label>
              <input
                id="quizName"
                v-model="editedQuiz.name"
                type="text"
                class="w-full p-2 bg-gray-700 rounded-lg text-white border border-gray-600"
              />
            </div>

            <!-- Chapter -->
            <div>
              <label for="quizChapter" class="block font-bold text-gray-400 mb-1">Chapter</label>
              <select
                id="quizChapter"
                v-model="editedQuiz.chapter_name"
                class="w-full p-2 bg-gray-700 rounded-lg text-white border border-gray-600"
              >
                <option v-for="chapter in chapters" :value="chapter.chapter_id" :key="chapter.chapter_id">
                  {{ chapter.name }}
                </option>
              </select>
            </div>

            <!-- Date of Quiz -->
            <div>
              <label for="quizDate" class="block font-bold text-gray-400 mb-1">Date of Quiz</label>
              <input
                id="quizDate"
                v-model="editedQuiz.date_of_quiz"
                type="datetime-local"
                class="w-full p-2 bg-gray-700 rounded-lg text-white border border-gray-600"
              />
            </div>

            <!-- Time Duration -->
            <div>
              <label for="quizDuration" class="block font-bold text-gray-400 mb-1">Time Duration (HH:MM)</label>
              <input
                id="quizDuration"
                v-model="editedQuiz.time_duration"
                type="time"
                step="1"
                class="w-full p-2 bg-gray-700 rounded-lg text-white border border-gray-600"
              />
            </div>
          </div>

          <!-- Footer -->
          <div class="text-center mt-6">
            <button
              @click="saveEditedQuiz"
              type="submit"
              class="bg-green-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-green-500 transition"
            >
              Save Changes
            </button>
            <button
              @click="closeEditModal"
              type="button"
              class="bg-red-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-red-500 transition"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
    <!-- Edit Question Modal -->
    <div
      v-if="showEditQuestionModal"
      class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50"
    >
      <div class="bg-gray-800 p-2 rounded-lg shadow-2xl w-full max-w-md text-gray-300">
        <!-- Header -->
        <div class="text-center mb-2">
          <h2 class="text-2xl font-bold text-white">Edit Question</h2>
          <p class="text-gray-400">Modify the details of the question</p>
        </div>

        <!-- Edit Form -->
        <form>
          <div class="space-y-2">
            <!-- Question Statement -->
            <div>
              <label for="question_statement" class="block text-sm font-medium text-gray-400 mb-1">
                Upload Question Image
              </label>
              <input 
                id="question_statement"
                type="file"
                @change="handleFileUploadForEditing"
                accept="image/*"
                class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
              />
            </div>

            <!-- Option 1 -->
            <div>
              <label for="option1" class="block font-bold text-gray-400 mb-1">Option 1</label>
              <textarea
                id="option1"
                v-model="editedQuestion.option1"
                rows="2"
                class="w-full p-1 bg-gray-700 rounded-lg text-white border border-gray-600"
              ></textarea>
            </div>

            <!-- Option 2 -->
            <div>
              <label for="option2" class="block font-bold text-gray-400 mb-1">Option 2</label>
              <textarea
                id="option2"
                v-model="editedQuestion.option2"
                rows="2"
                class="w-full p-1 bg-gray-700 rounded-lg text-white border border-gray-600"
              ></textarea>
            </div>

            <!-- Option 3 -->
            <div>
              <label for="option3" class="block font-bold text-gray-400 mb-1">Option 3</label>
              <textarea
                id="option3"
                v-model="editedQuestion.option3"
                rows="2"
                class="w-full p-1 bg-gray-700 rounded-lg text-white border border-gray-600"
              ></textarea>
            </div>

            <!-- Option 4 -->
            <div>
              <label for="option4" class="block font-bold text-gray-400 mb-1">Option 4</label>
              <textarea
                id="option4"
                v-model="editedQuestion.option4"
                rows="2"
                class="w-full p-1 bg-gray-700 rounded-lg text-white border border-gray-600"
              ></textarea>
            </div>

            <!-- Correct Option -->
            <div>
              <label for="correctOption" class="block font-bold text-gray-400 mb-1">Correct Option</label>
              <select
                id="correctOption"
                v-model="editedQuestion.correct_option"
                class="w-full p-2 bg-gray-700 rounded-lg text-white border border-gray-600"
              >
                <option value="option1">Option 1</option>
                <option value="option2">Option 2</option>
                <option value="option3">Option 3</option>
                <option value="option4">Option 4</option>
              </select>
            </div>
          </div>

          <!-- Footer -->
          <div class="text-center mt-6">
            <button
              @click="saveEditedQuestion"
              type="submit"
              class="bg-green-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-green-500 transition"
            >
              Save Changes
            </button>
            <button
              @click="closeEditQuestion"
              type="button"
              class="bg-red-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-red-500 transition"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>


  </div>
</template>


<script setup>
  import { reactive,onMounted,ref } from 'vue';
  ////////////////////////////////////////////////  Initialization  ///////////////////////////////////////////////////

  const quizzes = ref([]);
  const chapters = ref([]);
  const viewQuestionDetail = ref({});
  const showModal = ref(false);
  const showIdModal = ref(false);
  const showAddQuizModal = ref(false);
  const showAddQuestionModal = ref(false);
  const showEditQuizModal = ref(false);
  const showEditQuestionModal = ref(false);
  const editedQuiz = reactive({ name: '', chapter_name:'', date_of_quiz:'', time_duration:'',quiz_id: null});
  const editedQuestion = reactive({question_id:null, question_statement:'', option1:'', option2:'', option3:'', option4:'', correct_option:''});

  const newQuiz = reactive({
      name: '',
      chapter_name:'',
      date_of_quiz:'',
      time_duration:''
    });

  const selected_quiz = reactive({
      id:null,
      name:'',
    });

  const newQuestion = reactive({
      question_statement:null,
      option1:'',
      option2:'',
      option3:'',
      option4:'',
      correct_option:''
    });



  function give_chapter_name(chapter_id) {
    const chapterList = chapters.value;
    const chapter = chapterList.find(
        element => element.chapter_id === chapter_id || element.chapter_id === String(chapter_id)
    );
    return chapter ? chapter.name : "Unknown Chapter";
  }
  ////////////////////////////////////////////////  Quizzzes MODALS ///////////////////////////////////////////////////
  // Quiz Add Modal
  const viewQuizModal = () => {
      showAddQuizModal.value = true;
  }

  const closeViewQuizModal = () => {
      newQuiz.name=''
      newQuiz.chapter_name=''
      newQuiz.time_duration=''
      newQuiz.date_of_quiz=''
      showAddQuizModal.value = false;
  }
  // Quiz Edit Modal
  function editQuiz(quiz) {
    editedQuiz.chapter_name = quiz.chapter_id;
    editedQuiz.quiz_id = quiz.quiz_id;
    editedQuiz.name = quiz.name;
    editedQuiz.date_of_quiz = formatDateTimeForInput(quiz.date_of_quiz);
    editedQuiz.time_duration = quiz.time_duration;
    showEditQuizModal.value = true;
  }


  function formatDateTimeForInput(dateString) {
    const date = new Date(dateString); // Convert to Date object
    const yyyy = date.getFullYear();
    const MM = String(date.getMonth() + 1).padStart(2, "0"); // Months are zero-based
    const dd = String(date.getDate()).padStart(2, "0");
    const hh = String(date.getHours()).padStart(2, "0");
    const mm = String(date.getMinutes()).padStart(2, "0");
    return `${yyyy}-${MM}-${dd}T${hh}:${mm}`;
  }


  function closeEditModal(){
    editedQuiz.chapter_name = '';
    editedQuiz.name = '';
    editedQuiz.date_of_quiz = '';
    editedQuiz.time_duration = '';
    showEditQuizModal.value=false;
  }
 ////////////////////////////////////////////////  Questions MODALS ///////////////////////////////////////////////////
  // Question Add Modal
  const addQuestion = (quiz) => {
    selected_quiz.id = quiz.quiz_id;
    selected_quiz.name = quiz.name;
    showAddQuestionModal.value = true;
  };

  const closeAddQuestionModal = () => {
    selected_quiz.quiz_id = null;
    selected_quiz.name = '';
    showAddQuestionModal.value = false;
  }
  // Question Edit Modal
  const editQuestion = (question,quiz) => {
    editedQuestion.option1 = question.option1
    editedQuestion.option2 = question.option2
    editedQuestion.option3 = question.option3
    editedQuestion.option4 = question.option4
    editedQuestion.correct_option = question.correct_option
    editedQuestion.question_id = question.question_id
    selected_quiz.id = quiz.quiz_id;
    selected_quiz.name = quiz.name;
    showEditQuestionModal.value=true;
  }

  const closeEditQuestion = () => {
    editedQuestion.option1 = '';
    editedQuestion.option2 = '';
    editedQuestion.option3 = '';
    editedQuestion.option4 = '';
    editedQuestion.correct_option = '';
    editedQuestion.question_statement = null;
    editedQuestion.question_id = null;
    selected_quiz.id = null;
    selected_quiz.name = '';
    showEditQuestionModal.value = false;
  }

 ////////////////////////////////////////////////  Iframe MODALS ///////////////////////////////////////////////////


  const viewProfile = (question) => {
      viewQuestionDetail.value = question;
      showModal.value = true;
  }

  const closeViewProfile = () => {
      viewQuestionDetail.value = null;
      showModal.value = false;
  }

  const viewQuesDetailFunction = (question) => {
      viewQuestionDetail.value = question;
      showIdModal.value = true;
  }

  const closeViewIdProfile = () => {
      viewQuestionDetail.value=null;
      showIdModal.value = false;
  }

  onMounted(() => {
        fetch('http://127.0.0.1:5000/api/getQuizzes')
        .then(response=>response.json())
        .then(data=>{
            quizzes.value = data;
        })
        fetch('http://127.0.0.1:5000/api/getChapters')
        .then(response=>response.json())
        .then(data=>{
          chapters.value = data;
        })
  });

  ////////////////////////////////////////////////  Quiz  ///////////////////////////////////////////////////

  const addQuiz = () => {
    if(newQuiz.name!=='' && newQuiz.chapter_name!=='' && newQuiz.date_of_quiz!=='' && newQuiz.time_duration!==''){
      fetch('http://127.0.0.1:5000/api/postQuiz',{
          method:'POST',
          body:JSON.stringify({
            name:newQuiz.name,
            chapter_name:newQuiz.chapter_name,
            date_of_quiz:newQuiz.date_of_quiz,
            time_duration:newQuiz.time_duration
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
    }else{
      alert('Fill The Fields Please!')
    }
};

  const saveEditedQuiz = () => {
    fetch('http://127.0.0.1:5000/api/editQuiz',{
        method:'POST',
        body:JSON.stringify({
          chapter_name:editedQuiz.chapter_name,
          name:editedQuiz.name,
          quiz_id:editedQuiz.quiz_id,
          time_duration:editedQuiz.time_duration,
          date_of_quiz:editedQuiz.date_of_quiz
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
  }

  const deleteQuiz = (quiz_id,name) => {
    let confirmed = window.confirm('Do you want to delete ' + name);
    if (confirmed){
      let confirmed2 = window.confirm('It will Delete All the questions also!!.Do you Still Want to continue?');
      if (confirmed2){
        fetch('http://127.0.0.1:5000/api/deleteQuiz',{
            method:'POST',
            body:JSON.stringify({
              id:quiz_id,
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
                window.location.reload();
            }
        });
      }
    }
  }

  const makeActive = (quiz) => {
    fetch('http://127.0.0.1:5000/api/makeActive',{
      method:'POST',
      body:JSON.stringify({
        id:quiz.quiz_id,
      }),
      headers:{
          'Content-Type':'application/json',
          'Authentication-Token':localStorage.getItem('token')
      }  
    })
    .then(response=>response.json())
    .then(data=>{
      if(data.success){
        window.location.reload();
      }
    })
  }

  const makeInActive = (quiz) => {
    fetch('http://127.0.0.1:5000/api/makeInActive',{
      method:'POST',
      body:JSON.stringify({
        id:quiz.quiz_id,
      }),
      headers:{
          'Content-Type':'application/json',
          'Authentication-Token':localStorage.getItem('token')
      }
    })
    .then(response=>response.json())
    .then(data=>{
      if(data.success){
        window.location.reload();
      }
    })
  }

  ////////////////////////////////////////////////  Question  ///////////////////////////////////////////////////

  const addingQuestion = () => {
    if (
      newQuestion.option1 !== '' &&
      newQuestion.option2 !== '' &&
      newQuestion.option3 !== '' &&
      newQuestion.option4 !== '' &&
      newQuestion.correct_option !== '' &&
      newQuestion.question_statement // Ensure file is selected
    ) {
      // Create a FormData object
      const formData = new FormData();

      // Append fields to FormData
      formData.append('quiz_id', selected_quiz.id);
      formData.append('option1', newQuestion.option1);
      formData.append('option2', newQuestion.option2);
      formData.append('option3', newQuestion.option3);
      formData.append('option4', newQuestion.option4);
      formData.append('correct_option', newQuestion.correct_option);
      formData.append('question_statement', newQuestion.question_statement); // File object

      fetch('http://127.0.0.1:5000/api/postQuestion', {
        method: 'POST',
        body: formData, // Send FormData as the body
        headers: {
          'Authentication-Token': localStorage.getItem('token') // No 'Content-Type' header for FormData
        }
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert(data.message);
          } else {
            alert('Error: ' + data.message);
          }
        });
    } else {
      alert('Fill all the fields, including the file!');
    }
  };

  const saveEditedQuestion = () => {
    // Create a FormData object
    const formData = new FormData();

    // Append fields to FormData
    formData.append('quiz_id', selected_quiz.id);
    formData.append('question_id', editedQuestion.question_id);
    formData.append('option1', editedQuestion.option1);
    formData.append('option2', editedQuestion.option2);
    formData.append('option3', editedQuestion.option3);
    formData.append('option4', editedQuestion.option4);
    formData.append('correct_option', editedQuestion.correct_option);
    formData.append('question_statement', editedQuestion.question_statement);

    fetch('http://127.0.0.1:5000/api/editQuestion',{
        method:'POST',
        body:formData,
        headers:{
            'Authentication-Token':localStorage.getItem('token')
        }
    })
    .then(response=>response.json())
    .then(data=>{
        if(data.success){
            alert(data.message);
        }
    })
  }

  const deleteQuestion = (question_id) => {
    let confirmed = window.confirm('Do you want to delete Question with id:' + question_id);
    if (confirmed){
      fetch('http://127.0.0.1:5000/api/deleteQuestion',{
          method:'POST',
          body:JSON.stringify({
            id:question_id,
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
              window.location.reload();
          }
      })
    }
  }

  // Handle file upload
  const handleFileUpload = (event) => {
    const file = event.target.files[0]; // Get the first selected file
    if (file) {
      newQuestion.question_statement = file; // Assign the file to the reactive object
    } else {
      newQuestion.question_statement = null; // Reset if no file is selected
    }
  };

  const handleFileUploadForEditing = (event) => {
    const file = event.target.files[0]; // Get the first selected file
    if (file) {
      editedQuestion.question_statement = file; // Assign the file to the reactive object
    } else {
      editedQuestion.question_statement = null; // Reset if no file is selected
    }
  };

  

</script>