<script setup>
    import { onMounted, onUpdated,ref } from 'vue';

    const users = ref([]);
    const user = ref({});
    const showModal = ref(false);
    const showIdModal = ref(false);
    onMounted(() => {
        fetch('http://127.0.0.1:5000/api/getUsers')
        .then(response=>response.json())
        .then(data=>{
            users.value = data;
        })
    });


    const viewProfile = (userProfile) => {
        user.value = userProfile;
        showModal.value = true;
    }

    const closeViewProfile = () => {
        showModal.value = false;
    }

    const viewUserDetails = (userProfile) => {
        user.value = userProfile;
        showIdModal.value = true;
    }

    const closeViewIdProfile = () => {
        showIdModal.value = false;
    }

    onUpdated(() => {
        

    });

    function formatDate(dob) {
        if (!dob) return ''; 

        const date = new Date(dob);

        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); 
        const day = String(date.getDate()).padStart(2, '0');

        return `${year}-${month}-${day}`;
    }

</script>

<template>

    <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50">
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg w-full max-w-md">
            <div class="text-center mb-6">
                <h5 class="text-pink-500 text-xl font-semibold mb-2">Qualification Docs</h5>
                <p class="text-gray-400">User Details</p>
            </div>
            <div class="mb-6">
                <iframe sandbox="allow-scripts allow-same-origin"
                    v-if="user" 
                    :src="`http://127.0.0.1:5000/uploads/${user.qualification.slice(user.qualification.indexOf('/uploads') + 9)}`" 
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

    <div 
        v-if="showIdModal" 
        class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-70 z-50"
        >
        <div 
            class="bg-gray-800 p-6 rounded-lg shadow-2xl w-full max-w-md text-gray-300"
        >
            <!-- Header -->
            <div class="text-center mb-6">
            <h2 class="text-2xl font-bold text-white">User Profile</h2>
            <p class="text-gray-400">Detailed information about the user</p>
            </div>

            <!-- User Info -->
            <div class="space-y-4">
            <div class="flex items-center">
                <span class="text-pink-500 font-bold w-32">User ID:</span>
                <span>{{ user.user_id }}</span>
            </div>
            <div class="flex items-center">
                <span class="text-pink-500 font-bold w-32">Full Name:</span>
                <span>{{ user.fullname }}</span>
            </div>
            <div class="flex items-center">
                <span class="text-pink-500 font-bold w-32">Email:</span>
                <span>{{ user.email }}</span>
            </div>
            <div class="flex items-center">
                <span class="text-pink-500 font-bold w-32">DOB:</span>
                <span>{{ formatDate(user.dob) }}</span>
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



    <div v-else class="flex flex-col items-center justify-center p-6">
        <div class="bg-gray-800 container w-[90%] max-w-[1200px] rounded-lg shadow-lg p-6">
            <h1 class="text-white text-2xl font-bold mb-4 text-center">Attractive Table</h1>
            <table class="table-auto w-full border-collapse">
            <thead>
                <tr class="bg-gray-700 text-white">
                    <th class="border border-gray-600 px-4 py-2">User Id</th>
                    <th class="border border-gray-600 px-4 py-2">Email</th>
                    <th class="border border-gray-600 px-4 py-2">Qualification</th>
                    <th class="border border-gray-600 px-4 py-2">DOB</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.user_id" class="bg-gray-600 text-gray-300 hover:bg-gray-500 transition">
                    <td class="border border-gray-600 px-4 py-2 flex justify-center items-center">
                        <button 
                            @click="viewUserDetails(user)" 
                            class="w-10 h-10 bg-pink-600 text-white rounded-full flex items-center justify-center shadow-lg hover:bg-pink-500 transition">
                            <span class="text-sm font-bold">i</span>
                        </button>
                    </td>

                    <td class="border border-gray-600 px-4 py-2">{{ user.email }}</td>
                    <td class="border border-gray-600 px-4 py-2">
                        <button 
                                @click="viewProfile(user)" 
                                class="bg-pink-600 text-white font-medium px-4 py-2 text-sm rounded hover:bg-pink-500 transition"
                            >
                                View
                        </button>

                    </td>
                    <td class="border border-gray-600 px-4 py-2">{{ formatDate(user.dob) }}</td>
                </tr>
            </tbody>
            </table>
        </div>
    </div>

</template>