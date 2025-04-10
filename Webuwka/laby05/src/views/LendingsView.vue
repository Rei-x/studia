<script setup lang="ts">
import { useLendings } from '@/api/use-lendings'
import { ref, computed } from 'vue'
import LendBook from '@/components/LendBook.vue'
import { Button } from '@/components/ui/button'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'

const lendings = useLendings()

const formatDate = (dateString?: string) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

const itemsPerPage = 5
const currentPage = ref(1)

const activeLendings = computed(() => {
  return lendings.data.value?.filter((lending) => !lending.returnDate) || []
})

const historyLendings = computed(() => {
  return lendings.data.value?.filter((lending) => !!lending.returnDate) || []
})

const showActive = ref(true)

const displayedLendings = computed(() => {
  const filteredList = showActive.value ? activeLendings.value : historyLendings.value
  const startIndex = (currentPage.value - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  return filteredList.slice(startIndex, endIndex)
})

const totalFilteredItems = computed(() => {
  return showActive.value ? activeLendings.value.length : historyLendings.value.length
})

const switchTab = (isActive: boolean) => {
  showActive.value = isActive
  currentPage.value = 1
}
</script>

<template>
  <div class="max-w-5xl mx-auto">
    <h1 class="text-3xl font-bold text-gray-800 mb-6">Book Lendings</h1>

    <div class="mb-6 flex space-x-2 border-b border-gray-200">
      <button
        @click="switchTab(true)"
        :class="[
          'py-2 px-4 font-medium',
          showActive
            ? 'text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-500 hover:text-gray-700',
        ]"
      >
        Active Lendings
      </button>
      <button
        @click="switchTab(false)"
        :class="[
          'py-2 px-4 font-medium',
          !showActive
            ? 'text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-500 hover:text-gray-700',
        ]"
      >
        Lending History
      </button>
    </div>

    <div v-if="lendings.isLoading.value" class="flex justify-center py-10">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
    </div>

    <div
      v-if="lendings.isError.value"
      class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative"
      role="alert"
    >
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline"> Unable to load lendings. Please try again later.</span>
    </div>

    <div v-else-if="totalFilteredItems === 0" class="text-center py-10 text-gray-500">
      No {{ showActive ? 'active' : 'historical' }} lendings available.
    </div>

    <div v-else class="overflow-x-auto shadow-md rounded-lg">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-100">
          <tr>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Book
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Reader
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Borrow Date
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              Return Date
            </th>
            <th
              scope="col"
              class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider"
              v-if="showActive"
            >
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="lending in displayedLendings" :key="lending.id" class="hover:bg-gray-50">
            <td class="px-6 py-4">
              <div class="text-sm font-medium text-gray-900">{{ lending.book?.title }}</div>
              <div class="text-xs text-gray-500">by {{ lending.book?.author?.fullName }}</div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-gray-900">{{ lending.readerName }}</div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-gray-900">{{ formatDate(lending.lendDate) }}</div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-gray-900">
                {{ lending.returnDate ? formatDate(lending.returnDate) : 'Not returned' }}
              </div>
            </td>
            <td class="px-6 py-4 text-center" v-if="showActive">
              <div class="flex justify-center">
                <LendBook
                  :bookId="lending.book?.id ?? 0"
                  :bookTitle="lending.book?.title"
                  :lendingId="lending.id"
                />
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div class="py-4 flex justify-center" v-if="totalFilteredItems > itemsPerPage">
        <Pagination
          v-slot="{ page }"
          v-model:page="currentPage"
          :items-per-page="itemsPerPage"
          :total="totalFilteredItems"
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
