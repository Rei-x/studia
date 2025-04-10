<template>
  <component :is="layout">
    <slot />
  </component>
</template>

<script lang="ts">
import AppLayoutDefault from './AppLayoutDefault.vue'
import { markRaw, watch } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'RootLayout',
  setup() {
    const layout = markRaw(AppLayoutDefault)
    const route = useRoute()
    watch(
      () => route.meta,
      async (meta) => {
        try {
          const component = await import(`@/layouts/AppLayout${meta.layout}.vue`)
          layout.value = component?.default || AppLayoutDefault
        } catch {
          layout.value = AppLayoutDefault
        }
      },
      { immediate: true },
    )
    return { layout }
  },
}
</script>
