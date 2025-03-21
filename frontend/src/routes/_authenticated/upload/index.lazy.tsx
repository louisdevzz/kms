import { createLazyFileRoute } from '@tanstack/react-router'
import Upload from '@/features/upload'

export const Route = createLazyFileRoute('/_authenticated/upload/')({
  component: Upload,
})
