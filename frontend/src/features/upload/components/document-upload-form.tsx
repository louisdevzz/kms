import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { toast } from '@/hooks/use-toast'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { DocumentForm, documentSchema, Category } from '../data/schema'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { X } from 'lucide-react'

const categories: { label: string; value: Category }[] = [
  { label: 'Thông tin khoa công nghệ thông tin', value: 'thong_tin_khoa_cong_nghe_thong_tin' },
  { label: 'Thông tin khoa ngôn ngữ', value: 'thong_tin_khoa_ngon_ngu' },
  { label: 'Thông tin khoa kinh tế', value: 'thong_tin_khoa_kinh_te' },
  { label: 'Thông tin khoa y', value: 'thong_tin_khoa_y' },
  { label: 'Thông tin khoa công nghệ sinh học', value: 'thong_tin_khoa_cong_nghe_sinh_hoc' },
  { label: 'Thông tin khoa điều dưỡng', value: 'thong_tin_khoa_dieu_duong' },
  { label: 'Thông tin khoa khai phóng', value: 'thong_tin_khoa_khai_phong' },
  { label: 'Thông tin giảng viên', value: 'thong_tin_giang_vien' },
  { label: 'Thông tin nghiên cứu', value: 'thong_tin_nghien_cuu' },
  { label: 'Thông tin chi phí', value: 'thong_tin_chi_phi' },
]

export function DocumentUploadForm() {
  const [preview, setPreview] = useState<string | null>(null)
  const [selectedCategories, setSelectedCategories] = useState<Category[]>([])

  const form = useForm<DocumentForm>({
    resolver: zodResolver(documentSchema),
    defaultValues: {
      document: undefined,
      name:'a',
      doc_type:'pdf',
      owner: 'vohuunhan1310@gmail.com',
      tags:['a'],
      category: [],
      department_id: '',
      description: '',
      university: ''
    },
  })

  const onSubmit = async (data: DocumentForm) => {
    console.log("uploading")
    try {
      const formData = new FormData()
      if (data.document && data.document[0]) {
        formData.append('document', data.document[0])
      }
      formData.append('name', data.name)
      formData.append('doc_type', data.doc_type)
      formData.append('owner', data.owner)
      formData.append('department_id', data.department_id)
      formData.append('description', data.description)
      formData.append('university', data.university)

      // Append tags as individual items
      data.tags.forEach((tag) => {
        formData.append('tags[]', tag)
      })
      
      // Append each category individually
      data.category.forEach((category) => {
        formData.append('category[]', category)
      })

      console.log('FormData contents:')
      for (const [key, value] of formData.entries()) {
        console.log(`${key}:  ${(value)}`)
      }

      const response = await fetch(`${import.meta.env.VITE_API_URL}/kms/document?self=true`, {
        headers:{
          "Authorization": `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2b2h1dW5oYW4xMzEwQGdtYWlsLmNvbSIsImV4cCI6MTc0NDgwNzM2MH0.CEK3FMP7EjmAAygxe_EHr_4yBRXQFW7vANShjgW6u8c`,
          "Accept": "application/json"
        },
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to upload document')
      }
      console.log(await response.json())

      toast({
        title: 'Success',
        description: 'Document uploaded successfully',
      })
      form.reset()
      setPreview(null)
      setSelectedCategories([])
    } catch (error) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to upload document',
        variant: 'destructive',
      })
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleCategorySelect = (value: Category) => {
    if (!selectedCategories.includes(value)) {
      const newCategories = [...selectedCategories, value]
      setSelectedCategories(newCategories)
      form.setValue('category', newCategories)
    }
  }

  const removeCategory = (value: Category) => {
    const newCategories = selectedCategories.filter((cat) => cat !== value)
    setSelectedCategories(newCategories)
    form.setValue('category', newCategories)
  }

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Upload Document</CardTitle>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="document"
                render={({ field: { onChange, value, ...field } }) => (
                  <FormItem>
                    <FormLabel>File</FormLabel>
                    <FormControl>
                      <Input
                        type="file"
                        onChange={(e) => {
                          onChange(e.target.files)
                          handleFileChange(e)
                        }}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="owner"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Owner</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="category"
                render={() => (
                  <FormItem>
                    <FormLabel>Categories</FormLabel>
                    <div className="space-y-2">
                      <Select onValueChange={handleCategorySelect}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select categories" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {categories.map((category) => (
                            <SelectItem
                              key={category.value}
                              value={category.value}
                              disabled={selectedCategories.includes(category.value)}
                            >
                              {category.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <div className="flex flex-wrap gap-2">
                        {selectedCategories.map((category) => {
                          const categoryLabel = categories.find(
                            (c) => c.value === category
                          )?.label
                          return (
                            <Badge
                              key={category}
                              variant="secondary"
                              className="flex items-center gap-1"
                            >
                              {categoryLabel}
                              <button
                                type="button"
                                onClick={() => removeCategory(category)}
                                className="ml-1 rounded-full hover:bg-muted"
                              >
                                <X className="h-3 w-3" />
                              </button>
                            </Badge>
                          )
                        })}
                      </div>
                    </div>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="department_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Department</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Textarea {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="university"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>University</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button type="submit" className="w-full">
                Upload Document
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Document Preview</CardTitle>
        </CardHeader>
        <CardContent>
          {preview ? (
            <div className="aspect-video w-full overflow-hidden rounded-lg border">
              <iframe
                src={preview}
                className="h-full w-full"
                title="Document Preview"
              />
            </div>
          ) : (
            <div className="flex h-[300px] items-center justify-center rounded-lg border border-dashed">
              <p className="text-muted-foreground">No document selected</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
} 