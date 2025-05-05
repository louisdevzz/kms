import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ProfileDropdown } from '@/components/profile-dropdown'
import { Search } from '@/components/search'
import { ThemeSwitch } from '@/components/theme-switch'
import { DocumentEditForm } from './components/document-edit-form'
import EditProvider from './context/edit-context'

export default function Edit({ documentId }: { documentId: string }) {
  console.log('documentId', documentId)
  return (
    <EditProvider>
      <Header fixed>
        <Search />
        <div className='ml-auto flex items-center space-x-4'>
          <ThemeSwitch />
          <ProfileDropdown />
        </div>
      </Header>

      <Main>
        <div className='mb-2 flex flex-wrap items-center justify-between gap-x-4 space-y-2'>
          <div>
            <h2 className='text-2xl font-bold tracking-tight'>Edit Documents</h2>
            <p className='text-muted-foreground'>
              Here&apos;s a form to edit your documents
            </p>
          </div>
        </div>
        <div className='-mx-4 flex-1 overflow-auto px-4 py-1 lg:flex-row lg:space-x-12 lg:space-y-0'>
          <DocumentEditForm documentId={documentId} />
        </div>
      </Main>
    </EditProvider>
  )
}
