import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const getBaseUrl = () => {
  const envUrl = import.meta.env.VITE_API_URL || 'https://kms-production-958c.up.railway.app'
  // Ensure the URL has a protocol
  if (!envUrl.startsWith('http://') && !envUrl.startsWith('https://')) {
    return `https://${envUrl}`
  }
  return envUrl
}

const baseUrl = getBaseUrl()

const api = axios.create({
  baseURL: `${baseUrl}/kms`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to add auth token
api.interceptors.request.use((config) => {
  const { auth } = useAuthStore.getState()
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`
  }
  return config
})

export const fetchUser = async () => {
  try {
    const response = await api.get('/auth/me')
    // console.log(response)
    const { setUser } = useAuthStore.getState().auth
    setUser(response.data)
    return response.data
  } catch (error) {
    console.error('Error fetching user:', error)
    throw error
  }
}

/**
 * Upload a document to the server
 * @param formData - FormData object containing document and metadata
 * @param self - Whether the document is for personal use (default: true)
 * @returns The response data from the server
 */
export const uploadDocument = async (formData: FormData, self: boolean = true) => {
  try {
    const uploadApi = axios.create({
      baseURL: `${baseUrl}/kms`,
      headers: {
        'Authorization': `Bearer ${useAuthStore.getState().auth.accessToken}`,
        'Accept': 'application/json',
      },
    })
    
    const response = await uploadApi.post(`/document?self=${self}`, formData)
    return response.data
  } catch (error) {
    console.error('Error uploading document:', error)
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || 'Failed to upload document')
    }
    throw error
  }
}

/**
 * Fetch document IDs for the authenticated user
 * @param self - Whether to fetch only personal documents (default: true)
 * @returns Array of document IDs
 */
export const fetchDocuments = async (self: boolean = true) => {
  try {
    const response = await api.get(`/document/ids?self=${self}`)
    return response.data
  } catch (error) {
    console.error('Error fetching documents:', error)
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch documents')
    }
    throw error
  }
}

/**
 * Fetch metadata for a specific document
 * @param documentId - The ID of the document to fetch metadata for
 * @param self - Whether to fetch only personal document (default: true)
 * @returns Document metadata
 */
export const fetchDocumentMetadata = async (documentId: string, self: boolean = true) => {
  try {
    const response = await api.get(`/document/${documentId}?self=${self}`)
    return response.data
  } catch (error) {
    console.error('Error fetching document metadata:', error)
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch document metadata')
    }
    throw error
  }
}

/**
 * Fetch document content
 * @param documentId - The ID of the document to fetch content for
 * @param self - Whether to fetch only personal document (default: true)
 * @returns Document content as ArrayBuffer
 */
export const fetchDocumentContent = async (documentId: string, self: boolean = true) => {
  try {
    const response = await api.get(`/document/${documentId}/content?self=${self}`, {
      headers: {
        'Accept': 'application/pdf'
      },
      responseType: 'arraybuffer'
    })
    return response.data
  } catch (error) {
    console.error('Error fetching document content:', error)
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || 'Failed to fetch document content')
    }
    throw error
  }
}

/**
 * Remove a document from the server
 * @param documentId - The ID of the document to remove
 * @param self - Whether to remove only personal document (default: true)
 * @returns void
 */
export const removeDocument = async (documentId: string, self: boolean = true) => {
  try {
    await api.delete(`/document/${documentId}?self=${self}`)
  } catch (error) {
    console.error('Error removing document:', error)
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || 'Failed to remove document')
    }
    throw error
  }
}

export default api 