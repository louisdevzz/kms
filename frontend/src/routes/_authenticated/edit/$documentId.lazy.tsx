import { createLazyFileRoute } from '@tanstack/react-router'
import Edit from '@/features/edit'
import { useParams } from '@tanstack/react-router'


export const Route = createLazyFileRoute('/_authenticated/edit/$documentId')({
  component: EditRoute
})

export default function EditRoute() {
  const { documentId } = useParams({ from: '/_authenticated/edit/$documentId' })
  return <Edit documentId={documentId} />
}