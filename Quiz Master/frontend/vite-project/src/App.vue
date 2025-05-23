<script setup>
  import { useMainStore } from './store';

  const store = useMainStore();
  const setMainToken = (value) => {
    store.setMainToken(value);
  };

</script>

<template>
  <router-view></router-view>
</template>

<style scoped>

</style>
