<template>
  <!------------------------------------- Add Subject Modal ----------------------------------------->
  <div v-if="showAddSubjectModal" 
  class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50">
    <div 
      class="bg-gray-800 p-6 rounded-lg shadow-2xl w-full max-w-md text-gray-300"
    >
      <!-- Header -->
      <div class="text-center mb-6">
        <h2 class="text-2xl font-bold text-white">Add New Subject</h2>
        <p class="text-gray-400">Fill in the details below to create a new subject</p>
      </div>

      <!-- Form -->
      <form class="space-y-4">
        <!-- Subject Name -->
        <div>
          <label for="name" class="block text-sm font-medium text-gray-400 mb-1">Subject Name</label>
          <input id="name"
            v-model="newSubject.name"
            type="text" 
            placeholder="Enter subject name"
            class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            required
          />
        </div>

        <!-- Description -->
        <div>
          <label for="description" class="block text-sm font-medium text-gray-400 mb-1">Description</label>
          <textarea id="description"
            v-model="newSubject.description"
            placeholder="Enter subject description"
            class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            rows="4"
            required
          ></textarea>
        </div>

        <!-- Submit Button -->
        <div class="text-center">
          <button type="submit"
             @click="addSubject"
            class="bg-green-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-green-500 transition duration-300 shadow-md"
          >
            Add Subject
          </button>
        </div>
      </form>

      <!-- Footer with Close Button -->
      <div class="text-center mt-4">
        <button 
          @click="closeViewSubjectModal" 
          class="bg-red-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-red-500 transition duration-300 shadow-md"
        >
          Close
        </button>
      </div>
    </div>
  </div>
  <!------------------------------------- Add Chapter Modal ----------------------------------------->
  <div v-if="showAddChapterModal" 
  class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50">
    <div 
      class="bg-gray-800 p-6 rounded-lg shadow-2xl w-full max-w-md text-gray-300"
    >
      <!-- Header -->
      <div class="text-center mb-6">
        <h2 class="text-2xl font-bold text-white">Add New Chapter</h2>
        <p class="text-gray-400">Fill in the details below to create a new chapter in {{ selected_subject.name }}</p>
      </div>

      <!-- Form -->
      <form class="space-y-4">
        <!-- Chapter Name -->
        <div>
          <label for="name" class="block text-sm font-medium text-gray-400 mb-1">Chapter Name</label>
          <input id="name"
            v-model="newChapter.name"
            type="text" 
            placeholder="Enter chapter name"
            class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            required
          />
        </div>

        <!-- Description -->
        <div>
          <label for="description" class="block text-sm font-medium text-gray-400 mb-1">Description</label>
          <textarea id="description"
            v-model="newChapter.description"
            placeholder="Enter chapter description"
            class="w-full px-4 py-2 bg-gray-700 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            rows="4"
            required
          ></textarea>
        </div>

        <!-- Submit Button -->
        <div class="text-center">
          <button type="submit"
             @click="addingChapter"
            class="bg-green-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-green-500 transition duration-300 shadow-md"
          >
            Add Chapter
          </button>
        </div>
      </form>

      <!-- Footer with Close Button -->
      <div class="text-center mt-4">
        <button 
          @click="closeAddChapterModal" 
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
      Subjects
    </div>
    <!-- Add Subject Button -->
    <div class="mt-8 text-center">
        <button @click="viewSubjectModal" class="bg-orange-500 text-white font-bold px-6 py-3 rounded-lg hover:bg-orange-400 transition">
          + Add Subject
        </button>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 justify-items-center">
      <div
        v-for="subject in subjects"
        :key="subject.subject_id"
        class="bg-gray-800 w-full max-w-[500px] rounded-lg shadow-lg p-4">
        <h2 class="text-white text-xl font-bold mb-4 text-center">
          {{ subject.name }}
        </h2>
        <table class="w-full border-collapse text-left">
          <thead>
            <tr class="bg-gray-700 text-white">
              <th class="px-4 py-2 border-b border-gray-600">Chapter Name</th>
              <th class="px-4 py-2 border-b border-gray-600">Description</th>
              <th class="px-4 py-2 border-b border-gray-600">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="chapter in subject.chapters"
              :key="chapter.name"
              class="bg-gray-600 text-gray-300 hover:bg-gray-500 transition"
            >
              <td class="px-4 py-2 border-b border-gray-600">{{ chapter.name }}</td>
              <td class="px-4 py-2 border-b border-gray-600">{{ chapter.description }}</td>
              <td class="px-4 py-2 border-b border-gray-600">
                <button
                  class="text-blue-400 hover:text-blue-200 transition"
                  @click="editChapter(chapter,subject)"
                >
                  Edit
                </button>
                /
                <button
                  class="text-red-400 hover:text-red-200 transition"
                  @click="deleteChapter(chapter.chapter_id, chapter.name)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="text-center mt-4">
          <button
            @click="addChapter(subject)"
            class="bg-pink-600 text-white font-bold px-6 py-2 rounded-lg hover:bg-pink-500 transition"
          >
            + Chapter
          </button>
        </div>
        <div class="flex justify-center gap-4 mt-4">
          <button
            @click="editSubject(subject)"
            class="bg-blue-600 text-white font-bold px-6 py-2 rounded-lg hover:bg-blue-500 transition"
          >
            Edit Subject
          </button>
          <button
            @click="deleteSubject(subject.subject_id,subject.name)"
            class="bg-red-600 text-white font-bold px-6 py-2 rounded-lg hover:bg-red-500 transition"
          >
            Delete Subject
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Subject Modal -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50"
    >
      <div
        class="bg-gray-800 p-6 rounded-lg shadow-2xl w-full max-w-md text-gray-300"
      >
        <!-- Header -->
        <div class="text-center mb-6">
          <h2 class="text-2xl font-bold text-white">Edit Subject</h2>
          <p class="text-gray-400">Modify the details of the subject</p>
        </div>

        <!-- Edit Form -->
        <form>
          <div class="space-y-4">
            <div>
              <label for="subjectName" class="block font-bold text-gray-400 mb-1">
                Subject Name
              </label>
              <input
                id="subjectName"
                v-model="editedSubject.name"
                type="text"
                class="w-full p-2 bg-gray-700 rounded-lg text-white border border-gray-600"
              />
            </div>
            <div>
              <label
                for="subjectDescription"
                class="block font-bold text-gray-400 mb-1"
              >
                Description
              </label>
              <textarea
                id="subjectDescription"
                v-model="editedSubject.description"
                rows="4"
                class="w-full p-2 bg-gray-700 rounded-lg text-white border border-gray-600"
              ></textarea>
            </div>
          </div>

          <!-- Footer -->
          <div class="text-center mt-6">
            <button
              @click="saveEditedSubject"
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

    <!-- Edit Subject Modal -->
    <div
      v-if="showEditChapterModal"
      class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50"
    >
      <div
        class="bg-gray-800 p-6 rounded-lg shadow-2xl w-full max-w-md text-gray-300"
      >
        <!-- Header -->
        <div class="text-center mb-6">
          <h2 class="text-2xl font-bold text-white">Edit Chapter</h2>
          <p class="text-gray-400">Modify the details of the chapter in the {{ selected_subject.name }}.</p>
        </div>

        <!-- Edit Form -->
        <form>
          <div class="space-y-4">
            <div>
              <label for="chapterName" class="block font-bold text-gray-400 mb-1">
                Chapter Name
              </label>
              <input
                id="chapterName"
                v-model="editedChapter.name"
                type="text"
                class="w-full p-2 bg-gray-700 rounded-lg text-white border border-gray-600"
              />
            </div>
            <div>
              <label
                for="chapterDescription"
                class="block font-bold text-gray-400 mb-1"
              >
                Description
              </label>
              <textarea
                id="chapterDescription"
                v-model="editedChapter.description"
                rows="4"
                class="w-full p-2 bg-gray-700 rounded-lg text-white border border-gray-600"
              ></textarea>
            </div>
          </div>

          <!-- Footer -->
          <div class="text-center mt-6">
            <button
              @click="saveEditedChapter"
              type="submit"
              class="bg-green-600 text-white font-medium px-6 py-2 rounded-lg hover:bg-green-500 transition"
            >
              Save Changes
            </button>
            <button
              @click="closeEditChapter"
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

  const subjects = ref([]);
  const showAddSubjectModal = ref(false);
  const showAddChapterModal = ref(false);
  const showEditModal = ref(false);
  const showEditChapterModal = ref(false);
  const editedSubject = reactive({ name: '', description: '' ,subject_id: null});
  const editedChapter = reactive({ name: '', description: '' ,chapter_id: null});

  const newSubject = reactive({
      name: '',
      description: '',
    });

  const selected_subject = reactive({
      id:null,
      name:'',
    });

  const newChapter = reactive({
      name:'',
      description:''
    });


  ////////////////////////////////////////////////  Subject MODALS ///////////////////////////////////////////////////
  // Subject Add Modal
  const viewSubjectModal = () => {
      showAddSubjectModal.value = true;
  }

  const closeViewSubjectModal = () => {
      newSubject.name=''
      newSubject.description=''
      showAddSubjectModal.value = false;
  }
  // Subject Edit Modal
  function editSubject(subject) {
    editedSubject.subject_id = subject.subject_id;
    editedSubject.name = subject.name;
    editedSubject.description = subject.description;
    showEditModal.value=true;
  }

  function closeEditModal(){
    showEditModal.value=false;
  }
 ////////////////////////////////////////////////  Chapter MODALS ///////////////////////////////////////////////////
  // Chapter Add Modal
  const addChapter = (subject) => {
    selected_subject.id = subject.subject_id;
    selected_subject.name = subject.name;
    showAddChapterModal.value = true;
  };

  const closeAddChapterModal = () => {
    selected_subject.id = null;
    selected_subject.name = '';
    showAddChapterModal.value = false;
  }
  // Chapter Edit Modal
  const editChapter = (chapter,subject) => {
    editedChapter.name = chapter.name
    editedChapter.description = chapter.description
    editedChapter.chapter_id = chapter.chapter_id
    selected_subject.id = subject.subject_id;
    selected_subject.name = subject.name;
    showEditChapterModal.value=true;
  }

  const closeEditChapter = () => {
    editedChapter.name = '';
    editedChapter.description = '';
    editedChapter.chapter_id = null;
    selected_subject.id = null;
    selected_subject.name = '';
    showEditChapterModal.value = false;
  }

  onMounted(() => {
        fetch('http://127.0.0.1:5000/api/getSubjects')
        .then(response=>response.json())
        .then(data=>{
            subjects.value = data;
        })
    });
  ////////////////////////////////////////////////  Subject  ///////////////////////////////////////////////////


  const addSubject = () => {
    if(newSubject.name!=='' && newSubject.description!==''){
      fetch('http://127.0.0.1:5000/api/postSubject',{
          method:'POST',
          body:JSON.stringify({
            name:newSubject.name,
            description:newSubject.description
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

  const saveEditedSubject = () => {
    fetch('http://127.0.0.1:5000/api/editSubject',{
        method:'POST',
        body:JSON.stringify({
          id:editedSubject.subject_id,
          name:editedSubject.name,
          description:editedSubject.description
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

  const deleteSubject = (subject_id,name) => {
    let confirmed = window.confirm('Do you want to delete ' + name +' Subject');
    if (confirmed){
      fetch('http://127.0.0.1:5000/api/deleteSubject',{
          method:'POST',
          body:JSON.stringify({
            id:subject_id,
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

  ////////////////////////////////////////////////  Chapter  ///////////////////////////////////////////////////

  

  const addingChapter = () => {
    if(newChapter.name!=='' && newChapter.description!==''){
      fetch('http://127.0.0.1:5000/api/postChapter',{
          method:'POST',
          body:JSON.stringify({
            subject_id:selected_subject.id,
            name:newChapter.name,
            description:newChapter.description
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
  }

  const saveEditedChapter = () => {
    fetch('http://127.0.0.1:5000/api/editChapter',{
        method:'POST',
        body:JSON.stringify({
          chapter_id:editedChapter.chapter_id,
          subject_id:selected_subject.id,
          name:editedChapter.name,
          description:editedChapter.description
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

  const deleteChapter = (chapter_id,name) => {
    let confirmed = window.confirm('Do you want to delete ' + name +' Chapter.');
    if (confirmed){
      fetch('http://127.0.0.1:5000/api/deleteChapter',{
          method:'POST',
          body:JSON.stringify({
            id:chapter_id,
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

</script>