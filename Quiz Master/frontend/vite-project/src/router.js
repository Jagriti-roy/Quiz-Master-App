import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import HelloWorld from './components/HelloWorld.vue'
import AppNavbar from './components/AppNavbar.vue';
import AdminHome from './components/admin/AdminHome.vue';
import AdminNavbar from './components/admin/AdminNavbar.vue';
import AdminQuiz from './components/admin/AdminQuiz.vue';
import AdminUser from './components/admin/AdminUser.vue';
import AdminSummary from './components/admin/AdminSummary.vue';
import UserApp from './components/user/UserApp.vue';
import UserHome from './components/user/UserHome.vue';
import UserScore from './components/user/UserScore.vue';
import UserSummary from './components/user/UserSummary.vue';
import UserQuizStarting from './components/user/UserQuizStarting.vue';

const routes = [
  { path: '/', component: AppNavbar, name: 'AppNavbar' },

  
  {
    path: '/user',
    component: UserApp,
    children: [
        { path: 'uhome', component: UserHome },
        { path: 'uscore', component: UserScore },
        { path: 'usummary', component: UserSummary },
        {
          path: "/user/uquizstarted/:quizId", // Define `quizId` as a route parameter
          name: "uquizstarted",          // The route's name must match what you're using in the push method
          component: UserQuizStarting,
        },
    ]
  },

  {
    path: '/admin',
    component: AdminNavbar,
    children: [
        { path: 'dashboard', component: AdminHome },
        { path: 'quiz', component: AdminQuiz },
        { path: 'user', component: AdminUser },
        { path: 'summary', component: AdminSummary },
    ]
  },

  { 
    path: '/:pathMatch(.*)*',
    name: 'NotFound', 
    component: HelloWorld
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
