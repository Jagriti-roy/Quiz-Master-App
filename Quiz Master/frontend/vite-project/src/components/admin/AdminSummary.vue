<template>
    <div class="p-6 text-white">
      <h1 class="text-2xl font-bold mb-4">Admin Summary</h1>
  
      <!-- Subject-Wise Topic Scores Bar Chart -->
      <div class="mb-6">
        <h2 class="text-lg font-semibold mb-2">Subject-Wise Topic Scores</h2>
        <canvas id="scoreBarChart"></canvas>
      </div>
  
      <!-- Subject-Wise User Attempts Pie Chart -->
      <div>
        <h2 class="text-lg font-semibold mb-2">Subject-Wise User Attempts</h2>
        <canvas id="attemptPieChart"></canvas>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from "vue";
  import { Chart } from "chart.js/auto";
  
  // Data for the charts
  const scoreData = {
    labels: ["Math", "Science", "History", "English", "Physics"],
    datasets: [
      {
        label: "Average Scores",
        data: [85, 78, 90, 88, 70],
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
        borderColor: "#333",
        borderWidth: 1,
      },
    ],
  };
  
  const attemptData = {
    labels: ["Math", "Science", "History", "English", "Physics"],
    datasets: [
      {
        label: "User Attempts",
        data: [50, 30, 70, 40, 60],
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
      },
    ],
  };
  
  // Mount the charts
  onMounted(() => {
    // Subject-Wise Topic Scores Bar Chart
    new Chart(document.getElementById("scoreBarChart"), {
      type: "bar",
      data: scoreData,
      options: {
        responsive: true,
        plugins: {
          legend: { display: true },
        },
      },
    });
  
    // Subject-Wise User Attempts Pie Chart
    new Chart(document.getElementById("attemptPieChart"), {
      type: "pie",
      data: attemptData,
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
  