<script setup lang="ts">
import { fetchClient } from '@/api/client'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { ref } from 'vue'
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
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { BookDownIcon, BookUpIcon } from 'lucide-vue-next'

const props = defineProps<{
  lendingId?: number
  bookId: number
  bookTitle?: string
}>()

const isOpen = ref(false)
const readerName = ref('')
const errorMessage = ref('')

const queryClient = useQueryClient()

const lendBook = useMutation({
  mutationFn: async (opts: { bookId: number; readerName: string }) => {
    const response = await fetchClient.POST(`/api/v1/lendings/lend`, {
      body: opts,
    })
    if (response.error) {
      throw new Error('Failed to lend book')
    }
    return response.data
  },
  onSuccess: async () => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ['books'] }),
      queryClient.invalidateQueries({ queryKey: ['lendings'] }),
    ])
    isOpen.value = false
    readerName.value = ''
    errorMessage.value = ''
  },
  onError: (error) => {
    console.error('Error lending book:', error)
    errorMessage.value = 'Failed to lend book. Please try again.'
  },
})

const returnBook = useMutation({
  mutationFn: async (opts: { lendingId: number }) => {
    const response = await fetchClient.POST(`/api/v1/lendings/return/{lendingId}`, {
      params: {
        path: opts,
      },
    })
    if (response.error) {
      throw new Error('Failed to return book')
    }
    return response.data
  },
  onSuccess: async () => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ['books'] }),
      queryClient.invalidateQueries({ queryKey: ['lendings'] }),
    ])
    isOpen.value = false
    errorMessage.value = ''
  },
  onError: (error) => {
    console.error('Error returning book:', error)
    errorMessage.value = 'Failed to return book. Please try again.'
  },
})

const handleLendBook = () => {
  if (!readerName.value.trim()) {
    errorMessage.value = 'Reader name is required'
    return
  }

  lendBook.mutate({
    bookId: props.bookId,
    readerName: readerName.value,
  })
}

const handleReturnBook = () => {
  if (!props.lendingId) {
    errorMessage.value = 'Lending ID is missing'
    return
  }

  returnBook.mutate({
    lendingId: props.lendingId,
  })
}
</script>

<template>
  <Dialog v-model:open="isOpen">
    <DialogTrigger asChild>
      <Button :variant="lendingId ? 'outline' : 'default'" size="sm">
        <BookDownIcon v-if="!lendingId" class="mr-1 h-4 w-4" />
        <BookUpIcon v-else class="mr-1 h-4 w-4" />
        {{ lendingId ? 'Return' : 'Lend' }}
      </Button>
    </DialogTrigger>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>{{ lendingId ? 'Return Book' : 'Lend Book' }}</DialogTitle>
        <DialogDescription>
          {{
            lendingId
              ? `Confirm returning "${bookTitle || `book #${bookId}`}".`
              : `Enter reader details to lend "${bookTitle || `book #${bookId}`}".`
          }}
        </DialogDescription>
      </DialogHeader>

      <form @submit.prevent="lendingId ? handleReturnBook() : handleLendBook()">
        <div v-if="!lendingId" class="grid gap-4 py-4">
          <div class="grid gap-2">
            <Label for="readerName">Reader Name</Label>
            <Input id="readerName" v-model="readerName" placeholder="Enter reader name" required />
          </div>
        </div>

        <div v-if="errorMessage" class="bg-red-50 text-red-500 p-2 rounded mb-4">
          {{ errorMessage }}
        </div>

        <DialogFooter>
          <div class="flex justify-end gap-3">
            <Button type="button" variant="outline" @click="isOpen = false">Cancel</Button>
            <Button
              type="submit"
              :disabled="lendingId ? returnBook.isPending.value : lendBook.isPending.value"
            >
              {{
                lendingId
                  ? returnBook.isPending.value
                    ? 'Returning...'
                    : 'Return'
                  : lendBook.isPending.value
                    ? 'Lending...'
                    : 'Lend'
              }}
            </Button>
          </div>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
