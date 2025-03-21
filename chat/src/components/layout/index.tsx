import { PanelRightClose } from "lucide-react"
import Sidebar from "../Sidebar"
import { useState } from "react"
import { useNavigate } from "@tanstack/react-router"

export default function Layout({children}: {children: React.ReactNode}) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const navigate = useNavigate()


  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen)
  }

  const handleNewChat = () => {
    navigate({to: "/"})
  }

  const handleClearConversations = () => {
    navigate({to: "/"})
  }

  const handleToggleTheme = () => {
    // Toggle theme logic can be implemented later
  }

  return (
    <>
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
        <main className="flex-1 bg-white">
          {children}
        </main>
        </div>
    </>
  )
}