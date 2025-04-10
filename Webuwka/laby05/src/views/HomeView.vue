<script setup lang="ts">
// Book and Author DTOs
interface AuthorDTO {
  id: number
  firstName: string
  lastName: string
  biography: string
  fullName: string
}

interface BookDTO {
  id: number
  title: string
  author: AuthorDTO
  pages: number
  available: boolean
}

// Lending DTO
interface LendingDTO {
  id: number
  book: BookDTO
  readerName: string
  lendDate: string // ISO date-time string
  returnDate: string // ISO date-time string
}

// Sample book data conforming to BookDTO
const featuredBooks: BookDTO[] = [
  {
    id: 1,
    title: 'The Great Gatsby',
    author: {
      id: 1,
      firstName: 'F. Scott',
      lastName: 'Fitzgerald',
      biography: 'American novelist and short story writer.',
      fullName: 'F. Scott Fitzgerald',
    },
    pages: 180,
    available: true,
  },
  {
    id: 2,
    title: 'To Kill a Mockingbird',
    author: {
      id: 2,
      firstName: 'Harper',
      lastName: 'Lee',
      biography: "American novelist widely known for her novel 'To Kill a Mockingbird'.",
      fullName: 'Harper Lee',
    },
    pages: 281,
    available: true,
  },
  {
    id: 3,
    title: '1984',
    author: {
      id: 3,
      firstName: 'George',
      lastName: 'Orwell',
      biography: 'English novelist, essayist, journalist and critic.',
      fullName: 'George Orwell',
    },
    pages: 328,
    available: false,
  },
  {
    id: 4,
    title: 'The Hobbit',
    author: {
      id: 4,
      firstName: 'J.R.R.',
      lastName: 'Tolkien',
      biography: 'English writer, poet, philologist, and academic.',
      fullName: 'J.R.R. Tolkien',
    },
    pages: 310,
    available: true,
  },
]

// Sample lending data (if needed)
const recentLendings: LendingDTO[] = [
  {
    id: 1,
    book: featuredBooks[2], // 1984
    readerName: 'Alice Johnson',
    lendDate: '2023-10-15T10:30:00Z',
    returnDate: '2023-11-15T10:30:00Z',
  },
]
</script>

<template>
  <main class="min-h-screen bg-gray-50">
    
  </main>
</template>
