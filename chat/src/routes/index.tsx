import { useState, useRef, useEffect } from 'react'
import { createFileRoute, useNavigate } from '@tanstack/react-router'
import Sidebar from '../components/Sidebar'
import { PanelRightClose, ArrowUp } from 'lucide-react'
import { v4 as uuidv4 } from 'uuid'


export const Route = createFileRoute('/')({
  component: ChatPage,
})

function ChatPage() {
  const [messages, setMessages] = useState<string[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputValue.trim()) {
      setMessages([...messages, inputValue])
      setInputValue('')
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
        navigate({to: "/chat/" + uuidv4()})
      }
    }
  }

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px'
    }
  }

  useEffect(() => {
    adjustTextareaHeight()
  }, [inputValue])

  const handleNewChat = () => {
    setMessages([])
    setInputValue('')
  }

  const handleClearConversations = () => {
    setMessages([])
  }

  const handleToggleTheme = () => {
    setIsDarkMode(!isDarkMode)
  }

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen)
  }

  return (
    <div className="flex h-screen">
      {/* Mobile Sidebar Toggle */}
      <button
        onClick={toggleSidebar}
        className="lg:hidden fixed top-2 left-2 z-50 p-2 bg-white rounded-lg shadow-lg hover:bg-gray-100"
      >
        <PanelRightClose className="h-6 w-6" />
      </button>

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 w-[282px] bg-white z-40 lg:relative
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0 transition-transform duration-300 ease-in-out
        border-r border-gray-200
      `}>
        {/* Overlay for mobile */}
        <div
          className={`lg:hidden fixed inset-0 -z-10 ${isSidebarOpen ? 'block' : 'hidden'}`}
          onClick={toggleSidebar}
        />
        
        <Sidebar
          onNewChat={handleNewChat}
          onClearConversations={handleClearConversations}
          onToggleTheme={handleToggleTheme}
        />
      </div>

      {/* Main Content */}
      <main className="flex-1 bg-white">
        <div className="flex flex-col h-full">
          {/* Chat Area with Centered Input */}
          <div className="flex-1 flex flex-col items-center justify-center px-4">
            <div className="max-w-[800px] w-full space-y-8">
              <div className="text-center">
                <h1 className="text-5xl font-semibold mb-2">Good morning, Louis.</h1>
                <p className="text-[20px] text-gray-600">How can I help you today?</p>
              </div>

              {/* Input Area - Centered */}
              <div className="w-full">
                <form onSubmit={handleSubmit} className="relative bg-white rounded-2xl shadow-sm border border-gray-200">
                  <textarea
                    ref={textareaRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault()
                        handleSubmit(e)
                      }
                    }}
                    placeholder="What would you like to know?"
                    rows={1}
                    className="w-full min-h-[100px] max-h-[800px] py-4 px-4 pr-12 rounded-2xl focus:outline-none resize-none overflow-y-hidden"
                  />
                  <button 
                    type="submit" 
                    className="absolute right-2 bottom-2 bg-gray-200 rounded-full p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-300 cursor-pointer disabled:opacity-40"
                    disabled={!inputValue.trim()}
                  >
                    <ArrowUp className="h-5 w-5" />
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
} 