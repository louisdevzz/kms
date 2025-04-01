import { IconFileText, IconDownload, IconTrash } from '@tabler/icons-react'
import { Button } from '@/components/ui/button'

interface UserUpload {
  fileName: string
  fileSize: string
  uploadTime: string
  fileType: string
  downloads: number
}

const recentUploads: UserUpload[] = [
  {
    fileName: "Project_Report.pdf",
    fileSize: "2.4 MB",
    uploadTime: "2 minutes ago",
    fileType: "PDF",
    downloads: 12
  },
  {
    fileName: "Research_Data.xlsx",
    fileSize: "1.8 MB",
    uploadTime: "45 minutes ago",
    fileType: "Excel",
    downloads: 5
  },
  {
    fileName: "Presentation.pptx",
    fileSize: "5.1 MB",
    uploadTime: "2 hours ago",
    fileType: "PowerPoint",
    downloads: 8
  },
  {
    fileName: "Notes.docx",
    fileSize: "1.2 MB",
    uploadTime: "1 day ago",
    fileType: "Word",
    downloads: 3
  }
]

export function RecentUploads() {
  return (
    <div className="space-y-4">
      {recentUploads.map((upload, index) => (
        <div key={index} className="flex items-center justify-between rounded-lg border p-3 hover:bg-accent/50 transition-colors">
          <div className="flex items-center space-x-3">
            <IconFileText className="h-8 w-8 text-muted-foreground" />
            <div>
              <p className="text-sm font-medium">{upload.fileName}</p>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <span>{upload.fileType}</span>
                <span>•</span>
                <span>{upload.fileSize}</span>
                <span>•</span>
                <span>{upload.uploadTime}</span>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" className="hover:bg-background">
              <IconDownload className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="text-destructive hover:bg-background">
              <IconTrash className="h-4 w-4" />
            </Button>
          </div>
        </div>
      ))}
    </div>
  )
} 