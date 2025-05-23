<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router'; // Vue 3 router hook
import { useMainStore } from '../store';

// Props
defineProps({
    title: String, // Define props correctly without dangling commas
});

const store = useMainStore(); // Create store instance

// Function to update 'condition' in the store
const setMainToken = (value) => {
    store.setMainToken(value);  // Call the action to update the state
};

// Reactive state
const logFormToggle = ref(0);
const signLogFormToggle = ref(0);
const user = reactive({
    email: '',
    fullname: '',
    password: '',
    phone: '',
    dob: '',
    qualification: null,
});

// Router setup
const router = useRouter();

// Toggle functions
const toggleLogForm = () => {
  logFormToggle.value = logFormToggle.value === 0 ? 1 : 0;
};

const toggleSignLogForm = () => {
  signLogFormToggle.value = signLogFormToggle.value === 0 ? 1 : 0;
};

// Handle file upload
const handleFileUpload = (event) => {
  const file = event.target.files[0]; // Get the first selected file
  if (file) {
    user.qualification = file; // Assign the file to the reactive object
  } else {
    user.qualification = null; // Reset if no file is selected
  }
};

// Login function
const loginfunc = () => {
    if(user.email && user.password){
        fetch('http://127.0.0.1:5000/api/authenticate', {
            body: JSON.stringify({ email: user.email, password: user.password }),
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        })
        .then(response => response.json())
        .then(data => {
            const { role, token } = data;
            document.cookie = `Authentication-Token=${token}; path=/; secure; httponly; samesite=strict`;
            localStorage.setItem("token", token);

            if (role === 'admin') {
              router.push('/admin/dashboard');
            } else if (role === 'user') {
              localStorage.setItem('User_email', user.email);
              localStorage.setItem('User_password', user.password);
              router.push('/user/uhome');
            } else {
              alert('Incorrect email or password. Please try again.');
            }
        })
        .catch(error => {
            console.error('Login failed:', error);
            alert('An error occurred. Please try again.');
        });
    }else{
        alert('All fields are required.')
    }

};

// Signup function
const user_signupfunc = async () => {
  // Validate required fields
  if (
    !user.fullname ||
    !user.email ||
    !user.password ||
    !user.dob ||
    !user.qualification
  ) {
    return alert('All fields are required!');
  }

  // Create FormData object
  const formData = new FormData();
  formData.append('fullname', user.fullname);
  formData.append('email', user.email);
  formData.append('password', user.password);
  formData.append('dob', user.dob);
  formData.append('qualification_image', user.qualification);

  try {
    const response = await fetch('http://127.0.0.1:5000/api/postUsers', {
      method: 'POST',
      body: formData,  
    });

    if (response.ok) {
      const data = await response.json();  

      if (data.success) {
        user.email = '';
        user.fullname = '';
        user.password = '';
        user.dob = '';
        user.qualification = null;

        alert('You are ready to Login!');
        window.location.reload();
      } else {
        alert('Something went wrong!');
      }
    } else {
      // Handle HTTP errors (non-2xx responses)
      alert(`HTTP Error: ${response.status}`);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred. Please try again later.');
  }
};
</script>

<template>
    <nav class="text-center bg-gray-400 rounded shadow-inner h-20 sticky top-0">
        <ul class="text-center flex flex-col space-y-2">
            <li class="text-xl font-bold"><p class="font-mono">Welcome To Quiz Master</p></li>
            <li v-if="signLogFormToggle===0" class="text-xl font-bold font-sans"><button @click="toggleSignLogForm(1)" class="bg-stone-900 px-2 py-1 text-lg font-medium text-white rounded-lg hover:scale-105 transform transition duration-300 ease-in-out">Sign-up</button></li>
            <li v-else class="text-xl font-bold font-sans"><button @click="toggleSignLogForm(0)" class="bg-stone-900 px-2 py-1 text-lg font-medium text-white rounded-lg hover:scale-105 transform transition duration-300 ease-in-out">Log-in</button></li>
        </ul>
    </nav>
    <div v-if="signLogFormToggle===0" class="flex flex-col items-center justify-center mt-48">
        <div class="h-12 w-72 bg-gray-50 mb-2 flex items-center justify-center container rounded-sm shadow-inner shadow-xl">
            <button v-if="logFormToggle===0" @click="toggleLogForm(1)" class="block bg-stone-900 px-2 py-1 text-lg font-medium text-white rounded-lg hover:scale-105 transform transition duration-300 ease-in-out">Change To Admin Form</button>
            <button v-else @click="toggleLogForm(0)" class="block bg-stone-900 px-2 py-1 text-lg font-medium text-white rounded-lg hover:scale-105 transform transition duration-300 ease-in-out">Change To User Form</button>
        </div>
        <div class="h-52 w-96 bg-gray-50 flex flex-col items-center justify-center container rounded-sm shadow-inner shadow-xl hover:scale-105 transform transition duration-300 ease-in-out">
            <span v-if="logFormToggle===0" class="block text-lg font-medium text-slate-700">User Email:</span>
            <span v-else class="block text-lg font-medium text-slate-700">Admin Email:</span>
            <input v-model="user.email" type="email" class="peer rounded-lg bg-black text-white"/>
            <p class="mt-2 invisible peer-invalid:visible text-pink-600 text-sm">
                Please provide a valid email address.
            </p>
            <span v-if="logFormToggle===0" class="block text-lg font-medium text-slate-700">User Password:</span>
            <span v-else class="block text-lg font-medium text-slate-700">Admin Password:</span>
            <input v-model="user.password" type="password" class="peer rounded-lg bg-black text-white"/>
            <button @click="loginfunc" class="block bg-stone-900 px-2 py-1 text-lg font-medium text-white rounded-lg mt-4 hover:scale-105 transform transition duration-300 ease-in-out">Log-in</button>
        </div>
    </div>
    <div v-else class="flex flex-col items-center justify-center mt-24">
        <div class="h-12 w-72 bg-gray-50 mb-2 flex items-center justify-center container rounded-sm shadow-inner shadow-xl">
            <button class="block bg-stone-900 px-2 py-1 text-lg font-medium text-white rounded-lg hover:scale-105 transform transition duration-300 ease-in-out">User Sign Up Form</button>
        </div>
        <div class="h-[370px] w-96 bg-gray-50 flex flex-col items-center justify-center container rounded-sm shadow-inner shadow-xl">
            <span class="block text-lg font-medium text-slate-700">Email:</span>
            <input v-model="user.email" type="email" class="peer rounded-lg bg-black text-white" />
            <p class="invisible peer-invalid:visible text-pink-600 text-sm">
                Please provide a valid email address.
            </p>

            <span class="block text-lg font-medium text-slate-700">Password:</span>
            <input v-model="user.password" type="password" class="peer rounded-lg bg-black text-white" />

            <span class="block text-lg font-medium text-slate-700">Fullname:</span>
            <input v-model="user.fullname" type="text" class="peer rounded-lg bg-black text-white" />

            <span class="block text-lg font-medium text-slate-700">Qualification:</span>
            <p class="visible text-sm">Please provide a valid 12th Class Result.</p>
            <input @change="handleFileUpload"
                type="file" 
                accept=".pdf,.doc,.docx,.jpg,.png" 
                class="peer rounded-lg bg-black text-white file:cursor-pointer file:bg-gray-700 file:text-white file:rounded-md file:px-3 file:py-1 file:border-none"
            />

            <span class="block text-lg font-medium text-slate-700">Dob:</span>
            <input v-model="user.dob" 
                type="date" 
                class="peer rounded-lg text-slate-700 border-2 border-black" 
            />

            <button @click="user_signupfunc" class="block bg-stone-900 px-2 py-1 text-lg font-medium text-white rounded-lg mt-2 hover:scale-105 transform transition duration-300 ease-in-out">
                Sign-up
            </button>
        </div>
    </div>
</template>