import { z } from 'zod'

export const categoryEnum = z.enum([
  'thong_tin_truong_dai_hoc',
  'thong_tin_khoa_cong_nghe_thong_tin',
  'thong_tin_khoa_ngon_ngu',
  'thong_tin_khoa_kinh_te',
  'thong_tin_khoa_y',
  'thong_tin_khoa_cong_nghe_sinh_hoc',
  'thong_tin_khoa_dieu_duong',
  'thong_tin_khoa_khai_phong',
  'thong_tin_giang_vien',
  'thong_tin_nghien_cuu',
  'thong_tin_chi_phi',
])

export type Category = z.infer<typeof categoryEnum>

export const documentSchema = z.object({
  document: z
    .instanceof(FileList)
    .refine((files) => files.length > 0, {
      message: 'Please upload a file',
    }),
  name: z.string(),
  doc_type: z.string(),
  owner: z.string().min(1, 'Owner is required'),
  category: z.string().min(1, 'At least one category is required'),
  tags:z.array(z.string()),
  department_id: z.string().min(1, 'Department is required'),
  description: z.string().min(1, 'Description is required'),
  university: z.string().min(1, 'University is required'),
  additional: z.string()
})

export type DocumentForm = z.infer<typeof documentSchema>
