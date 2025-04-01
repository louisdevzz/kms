import { QueryClient } from '@tanstack/react-query'
import { createRootRouteWithContext, Outlet, redirect } from '@tanstack/react-router'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { TanStackRouterDevtools } from '@tanstack/router-devtools'
import { Toaster } from '@/components/ui/toaster'
import GeneralError from '@/features/errors/general-error'
import NotFoundError from '@/features/errors/not-found-error'
import { checkAuth } from '@/lib/auth'
import { Analytics } from "@vercel/analytics/react"

export const Route = createRootRouteWithContext<{
  queryClient: QueryClient
}>()({
  component: () => {
    return (
      <>
        <Outlet />
        <Toaster />
        {import.meta.env.MODE === 'development' && (
          <>
            <ReactQueryDevtools buttonPosition='bottom-left' />
            <TanStackRouterDevtools position='bottom-right' />
            <Analytics />
          </>
        )}
      </>
    )
  },
  beforeLoad: async ({ location }) => {
    // Skip redirect for auth routes
    if (location.pathname.startsWith('/(auth)') || 
        location.pathname === '/sign-in' || 
        location.pathname === '/sign-up') {
      return
    }

    // Check if user is authenticated
    const isAuthenticated = checkAuth()
    
    if (!isAuthenticated) {
      throw redirect({
        to: '/sign-in'
      })
    }
  },
  notFoundComponent: NotFoundError,
  errorComponent: GeneralError,
})
