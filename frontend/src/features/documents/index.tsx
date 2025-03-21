import { useState } from 'react'
import {
  IconAdjustmentsHorizontal,
  IconSortAscendingLetters,
  IconSortDescendingLetters,
  IconFileText,
  IconEye,
} from '@tabler/icons-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ProfileDropdown } from '@/components/profile-dropdown'
import { Search } from '@/components/search'
import { ThemeSwitch } from '@/components/theme-switch'
import { PDFViewerDialog } from '@/components/pdf-viewer-dialog'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

const DocumentCard = ({ document }: { document: any }) => {
  const [isViewerOpen, setIsViewerOpen] = useState(false)
  const handleView = async () => {
    try {
      // console.log('document', document)
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/knowledge/documents/download?document_name=${document.name}`,
        { responseType: 'blob' }
      )
      const url = URL.createObjectURL(response.data)
      // console.log('url', url)
      setDocumentUrl(url)
      setIsViewerOpen(true)
    } catch (error) {
      console.error('Error fetching document:', error)
    }
  }

  const [documentUrl, setDocumentUrl] = useState<string>('')

  return (
    <>
      <div className="rounded-lg border p-4 hover:shadow-md">
        <div className="mb-4 flex items-center justify-between">
          <div className="flex size-10 items-center justify-center rounded-lg bg-muted p-2">
            <IconFileText className="h-5 w-5" />
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={handleView}
            className="flex items-center gap-2"
          >
            <IconEye className="h-4 w-4" />
            View
          </Button>
        </div>
        <div>
          <h2 className="mb-1 font-semibold">{document.name}</h2>
          <p className="line-clamp-2 text-gray-500">{document.description || 'No description available'}</p>
        </div>
      </div>

      <PDFViewerDialog
        open={isViewerOpen}
        onOpenChange={setIsViewerOpen}
        documentUrl={documentUrl}
        title={document.name}
      />
    </>
  )
}

export default function Apps() {
  const [sort, setSort] = useState('ascending')
  const [searchTerm, setSearchTerm] = useState('')

  const fetchDocuments = async () => {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/knowledge/documents/user?user=aaaaaaaaaaaaaa`)
    return response.data
  }

  const { data: documents } = useQuery({
    queryKey: ['documents'],
    queryFn: () => fetchDocuments(),
  })

  // console.log(documents)


  return (
    <>
      {/* ===== Top Heading ===== */}
      <Header>
        <Search />
        <div className='ml-auto flex items-center gap-4'>
          <ThemeSwitch />
          <ProfileDropdown />
        </div>
      </Header>

      {/* ===== Content ===== */}
      <Main fixed>
        <div>
          <h1 className='text-2xl font-bold tracking-tight'>
            Documents
          </h1>
          <p className='text-muted-foreground'>
            Here&apos;s a list of your documents!
          </p>
        </div>
        <div className='my-4 flex items-end justify-between sm:my-0 sm:items-center'>
          <div className='flex flex-col gap-4 sm:my-4 sm:flex-row'>
            <Input
              placeholder='Filter apps...'
              className='h-9 w-40 lg:w-[250px]'
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />

          </div>

          <Select value={sort} onValueChange={setSort}>
            <SelectTrigger className='w-16'>
              <SelectValue>
                <IconAdjustmentsHorizontal size={18} />
              </SelectValue>
            </SelectTrigger>
            <SelectContent align='end'>
              <SelectItem value='ascending'>
                <div className='flex items-center gap-4'>
                  <IconSortAscendingLetters size={16} />
                  <span>Ascending</span>
                </div>
              </SelectItem>
              <SelectItem value='descending'>
                <div className='flex items-center gap-4'>
                  <IconSortDescendingLetters size={16} />
                  <span>Descending</span>
                </div>
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
        <Separator className='shadow' />
        <ul className='faded-bottom no-scrollbar grid gap-4 overflow-auto pb-16 pt-4 md:grid-cols-2 lg:grid-cols-3'>
          {documents?.user?.map((app: any,index: number) => (
            <DocumentCard key={index} document={app} />
          ))}
        </ul>
      </Main>
    </>
  )
}
