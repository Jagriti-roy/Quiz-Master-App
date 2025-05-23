<script>
export default {
  data() {
    return {
      scores: [],
    };
  },
  methods: {
  formatQuizDate(dateString) {
    const options = {
      weekday: "short", 
      day: "2-digit",
      month: "long",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true, 
    };
    const date = new Date(dateString);
    return date.toLocaleString("en-US", options);
  }
  },
  mounted() {
    const userEmail = localStorage.getItem('User_email');
    fetch(`http://127.0.0.1:5000/api/getScores/${userEmail}`,{
      headers: {
        "Authentication-Token": localStorage.getItem("token"),
      },
    })
    .then(response=>response.json())
    .then(data=>{
      this.scores = data;
    })
  }
};


</script>


<template>
    <div class="p-6 bg-gray-100">
      <h2 class="text-2xl font-bold text-center mb-6">Quiz Scores</h2>
      <div class="overflow-x-auto">
        <table class="table-auto w-full border-collapse border border-gray-300 shadow-lg rounded-lg">
          <thead class="bg-gray-700 text-white">
            <tr>
              <th class="px-4 py-2 border border-gray-300">ID</th>
              <th class="px-4 py-2 border border-gray-300">No. of Questions</th>
              <th class="px-4 py-2 border border-gray-300">Date</th>
              <th class="px-4 py-2 border border-gray-300">Score</th>
            </tr>
          </thead>
          <tbody class="bg-white">
            <tr v-for="score in scores" :key="score.id" class="hover:bg-gray-100">
              <td class="px-4 py-2 border border-gray-300 text-center">{{ score.id }}</td>
              <td class="px-4 py-2 border border-gray-300 text-center">{{ score.numQuestions }}</td>
              <td class="px-4 py-2 border border-gray-300 text-center">{{ formatQuizDate(score.date) }}</td>
              <td class="px-4 py-2 border border-gray-300 text-center">{{ score.score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  