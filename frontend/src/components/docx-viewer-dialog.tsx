import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { useEffect, useState } from 'react'

interface DocxViewerDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  documentUrl: string
  title?: string
}

export function DocxViewerDialog({
  open,
  onOpenChange,
  documentUrl,
  title = 'Document Viewer',
}: DocxViewerDialogProps) {
  const [docxUrl, setDocxUrl] = useState<string>('')
  
  useEffect(() => {
    if (documentUrl) {
      setDocxUrl(documentUrl)
    }
    
    // Cleanup function to revoke object URL when component unmounts
    return () => {
      if (docxUrl && docxUrl.startsWith('blob:')) {
        URL.revokeObjectURL(docxUrl)
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
          {docxUrl ? (
            <iframe
              src={`https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(docxUrl)}`}
              className="w-full h-full border-0"
              title={title}
            />
          ) : (
            <div className="flex items-center justify-center h-full">
              <p>Loading Word document...</p>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
} 