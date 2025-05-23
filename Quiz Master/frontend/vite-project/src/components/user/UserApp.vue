<script setup>
    import { onMounted } from 'vue';
    import { useRouter } from 'vue-router'; 
    import { RouterLink } from 'vue-router';
    import { useMainStore } from '../../store';

    const store = useMainStore();

    const router = useRouter();
    
    const logout_func = () => {

        fetch("http://127.0.0.1:5000/api/logout")
        .then((res) => {
            alert("Logged out successfuly!")
        })
        .then((data) => {
            router.push("/");
        })
        .catch((err) => {
            alert("Some error occured during Log-out");
        })
        localStorage.removeItem('token')
        localStorage.removeItem('User_email')
        localStorage.removeItem('User_password')
        localStorage.removeItem('maintoken')
    }

    onMounted(() => {
    });

</script>

<template>
    <nav v-if="store.maintoken===0" class="bg-gray-400 rounded shadow-inner p-4 h-20 sticky top-0 flex justify-between items-center">
        <ul class="flex flex-row space-x-4">
            <li class="">
            <router-link to="/user/uhome">
                <button class="relative overflow-hidden bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg group">
                <span class="absolute inset-0 bg-[#242424] transition-transform transform scale-x-0 group-hover:scale-x-100 origin-left"></span>
                <span class="relative z-10">Home</span>
                </button>
            </router-link>
            </li>
            <li class="">
            <router-link to="/user/uscore">
                <button class="relative overflow-hidden bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg group">
                <span class="absolute inset-0 bg-[#242424] transition-transform transform scale-x-0 group-hover:scale-x-100 origin-left"></span>
                <span class="relative z-10">Scores</span>
                </button>
            </router-link>
            </li>
            <li class="">
            <router-link to="/user/usummary">
                <button class="relative overflow-hidden bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg group">
                <span class="absolute inset-0 bg-[#242424] transition-transform transform scale-x-0 group-hover:scale-x-100 origin-left"></span>
                <span class="relative z-10">Summary</span>
                </button>
            </router-link>
            </li>
            <li>
            <button @click="logout_func" class="relative overflow-hidden bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg group">
                <span class="absolute inset-0 bg-[#242424] transition-transform transform scale-x-0 group-hover:scale-x-100 origin-left"></span>
                <span class="relative z-10">Log out</span>
            </button>
            </li>
        </ul>

        <div class="flex items-center space-x-4">
            <div class="relative">
            <input
                type="text"
                placeholder="Search..."
                class="px-4 py-2 w-64 bg-gray-600 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-pink-500"
            />
            <button class="absolute right-1 top-1/2 transform -translate-y-1/2 bg-pink-500 text-white px-4 py-1 rounded-lg hover:bg-pink-600 transition duration-300">
                Search
            </button>
            </div>
            <div>
            <span class="text-lg text-white font-semibold">Welcome, User</span>
            </div>
        </div>
    </nav>

    <router-view></router-view>
</template>