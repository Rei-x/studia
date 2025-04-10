<script setup lang="ts">
import { fetchClient } from '@/api/client'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { ref } from 'vue'
import { TrashIcon } from 'lucide-vue-next'

const props = defineProps<{
  bookId: number
  bookTitle?: string
}>()

const isOpen = ref(false)

const deleteError = ref('')

const queryClient = useQueryClient()

const deleteBook = useMutation({
  mutationFn: async (id: number) => {
    const response = await fetchClient.DELETE(`/api/v1/books/{id}`, {
      params: {
        path: {
          id,
        },
      },
    })
    if (response.error) {
      throw new Error('Failed to delete book')
    }
    return response.data
  },
  onSuccess: async () => {
    await queryClient.invalidateQueries({ queryKey: ['books'] })
    isOpen.value = false
  },
  onError: (error) => {
    console.error('Error deleting book:', error)
    deleteError.value = 'Failed to delete book. Please try again.'
  },
})

const confirmDelete = () => {
  deleteError.value = ''
  deleteBook.mutate(props.bookId)
}
</script>

<template>
  <Dialog v-model:open="isOpen">
    <DialogTrigger asChild>
      <Button variant="destructive" size="sm">
        <TrashIcon />
      </Button>
    </DialogTrigger>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogDescription>
          Are you sure you want to delete
          <span class="font-semibold">{{ bookTitle || `book #${bookId}` }}</span
          >? This action cannot be undone.
        </DialogDescription>
      </DialogHeader>

      <div v-if="deleteError" class="bg-red-50 text-red-500 p-2 rounded mb-4">
        {{ deleteError }}
      </div>

      <DialogFooter>
        <div class="flex justify-end gap-3">
          <Button variant="outline" @click="isOpen = false"> Cancel </Button>
          <Button
            variant="destructive"
            @click="confirmDelete"
            :disabled="deleteBook.isPending.value"
          >
            {{ deleteBook.isPending.value ? 'Deleting...' : 'Delete' }}
          </Button>
        </div>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
