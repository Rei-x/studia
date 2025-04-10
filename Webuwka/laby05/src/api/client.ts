import type { paths } from '@/lib/api'
import createFetchClient from 'openapi-fetch'

export const fetchClient = createFetchClient<paths>({
  baseUrl: 'https://java-webowka-znowu.sharkserver.kowalinski.dev',
})
