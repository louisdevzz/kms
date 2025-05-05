import { useEffect, useState } from 'react'
import {
  IconAdjustmentsHorizontal,
  IconSortAscendingLetters,
  IconSortDescendingLetters,
  IconFileText,
  IconEye,
  IconShare,
  IconEdit,
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
import { TextViewerDialog } from '@/components/text-viewer-dialog'
import { ImageViewerDialog } from '@/components/image-viewer-dialog'
import { ExcelViewerDialog } from '@/components/excel-viewer-dialog'
import { DocxViewerDialog } from '@/components/docx-viewer-dialog'
import { useQuery } from '@tanstack/react-query'
import { fetchDocuments, fetchDocumentMetadata, fetchDocumentContent, searchDocuments, shareDocument } from '@/lib/api'
import { useNavigate } from '@tanstack/react-router'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogClose } from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { useState as useDialogState } from 'react'

interface DocumentCardProps{
  documentId: string;
}

const DocumentCard = ({ documentId }: DocumentCardProps) => {
  const [isViewerOpen, setIsViewerOpen] = useState(false)
  const [documentUrl, setDocumentUrl] = useState<string>('')
  const navigate = useNavigate()
  const [isShareDialogOpen, setIsShareDialogOpen] = useState(false)
  const [shareEmail, setShareEmail] = useState('')
  const [isSharing, setIsSharing] = useState(false)
  const [permission, setPermission] = useState('read')

  const { data: metadataDoc, isLoading: isLoadingMetadata } = useQuery({
    queryKey: ['metadataDoc', documentId],
    queryFn: () => fetchDocumentMetadata(documentId)
  })

  // console.log('metadataDoc', metadataDoc)

  const { data: document, isLoading: isLoadingDocument } = useQuery({
    queryKey: ['document', documentId],
    queryFn: () => fetchDocumentContent(documentId)
  })

  const getDataUrl = () => {
    try {
      if (!document) {
        return '';
      }

      if (document instanceof ArrayBuffer) {
        let mimeType = 'application/pdf';
        const type = metadataDoc?.dType || 'pdf';
        
        // If the type is already a MIME type, use it directly
        if (type.includes('/')) {
          mimeType = type;
        } else {
          // Otherwise, map simplified type to MIME type
          switch (type) {
            case 'pdf':
              mimeType = 'application/pdf';
              break;
            case 'text':
              mimeType = 'text/plain';
              break;
            case 'image':
              mimeType = 'image/jpeg'; // Default image type
              break;
            case 'excel':
              mimeType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
              break;
            case 'docx':
              mimeType = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
              break;
            default:
              mimeType = 'application/pdf';
          }
        }
        
        const blob = new Blob([document], { type: mimeType });
        return URL.createObjectURL(blob);
      }

      return '';
    } catch (error) {
      console.error('Error processing document data:', error);
      return '';
    }
  }

  useEffect(() => {
    if (document) {
      const url = getDataUrl();
      setDocumentUrl(url);
    }
    
    return () => {
      if (documentUrl && documentUrl.startsWith('blob:')) {
        URL.revokeObjectURL(documentUrl);
      }
    };
  }, [document]);

  const handleView = () => {
    setIsViewerOpen(true)
  }

  const handleShare = async () => {
    if (!shareEmail) return
    
    setIsSharing(true)
    try {
      // Call the actual API function to share the document
      await shareDocument(documentId, shareEmail, permission)
      
      alert(`Document shared with ${shareEmail} with ${permission} permission`)
      setIsShareDialogOpen(false)
      setShareEmail('')
      setPermission('read')
    } catch (error) {
      console.error('Error sharing document:', error)
      alert('Failed to share document. Please try again.')
    } finally {
      setIsSharing(false)
    }
  }

  const handleShareClick = () => {
    setIsShareDialogOpen(true)
  }

  if (isLoadingMetadata || isLoadingDocument) {
    return (
      <div className="rounded-lg border p-4">
        <div className="animate-pulse">
          <div className="h-10 w-10 rounded-lg bg-muted mb-4" />
          <div className="h-4 w-3/4 bg-muted rounded mb-2" />
          <div className="h-4 w-1/2 bg-muted rounded" />
        </div>
      </div>
    )
  }

  const renderDocumentViewer = () => {
    const documentType = metadataDoc?.dType || 'pdf';
    // console.log('documentType', documentType)
    
    if (documentType === 'pdf' || documentType === 'application/pdf') {
      return (
        <PDFViewerDialog
          open={isViewerOpen}
          onOpenChange={setIsViewerOpen}
          documentUrl={documentUrl}
          title={metadataDoc?.name}
        />
      );
    } else if (documentType === 'text' || documentType === 'text/plain') {
      return (
        <TextViewerDialog
          open={isViewerOpen}
          onOpenChange={setIsViewerOpen}
          documentUrl={documentUrl}
          title={metadataDoc?.name}
        />
      );
    } else if (documentType === 'image' || documentType.startsWith('image/')) {
      return (
        <ImageViewerDialog
          open={isViewerOpen}
          onOpenChange={setIsViewerOpen}
          documentUrl={documentUrl}
          title={metadataDoc?.name}
        />
      );
    } else if (documentType === 'excel' || 
              documentType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' || 
              documentType === 'application/vnd.ms-excel') {
      return (
        <ExcelViewerDialog
          open={isViewerOpen}
          onOpenChange={setIsViewerOpen}
          documentUrl={documentUrl}
          title={metadataDoc?.name}
        />
      );
    } else if (documentType === 'docx' || 
              documentType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
              documentType === 'application/msword') {
      return (
        <DocxViewerDialog
          open={isViewerOpen}
          onOpenChange={setIsViewerOpen}
          documentUrl={documentUrl}
          title={metadataDoc?.name}
        />
      );
    } else {
      // Default to PDF viewer
      return (
        <PDFViewerDialog
          open={isViewerOpen}
          onOpenChange={setIsViewerOpen}
          documentUrl={documentUrl}
          title={metadataDoc?.name}
        />
      );
    }
  };

  return (
    <>
      <div className="rounded-lg border p-4 hover:shadow-md">
        <div className="mb-4 flex items-center justify-between">
          <div className="flex size-10 items-center justify-center rounded-lg bg-muted p-2">
            <IconFileText className="h-5 w-5" />
          </div>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleView}
              className="flex items-center gap-2"
            >
              <IconEye className="h-4 w-4" />
              View
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate({ to: `/edit/${documentId}` })}
              className="flex items-center gap-2"
            >
              <IconEdit className="h-4 w-4" />
              Edit
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleShareClick}
              className="flex items-center gap-2"
            >
              <IconShare className="h-4 w-4" />
              Share
            </Button>
          </div>
        </div>
        <div>
          <h2 className="mb-1 font-semibold">{metadataDoc?.name}</h2>
          <p className="line-clamp-2 text-gray-500">{metadataDoc?.description || 'No description available'}</p>
        </div>
      </div>

      {renderDocumentViewer()}
      
      <Dialog open={isShareDialogOpen} onOpenChange={setIsShareDialogOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Share Document</DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="email" className="text-right">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                value={shareEmail}
                onChange={(e) => setShareEmail(e.target.value)}
                placeholder="Enter recipient's email"
                className="col-span-3"
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="permission" className="text-right">
                Permission
              </Label>
              <div className="col-span-3">
                <Select value={permission} onValueChange={setPermission}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select permission" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="read">Read only</SelectItem>
                    <SelectItem value="edit">Can edit</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline">Cancel</Button>
            </DialogClose>
            <Button 
              onClick={handleShare} 
              disabled={!shareEmail || isSharing}
            >
              {isSharing ? 'Sharing...' : 'Share'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  )
}

export default function Documents() {
  const [sort, setSort] = useState('ascending')
  const [searchTerm, setSearchTerm] = useState('')
  const [filteredDocumentIds, setFilteredDocumentIds] = useState<string[]>([])

  const { data: documentIds, error, isLoading } = useQuery({
    queryKey: ['documentIds'],
    queryFn: () => fetchDocuments(true)
  })

  useEffect(() => {
    if (documentIds) {
      setFilteredDocumentIds(documentIds)
    }
  }, [documentIds])
  
  const handleSearch = async () => {
    if (!searchTerm.trim()) {
      // If search term is empty, reset to all documents
      setFilteredDocumentIds(documentIds || [])
      return
    }
    
    try {
      const searchResults = await searchDocuments(searchTerm)
      // Extract document IDs from search results
      const resultIds = searchResults.map((doc: any) => doc.id)
      setFilteredDocumentIds(resultIds)
    } catch (error) {
      console.error('Error searching documents:', error)
      // In case of error, keep the current list
    }
  }
  
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchTerm) {
        handleSearch()
      } else {
        setFilteredDocumentIds(documentIds || [])
      }
    }, 500)
    
    return () => clearTimeout(delayDebounceFn)
  }, [searchTerm, documentIds])

  if (error) {
    return (
      <>
        <Header>
          <Search />
          <div className='ml-auto flex items-center gap-4'>
            <ThemeSwitch />
            <ProfileDropdown />
          </div>
        </Header>
        <Main fixed>
          <div className="flex flex-col items-center justify-center h-[50vh]">
            <h1 className="text-2xl font-bold text-red-500 mb-2">Error</h1>
            <p className="text-muted-foreground">Unable to fetch documents. Please try again later.</p>
          </div>
        </Main>
      </>
    )
  }

  // console.log('documentIds',documentIds)



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
              placeholder='Filter documents...'
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
        {isLoading ? (
          <div className="py-8 text-center">
            <p className="text-muted-foreground">Loading documents...</p>
          </div>
        ) : filteredDocumentIds.length === 0 ? (
          <div className="py-8 text-center">
            <p className="text-muted-foreground">No documents found. Try a different search term.</p>
          </div>
        ) : (
          <ul className='faded-bottom no-scrollbar grid gap-4 overflow-auto pb-16 pt-4 md:grid-cols-2 lg:grid-cols-3'>
            {filteredDocumentIds.map((documentId: string) => (
              <DocumentCard
                key={documentId}
                documentId={documentId}
              />
            ))}
          </ul>
        )}
      </Main>
    </>
  )
}
