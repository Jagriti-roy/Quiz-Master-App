<template>
    <div class="p-6 text-white">
      <h1 class="text-2xl font-bold mb-4">User Summary</h1>
  
      <!-- Subject-Wise Quizzes Bar Chart -->
      <div class="mb-6">
        <h2 class="text-lg font-semibold mb-2">Subject-Wise No. of Quizzes</h2>
        <canvas id="subjectBarChart"></canvas>
      </div>
  
      <!-- Month-Wise Quizzes Pie Chart -->
      <div>
        <h2 class="text-lg font-semibold mb-2">Month-Wise No. of Quizzes Attempted</h2>
        <canvas id="monthPieChart"></canvas>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from "vue";
  import { Chart } from "chart.js/auto";
  
  // Data for the charts
  const subjectData = {
    labels: ["Math", "Science", "History", "English", "Physics"],
    datasets: [
      {
        label: "Quizzes",
        data: [12, 8, 15, 10, 9],
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
        borderColor: "#333",
        borderWidth: 1,
      },
    ],
  };
  
  const monthData = {
    labels: ["January", "February", "March", "April", "May"],
    datasets: [
      {
        label: "Quizzes Attempted",
        data: [10, 7, 5, 15, 8],
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
      },
    ],
  };
  
  // Mount the charts
  onMounted(() => {
    // Subject-Wise Bar Chart
    new Chart(document.getElementById("subjectBarChart"), {
      type: "bar",
      data: subjectData,
      options: {
        responsive: true,
        plugins: {
          legend: { display: true },
        },
      },
    });
  
    // Month-Wise Pie Chart
    new Chart(document.getElementById("monthPieChart"), {
      type: "pie",
      data: monthData,
      options: {
        responsive: true,
        plugins: {
          legend: { display: true },
        },
      },
    });
  });
  </script>
  
  <style scoped>
  h1,
  h2 {
    text-align: center;
  }
  </style>
  