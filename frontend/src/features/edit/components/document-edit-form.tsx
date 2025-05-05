import { useState, useEffect } from 'react'
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
import { useAuthStore } from '@/stores/authStore'
import { fetchDocumentContent, updateDocument } from '@/lib/api'


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

const tags: { label: string; value: string }[] = [
  { label: 'Báo cáo nghiên cứu', value: 'bao_cao_nghien_cuu' },
  { label: 'Tài liệu kỹ thuật', value: 'tai_lieu_ky_thuat' },
  { label: 'Báo cáo tổng hợp', value: 'bao_cao_tong_hop' },
  { label: 'Bài thuyết trình', value: 'bai_thuyet_trinh' },
  { label: 'Hướng dẫn sử dụng', value: 'huong_dan_su_dung' },
  { label: 'Quy định chính sách', value: 'quy_dinh_chinh_sach' },
  { label: 'Quy trình nghiệp vụ', value: 'quy_trinh_nghiep_vu' },
  { label: 'Biên bản họp', value: 'bien_ban_hop' },
  { label: 'Phân tích dữ liệu', value: 'phan_tich_du_lieu' },
  { label: 'Tài liệu dự án', value: 'tai_lieu_du_an' },
  { label: 'Tài liệu đào tạo', value: 'tai_lieu_dao_tao' },
  { label: 'Mẫu tài liệu', value: 'mau_tai_lieu' },
  { label: 'Tài liệu tham khảo', value: 'tai_lieu_tham_khao' },
  { label: 'Quy trình chuẩn', value: 'quy_trinh_chuan' },
  { label: 'Kinh nghiệm thực tiễn', value: 'kinh_nghiem_thuc_tien' }
]

export function DocumentEditForm({ documentId }: { documentId: string }) {
  const [preview, setPreview] = useState<string | null>(null)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [nameFile, setNameFile] = useState<string|null>(null)
  const [type, setType] = useState<string|null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const {auth} = useAuthStore()

  const owner = auth.user?.email ?? '';

  const form = useForm<DocumentForm>({
    resolver: zodResolver(documentSchema),
    defaultValues: {
      document: undefined,
      name: '',
      doc_type: '',
      owner: owner,
      tags:[],
      category: '',
      department_id: '',
      description: '',
      university: '',
      additional: ''
    },
  })

  useEffect(() => {
    const fetchDocument = async () => {
      if (!documentId) return;
      
      try {
        setIsLoading(true);
        const document = await fetchDocumentContent(documentId, true);
        
        if (document) {
          form.reset({
            ...document,
            document: undefined, // Keep the document field as undefined since we don't want to require re-upload
          });
          
          setSelectedCategory(document.category);
          setSelectedTags(document.tags || []);
          setNameFile(document.name);
          setType(document.doc_type);
          
          // If there's a document preview URL, set it
          if (document.document_url) {
            setPreview(document.document_url);
          }
        }
      } catch (error) {
        toast({
          title: 'Error',
          description: 'Failed to load document',
          variant: 'destructive',
        });
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDocument();
  }, [documentId, form]);

  const onSubmit = async (data: DocumentForm) => {
    try {
      const formData = new FormData()
      if (data.document && data.document[0]) {
        formData.append('document', data.document[0])
      }
      formData.append('name', nameFile?.replace(/\.(pdf|txt|doc)$/, '') ?? 'Untitled')
      formData.append('doc_type', type?.replace('application/','') ?? 'pdf')
      formData.append('owner', owner)
      formData.append('department_id', data.department_id)
      formData.append('description', data.description)
      formData.append('university', data.university)

      // Append tags as individual items
      data.tags.forEach((tag) => {
        formData.append('tags', tag)
      })
      
      // Append each category individually
      formData.append('category', data.category)
      formData.append('additional', data.additional)

      // Use the update API function
      await updateDocument(documentId, formData)

      toast({
        title: 'Success',
        description: 'Document updated successfully',
      })
    } catch (error) {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to update document',
        variant: 'destructive',
      })
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      setNameFile(file.name)
      setType(file.type)
      reader.onloadend = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleCategorySelect = (value: Category) => {
    setSelectedCategory(value)
    form.setValue('category', value)
  }

  const handleTagSelect = (value: string) => {
    if (!selectedTags.includes(value)) {
      const newTags = [...selectedTags, value]
      setSelectedTags(newTags)
      form.setValue('tags', newTags)
    }
  }

  const removeTag = (value: string) => {
    const newTags = selectedTags.filter((tag) => tag !== value)
    setSelectedTags(newTags)
    form.setValue('tags', newTags)
  }

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card>
        <CardHeader>
          <CardTitle>Edit Document</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center h-[300px]">
              <p className="text-muted-foreground">Loading document...</p>
            </div>
          ) : (
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <FormField
                  control={form.control}
                  name="document"
                  render={({ field: { onChange, value, ...field } }) => (
                    <FormItem>
                      <FormLabel>File (Upload new to replace)</FormLabel>
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
                  name="category"
                  render={() => (
                    <FormItem>
                      <FormLabel>Category</FormLabel>
                      <div className="space-y-2">
                        <Select onValueChange={handleCategorySelect} value={selectedCategory || undefined}>
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select category" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {categories.map((category) => (
                              <SelectItem
                                key={category.value}
                                value={category.label}
                              >
                                {category.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
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

                <FormField
                  control={form.control}
                  name="additional"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Additional</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="tags"
                  render={() => (
                    <FormItem>
                      <FormLabel>Tags</FormLabel>
                      <div className="space-y-2">
                        <Select onValueChange={handleTagSelect}>
                          <FormControl>
                            <SelectTrigger>
                              <SelectValue placeholder="Select tags" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {tags.map((tag) => (
                              <SelectItem
                                key={tag.value}
                                value={tag.label}
                                disabled={selectedTags.includes(tag.value)}
                              >
                                {tag.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                        <div className="flex flex-wrap gap-2">
                          {selectedTags.map((tagValue) => {
                            const tagLabel = tags.find(
                              (t) => t.label === tagValue
                            )?.label
                            return (
                              <Badge
                                key={tagValue}
                                variant="secondary"
                                className="flex items-center gap-1"
                              >
                                {tagLabel}
                                <button
                                  type="button"
                                  onClick={() => removeTag(tagValue)}
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

                <Button type="submit" className="w-full">
                  Update Document
                </Button>
              </form>
            </Form>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Document Preview</CardTitle>
        </CardHeader>
        <CardContent>
          {preview ? (
            <div className="aspect-video w-full h-[600px] overflow-hidden rounded-lg border">
              <iframe
                src={preview}
                className="h-full w-full"
                title="Document Preview"
              />
            </div>
          ) : (
            <div className="flex h-[300px] items-center justify-center rounded-lg border border-dashed">
              <p className="text-muted-foreground">No document preview available</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
} 