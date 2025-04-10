<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <nav class="bg-blue-600 text-white py-3 mb-4">
    <div class="max-w-5xl mx-auto px-6 flex items-center justify-between">
      <div class="flex space-x-6 items-center">
        <RouterLink to="/" class="text-lg font-semibold hover:text-blue-200 transition">
          Book App
        </RouterLink>

        <div class="flex space-x-4">
          <RouterLink
            to="/"
            class="hover:text-blue-200 transition py-1 px-2"
            :class="route.path === '/' ? 'bg-blue-700 rounded' : ''"
          >
            Books
          </RouterLink>
          <RouterLink
            to="/lendings"
            class="hover:text-blue-200 transition py-1 px-2"
            :class="route.path === '/lendings' ? 'bg-blue-700 rounded' : ''"
          >
            Lendings
          </RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>
