<script setup lang="ts">
import AppNavbar from '@/components/AppNavbar.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <AppNavbar />
    <main class="p-6">
      <slot />
    </main>
  </div>
</template>
