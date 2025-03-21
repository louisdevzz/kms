import { createLazyFileRoute } from '@tanstack/react-router'
import Documents from '@/features/documents'

export const Route = createLazyFileRoute('/_authenticated/documents/')({
  component: Documents,
})
