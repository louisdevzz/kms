import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { useEffect, useState } from 'react'

interface ImageViewerDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  documentUrl: string
  title?: string
}

export function ImageViewerDialog({
  open,
  onOpenChange,
  documentUrl,
  title = 'Image Viewer',
}: ImageViewerDialogProps) {
  const [imageUrl, setImageUrl] = useState<string>('')
  
  useEffect(() => {
    if (documentUrl) {
      setImageUrl(documentUrl)
    }
    
    // Cleanup function to revoke object URL when component unmounts
    return () => {
      if (imageUrl && imageUrl.startsWith('blob:')) {
        URL.revokeObjectURL(imageUrl)
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
        <div className="flex-1 overflow-auto flex items-center justify-center p-4">
          {imageUrl ? (
            <img 
              src={imageUrl} 
              alt={title || "Image preview"} 
              className="max-w-full max-h-full object-contain"
            />
          ) : (
            <div className="flex items-center justify-center h-full">
              <p>Loading image...</p>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
} 