import React, { useState } from 'react'
import useDialogState from '@/hooks/use-dialog-state'
import { DocumentForm } from '../data/schema'

type DocumentDialogType = 'create' | 'update' | 'delete' | 'import'

interface DocumentContextType {
  open: DocumentDialogType | null
  setOpen: (str: DocumentDialogType | null) => void
  currentRow: DocumentForm | null
  setCurrentRow: React.Dispatch<React.SetStateAction<DocumentForm | null>>
}

const DocumentContext = React.createContext<DocumentContextType | null>(null)

interface Props {
  children: React.ReactNode
}

export default function DocumentProvider({ children }: Props) {
  const [open, setOpen] = useDialogState<DocumentDialogType>(null)
  const [currentRow, setCurrentRow] = useState<DocumentForm | null>(null)
  return (
    <DocumentContext value={{ open, setOpen, currentRow, setCurrentRow }}>
      {children}
    </DocumentContext>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export const useDocument = () => {
  const documentContext = React.useContext(DocumentContext)

  if (!documentContext) {
    throw new Error('useDocument has to be used within <DocumentContext>')
  }

  return documentContext
}
