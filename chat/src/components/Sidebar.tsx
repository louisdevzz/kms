interface SidebarProps {
  onNewChat: () => void
  onClearConversations: () => void
  onToggleTheme: () => void
}

export default function Sidebar({ onNewChat, onClearConversations, onToggleTheme }: SidebarProps) {
  return (
    <aside className="h-full flex flex-col">
      {/* Top section with New Chat and History */}
      <div className="flex-1 flex flex-col gap-1 p-5">
        <button 
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2 bg-black text-white rounded-xl py-2 px-4 cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          <span className="text-lg">New chat</span>
        </button>
        
        {/* Chat History */}
        <div className="flex flex-col gap-1 mt-1">
          <button className="flex items-center gap-3 p-3 hover:bg-gray-100 rounded-lg w-full">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            <span className="text-sm">AI Chat Tool Ethics</span>
          </button>
          <button className="flex items-center gap-3 p-3 hover:bg-gray-100 rounded-lg w-full">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            <span className="text-sm">AI Chat Tool Impact Writing</span>
          </button>
        </div>
      </div>

      {/* Footer Section - Fixed at bottom */}
      <div className="mt-auto border-t border-[rgba(0,0,0,0.1)] p-2">
        <button 
          onClick={onClearConversations}
          className="flex items-center gap-3 p-3 hover:bg-gray-100 rounded-lg w-full"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          <span className="text-sm">Clear conversations</span>
        </button>
        <button 
          onClick={onToggleTheme}
          className="flex items-center gap-3 p-3 hover:bg-gray-100 rounded-lg w-full"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <span className="text-sm">Light mode</span>
        </button>
        <button className="flex items-center gap-3 p-3 hover:bg-gray-100 rounded-lg w-full">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span className="text-sm">My account</span>
        </button>
        <button className="flex items-center gap-3 p-3 hover:bg-gray-100 rounded-lg w-full">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          <span className="text-sm">Updates & FAQ</span>
        </button>
        <button className="flex items-center gap-3 p-3 hover:bg-gray-100 rounded-lg w-full">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span className="text-sm">Log out</span>
        </button>
      </div>
    </aside>
  )
} 