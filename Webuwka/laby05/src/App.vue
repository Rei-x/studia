<script setup lang="ts">
import AppLayout from '@/layouts/RootLayout.vue'
import { RouterView } from 'vue-router'
import { Toaster } from '@/components/ui/sonner'
</script>

<template>
  <Toaster />
  <AppLayout>
    <RouterView />
  </AppLayout>
</template>
