<script setup>
    import { useRouter } from 'vue-router'; // Vue 3 router hook
    import { RouterLink } from 'vue-router';
    // Router setup
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
    }

</script>

<template>
    <nav class="bg-gray-400 rounded shadow-inner p-4 h-20 sticky top-0">
        <ul class="flex flex-row space-x-4">
            <li class="">
                <router-link  to="/admin/dashboard">
                    <button class="relative overflow-hidden bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg group">
                        <span class="absolute inset-0 bg-[#242424] transition-transform transform scale-x-0 group-hover:scale-x-100 origin-left"></span>
                        <span class="relative z-10">Home</span>
                    </button>
                </router-link>
            </li>
            <li class="">
                <router-link to="/admin/quiz">
                    <button class="relative overflow-hidden bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg group">
                        <span class="absolute inset-0 bg-[#242424] transition-transform transform scale-x-0 group-hover:scale-x-100 origin-left"></span>
                        <span class="relative z-10">Quiz</span>
                    </button>
                </router-link>
            </li>
            <li class="">
                <router-link to="/admin/user">
                    <button class="relative overflow-hidden bg-gray-600 text-white font-semibold py-2 px-6 rounded-lg group">
                        <span class="absolute inset-0 bg-[#242424] transition-transform transform scale-x-0 group-hover:scale-x-100 origin-left"></span>
                        <span class="relative z-10">User</span>
                    </button>
                </router-link>
            </li>
            <li class="">
                <router-link to="/admin/summary">
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
    </nav>
    <router-view></router-view>
</template>