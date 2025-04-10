import { fetchClient } from '@/api/client'
import { useQuery } from '@tanstack/vue-query'

export const useLendings = () => {
  return useQuery({
    queryKey: ['lendings'],
    queryFn: async () => {
      const response = await fetchClient.GET('/api/v1/lendings')
      if (response.error) {
        throw new Error('Failed to fetch lending information')
      }
      return response.data ?? []
    },
    select: (data) => {
      return [...data].sort((a, b) => {
        if (!a.lendDate || !b.lendDate) {
          return 0
        }

        if (a.returnDate && b.returnDate) {
          const dateA = new Date(a.returnDate)
          const dateB = new Date(b.returnDate)

          return dateB.getTime() - dateA.getTime()
        }

        if (a.returnDate && !b.returnDate) {
          return 1
        }

        if (!a.returnDate && b.returnDate) {
          return -1
        }

        const dateA = new Date(a.lendDate)
        const dateB = new Date(b.lendDate)
        return dateB.getTime() - dateA.getTime()
      })
    },
  })
}
