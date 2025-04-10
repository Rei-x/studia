<script setup lang="ts">
import { fetchClient } from '@/api/client'
import AddOrEditBook from '@/components/AddOrEditBook.vue'
import DeleteBook from '@/components/DeleteBook.vue'
import LendBook from '@/components/LendBook.vue'
import { useQuery } from '@tanstack/vue-query'
import { computed, ref } from 'vue'

import { Button } from '@/components/ui/button'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'

import {
  Pagination,
  PaginationEllipsis,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'
import PaginationContent from '@/components/ui/pagination/PaginationContent.vue'
import { useLendings } from '@/api/use-lendings'

const books = useQuery({
  queryKey: ['books'],
  queryFn: async () => {
    const response = await fetchClient.GET('/api/v1/books')
    if (response.error) {
      throw new Error('Network response was not ok')
    }
    return response.data ?? []
  },
})

const lendings = useLendings()

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

// Combine books with lending information
const booksWithLendingInfo = computed(() => {
  if (!books.data.value) return []

  return books.data.value.map((book) => {
    // Find corresponding lending if the book is borrowed
    const lending = lendings.data.value?.find((l) => l.book?.id === book.id && !l.returnDate)

    return {
      ...book,
      borrower: lending?.readerName || null,
      lendingId: lending?.id || null,
      lendDate: lending?.lendDate || null,
    }
  })
})

// Pagination
const itemsPerPage = 5
const currentPage = ref(1)

const paginatedBooks = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  return booksWithLendingInfo.value.slice(startIndex, endIndex)
})

const totalBooks = computed(() => {
  return booksWithLendingInfo.value.length || 0
})
</script>

<template>
  <div class="max-w-5xl mx-auto">
    <h1 class="text-3xl font-bold text-gray-800 mb-6">Book Collection</h1>
    <AddOrEditBook />

    <div v-if="books.isLoading.value" class="flex justify-center py-10">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
    </div>

    <div
      v-if="books.isError.value"
      class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative"
      role="alert"
    >
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline"> Unable to load books. Please try again later.</span>
    </div>

    <div
      v-else-if="books.data.value && books.data.value.length === 0"
      class="text-center py-10 text-gray-500"
    >
      No books available.
    </div>

    <div v-else-if="books.data.value" class="overflow-x-auto shadow-md rounded-lg">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-100">
          <tr>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Title
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Author
            </th>
            <th
              scope="col"
              class="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Pages
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Status
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Borrower
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider text-center"
            >
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="book in paginatedBooks" :key="book.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ book.title }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ book.author?.fullName }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ book.pages }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <span
                      :class="[
                        'px-2 inline-flex text-xs leading-5 font-semibold rounded-full',
                        book.available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800',
                      ]"
                    >
                      {{ book.available ? 'Available' : 'Borrowed' }}
                    </span>
                  </TooltipTrigger>
                  <TooltipContent v-if="!book.available && book.lendDate">
                    <p>Borrowed on: {{ formatDate(book.lendDate) }}</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">
                {{ book.borrower || '-' }}
              </div>
            </td>
            <td
              class="px-6 whitespace-nowrap text-right text-sm flex justify-center items-center gap-2"
            >
              <AddOrEditBook
                :bookId="book.id"
                :bookTitle="book.title"
                :bookAuthorId="book.author?.id"
                :bookPages="book.pages"
                :isEdit="true"
              />
              <DeleteBook :bookId="book.id ?? 0" :bookTitle="book.title" />
              <LendBook
                :bookId="book.id ?? 0"
                :bookTitle="book.title"
                :lendingId="book.lendingId ?? undefined"
              />
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div class="py-4 flex justify-center">
        <Pagination
          v-slot="{ page }"
          v-model:page="currentPage"
          :items-per-page="itemsPerPage"
          :total="totalBooks"
          :sibling-count="1"
          show-edges
        >
          <PaginationContent v-slot="{ items }" class="flex items-center gap-1">
            <PaginationPrevious />

            <template v-for="(item, index) in items">
              <PaginationItem v-if="item.type === 'page'" :key="index" :value="item.value" as-child>
                <Button class="w-9 h-9 p-0" :variant="item.value === page ? 'default' : 'outline'">
                  {{ item.value }}
                </Button>
              </PaginationItem>
              <PaginationEllipsis v-else :key="item.type" :index="index" />
            </template>

            <PaginationNext />
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  </div>
</template>
