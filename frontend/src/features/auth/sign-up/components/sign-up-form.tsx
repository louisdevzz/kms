import { HTMLAttributes, useState } from 'react'
import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { IconBrandGoogle } from '@tabler/icons-react'
import { cn } from '@/lib/utils'
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
import { PasswordInput } from '@/components/password-input'
import { useNavigate } from '@tanstack/react-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

type SignUpFormProps = HTMLAttributes<HTMLDivElement>

const formSchema = z
  .object({
    email: z
      .string()
      .min(1, { message: 'Please enter your email' })
      .email({ message: 'Invalid email address' }),
    password: z
      .string()
      .min(1, {
        message: 'Please enter your password',
      })
      .min(7, {
        message: 'Password must be at least 7 characters long',
      }),
    name: z.string().min(1, { message: 'Please enter your name' }),
    department_id: z.string().min(1, { message: 'Please enter your department' }),
    roles: z.string().min(1, { message: 'Please enter at least one role' })
  })

export function SignUpForm({ className, ...props }: SignUpFormProps) {
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()
  const setAccessToken = useAuthStore((state) => state.auth.setAccessToken)
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: '',
      password: '',
      name: '',
      department_id: '',
      roles: '',
    },
  })

  async function onSubmit(data: z.infer<typeof formSchema>) {
    setIsLoading(true)
    try {
      const formData = new FormData()
      formData.append('email', data.email)
      formData.append('password', data.password)
      formData.append('name', data.name)
      formData.append('department_id', data.department_id)
      // Split roles string into array and append each role
      const rolesArray = data.roles.split(',').map(role => role.trim())
      rolesArray.forEach(role => {
        formData.append('roles', role)
      })

      const baseUrl = 'https://kms-production-958c.up.railway.app'
      const apiUrl = `${baseUrl}/kms/auth/signup`

      const signUpRes = await axios.post(apiUrl, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      if(signUpRes.status == 200){
        // After successful signup, automatically sign in
        const loginFormData = new FormData()
        loginFormData.append('email', data.email)
        loginFormData.append('password', data.password)

        const loginUrl = `${baseUrl}/kms/auth/login`
        const loginRes = await axios.post(loginUrl, loginFormData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })

        if(loginRes.status == 200){
          localStorage.setItem('email', data.email)
          setAccessToken(loginRes.data.access_token)
          navigate({to: "/"})
        }
      }
    } catch (error) {
      console.error('Signup error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className={cn('grid gap-6', className)} {...props}>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)}>
          <div className='grid gap-2'>
            <FormField
              control={form.control}
              name='email'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input placeholder='name@example.com' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='password'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <PasswordInput placeholder='********' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='name'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input placeholder='John Doe' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='department_id'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Department</FormLabel>
                  <FormControl>
                    <Input placeholder='IT' {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name='roles'
              render={({ field }) => (
                <FormItem className='space-y-1'>
                  <FormLabel>Roles (comma-separated)</FormLabel>
                  <FormControl>
                    <Input 
                      placeholder='Admin, User, Manager' 
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button className='mt-2' disabled={isLoading}>
              Create Account
            </Button>

            <div className='relative my-2'>
              <div className='absolute inset-0 flex items-center'>
                <span className='w-full border-t' />
              </div>
              <div className='relative flex justify-center text-xs uppercase'>
                <span className='bg-background px-2 text-muted-foreground'>
                  Or continue with
                </span>
              </div>
            </div>

            <div className='flex items-center gap-2'>
              <Button
                variant='outline'
                className='w-full'
                type='button'
                disabled={isLoading}
              >
                <IconBrandGoogle className='h-4 w-4' /> Google
              </Button>
            </div>
          </div>
        </form>
      </Form>
    </div>
  )
}
