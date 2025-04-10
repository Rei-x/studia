<script setup lang="ts">
import { fetchClient } from '@/api/client'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { ref, watch } from 'vue'
import { toast } from 'vue-sonner'
import * as z from 'zod'

const props = defineProps({
  bookId: { type: Number, default: undefined },
  bookTitle: { type: String, default: '' },
  bookAuthorId: { type: Number, default: undefined },
  bookPages: { type: Number, default: undefined },
  isEdit: { type: Boolean, default: false },
})

const isDialogOpen = ref(false)
const formError = ref('')
const mode = ref(props.isEdit ? 'edit' : 'add')

const formSchema = toTypedSchema(
  z.object({
    title: z.string().min(1, 'Title is required'),
    authorId: z.number({ required_error: 'Please select an author' }),
    pages: z.number().min(1, 'Number of pages must be at least 1'),
  }),
)

console.log('running!!', props.bookTitle)
const form = useForm({
  validationSchema: formSchema,
  initialValues: {
    title: props.bookTitle || '',
    authorId: props.bookAuthorId,
    pages: props.bookPages,
  },
})

watch(
  () => props.bookId,
  () => {
    console.log('setting values')
    if (props.isEdit && props.bookId) {
      form.setValues({
        title: props.bookTitle || '',
        authorId: props.bookAuthorId,
        pages: props.bookPages,
      })
      mode.value = 'edit'
    } else {
      mode.value = 'add'
    }
  },
)

const resetForm = () => {
  form.resetForm()
  formError.value = ''
  if (!props.isEdit) {
    form.setValues({
      title: '',
      authorId: undefined,
      pages: undefined,
    })
  }
}

const closeDialog = () => {
  isDialogOpen.value = false
  resetForm()
}

const authors = useQuery({
  queryKey: ['authors'],
  queryFn: async () => {
    const response = await fetchClient.GET('/api/v1/authors')
    if (response.error) {
      throw new Error('Network response was not ok')
    }
    return response.data
  },
})

const queryClient = useQueryClient()

const createBook = useMutation({
  mutationFn: async (book: { title: string; authorId: number; pages: number }) => {
    const response = await fetchClient.POST('/api/v1/books', {
      body: book,
    })
    if (response.error) {
      throw new Error('Network response was not ok')
    }
    return response.data
  },
  onSuccess: async () => {
    await queryClient.invalidateQueries({ queryKey: ['books'] })
    toast('Success', {
      description: 'Book created successfully',
    })
    isDialogOpen.value = false
    resetForm()
  },
  onError: (error) => {
    console.error('Error creating book:', error)
    formError.value = 'Failed to create book. Please try again.'
  },
})

const updateBook = useMutation({
  mutationFn: async (book: { id: number; title: string; authorId: number; pages: number }) => {
    const response = await fetchClient.PUT(`/api/v1/books/{id}`, {
      params: {
        path: {
          id: book.id,
        },
      },
      body: { title: book.title, authorId: book.authorId, pages: book.pages },
    })
    if (response.error) {
      throw new Error('Network response was not ok')
    }
    return response.data
  },
  onSuccess: async () => {
    await queryClient.invalidateQueries({ queryKey: ['books'] })
    toast('Success', {
      description: 'Book updated successfully',
    })
    isDialogOpen.value = false
    resetForm()
  },
  onError: (error) => {
    console.error('Error updating book:', error)
    formError.value = 'Failed to update book. Please try again.'
  },
})

const onSubmit = form.handleSubmit(
  (values) => {
    formError.value = ''
    if (mode.value === 'edit' && props.bookId) {
      updateBook.mutate({
        id: props.bookId,
        title: values.title,
        authorId: values.authorId,
        pages: values.pages,
      })
    } else {
      createBook.mutate({
        title: values.title,
        authorId: values.authorId,
        pages: values.pages,
      })
    }
  },
  (err) => {
    console.error('Form submission error:', err)
    formError.value = 'Please fill in all required fields correctly.'
  },
)
</script>

<template>
  <div class="my-5">
    <Dialog v-model:open="isDialogOpen">
      <DialogTrigger asChild>
        <Button v-if="!isEdit">Add New Book</Button>
        <Button v-else variant="outline" size="sm" class="h-8 px-2 lg:px-3"> Edit </Button>
      </DialogTrigger>
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{{ mode === 'edit' ? 'Edit Book' : 'Add New Book' }}</DialogTitle>
          <DialogDescription>
            {{
              mode === 'edit'
                ? 'Update the details of this book.'
                : 'Fill in the details to add a new book to your collection.'
            }}
          </DialogDescription>
        </DialogHeader>

        <div v-if="formError" class="bg-red-50 text-red-500 p-2 rounded mb-4">
          {{ formError }}
        </div>
        <form id="addBookForm" @submit="onSubmit">
          <FormField v-slot="{ componentField }" name="title">
            <FormItem class="mb-4">
              <FormLabel>Title</FormLabel>
              <FormControl>
                <Input type="text" placeholder="Enter book title" v-bind="componentField" />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="authorId">
            <FormItem class="mb-4">
              <FormLabel>Author</FormLabel>
              <Select v-bind="componentField">
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select an author" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectGroup>
                    <div v-if="authors.isLoading.value" class="p-2 text-gray-600">
                      Loading authors...
                    </div>
                    <SelectItem
                      v-for="author in authors.data?.value"
                      :key="author.id"
                      :value="author.id ?? 0"
                    >
                      {{ author.firstName }} {{ author.lastName }}
                    </SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          </FormField>

          <FormField v-slot="{ componentField }" name="pages">
            <FormItem class="mb-4">
              <FormLabel>Number of Pages</FormLabel>
              <FormControl>
                <Input
                  type="number"
                  min="1"
                  placeholder="Enter number of pages"
                  v-bind="componentField"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          </FormField>
        </form>

        <DialogFooter>
          <Button type="button" variant="secondary" @click="closeDialog"> Cancel </Button>
          <Button
            type="submit"
            form="addBookForm"
            :disabled="createBook.isPending.value || updateBook.isPending.value"
          >
            {{
              createBook.isPending.value || updateBook.isPending.value
                ? 'Saving...'
                : mode === 'edit'
                  ? 'Update Book'
                  : 'Save Book'
            }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>
