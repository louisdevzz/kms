import { IconFileText, IconDownload, IconTrash } from '@tabler/icons-react'
import { Button } from '@/components/ui/button'
import axios from 'axios'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { toast } from '@/hooks/use-toast'
import {fetchDocumentMetadata,fetchDocumentContent } from "@/lib/api"


interface RecentUploadsProps {
  documentIds: string[]
}

interface RecentUploadCardProps {
  documentId: string;
}

const RecentUploadCard = ({documentId}: RecentUploadCardProps) =>{
  const queryClient = useQueryClient();

  const { data: metadataDoc, error } = useQuery({
    queryKey: ['metadataDoc', documentId],
    queryFn: () => fetchDocumentMetadata(documentId),
  })
  
  // console.log('metadataDoc:', metadataDoc);


  const downloadFile = async () => {
    if (!metadataDoc || !metadataDoc.versions || metadataDoc.versions.length === 0) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to download document',
        variant: 'destructive',
      })
      return;
    }

    try {
      const content = await fetchDocumentContent(documentId)

      const fileData = content

      if (!fileData) {
        return '';
      }

      const blob = new Blob([fileData], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);

      
      // Create a temporary link element
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${metadataDoc.name || 'document'}.pdf`); // Set filename
      
      // Append to body, click, and remove
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Clean up the URL
      window.URL.revokeObjectURL(url);
      
      toast({
        title: 'Success',
        description: 'Document download successfully',
      })
    } catch (error) {
      console.error('Error downloading file:', error);
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to download document',
        variant: 'destructive',
      })
    }
  };

  const removeFile = async () => {
    if (!metadataDoc) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'No document',
        variant: 'destructive',
      })
      return;
    }
    const baseUrl = 'https://kms-production-958c.up.railway.app'
    const apiUrl = `${baseUrl}/kms/document/${documentId}`
    try {
      await axios.delete(
        apiUrl,
        {
          headers: {
            "Authorization": `Bearer ${JSON.parse(localStorage.getItem('access_token') || '')}`,
          }
        }
      );
      
      // Invalidate the query to refresh the list
      queryClient.invalidateQueries({ queryKey: ['documents'] });
      
      toast({
        title: 'Success',
        description: 'Document remove successfully',
      })
    } catch (error) {
      console.error('Error removing document:', error);
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to remove document',
        variant: 'destructive',
      })
    }
  };

  if(error){
    console.error('error fetch', error)
  }

  return(
    <div className="flex items-center justify-between rounded-lg border p-3 hover:bg-accent/50 transition-colors">
      <div className="flex items-center space-x-3">
        <IconFileText className="h-8 w-8 text-muted-foreground" />
        <div>
          <p className="text-sm font-medium">{metadataDoc?.name}</p>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>{metadataDoc?.dType}</span>
            <span>•</span>
            <span>{metadataDoc?.versions && metadataDoc.versions.length > 0 ? metadataDoc.versions[0].file_size : 'N/A'} KB</span>
            <span>•</span>
            <span>{metadataDoc?.versions && metadataDoc.versions.length > 0 ? metadataDoc.versions[0].modification_date : 'N/A'}</span>
          </div>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Button 
          variant="ghost" 
          size="sm" 
          className="hover:bg-background"
          onClick={downloadFile}
          disabled={!metadataDoc || !metadataDoc.versions || metadataDoc.versions.length === 0}
        >
          <IconDownload className="h-4 w-4" />
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          className="text-destructive hover:bg-background"
          onClick={removeFile}
          disabled={!metadataDoc}
        >
          <IconTrash className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}

export function RecentUploads({documentIds}: RecentUploadsProps) {
  
  return (
    <div className="space-y-4">
      {documentIds?.length > 0 && documentIds?.map((documentId, index) => (
        <RecentUploadCard key={index} documentId={documentId}/>
      ))}
    </div>
  )
} 