import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { useEffect, useState } from 'react'

interface PDFViewerDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  documentUrl: string
  title?: string
}

export function PDFViewerDialog({
  open,
  onOpenChange,
  documentUrl,
  title = 'Document Viewer',
}: PDFViewerDialogProps) {
  const [pdfUrl, setPdfUrl] = useState<string>('')
  
  useEffect(() => {
    if (documentUrl) {
      setPdfUrl(documentUrl)
    }
    
    // Cleanup function to revoke object URL when component unmounts
    return () => {
      if (pdfUrl && pdfUrl.startsWith('blob:')) {
        URL.revokeObjectURL(pdfUrl)
      }
    }
  }, [documentUrl])
  
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-5xl h-[80vh] flex flex-col p-0">
        <DialogHeader className="px-6 py-2 flex-none">
          <div className="flex items-center justify-between">
            <DialogTitle>{title}</DialogTitle>
          </div>
        </DialogHeader>
        <div className="flex-1 overflow-hidden">
          {pdfUrl ? (
            <iframe
              src={pdfUrl}
              className="w-full h-full border-0"
              title={title}
            />
          ) : (
            <div className="flex items-center justify-center h-full">
              <p>Loading PDF...</p>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
} 