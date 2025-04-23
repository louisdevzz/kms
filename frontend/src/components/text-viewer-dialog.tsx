import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { useEffect, useState } from 'react'
import { ScrollArea } from '@/components/ui/scroll-area'

interface TextViewerDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  documentUrl: string
  title?: string
}

export function TextViewerDialog({
  open,
  onOpenChange,
  documentUrl,
  title = 'Text Viewer',
}: TextViewerDialogProps) {
  const [textContent, setTextContent] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  
  useEffect(() => {
    if (documentUrl && open) {
      setIsLoading(true)
      fetch(documentUrl)
        .then(response => response.text())
        .then(text => {
          setTextContent(text)
          setIsLoading(false)
        })
        .catch(error => {
          console.error('Error loading text:', error)
          setIsLoading(false)
        })
    }
    
    return () => {
      // Cleanup if needed
    }
  }, [documentUrl, open])
  
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-5xl h-[80vh] flex flex-col p-0">
        <DialogHeader className="px-6 py-2 flex-none">
          <div className="flex items-center justify-between">
            <DialogTitle>{title}</DialogTitle>
          </div>
        </DialogHeader>
        <div className="flex-1 overflow-hidden p-6">
          {isLoading ? (
            <div className="flex items-center justify-center h-full">
              <p>Loading text...</p>
            </div>
          ) : (
            <ScrollArea className="h-full p-6 border border-gray-300 rounded-lg">
              <pre className="whitespace-pre-wrap font-mono text-sm">{textContent}</pre>
            </ScrollArea>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
} 