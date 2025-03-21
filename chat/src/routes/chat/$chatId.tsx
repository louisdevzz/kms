import { createFileRoute } from "@tanstack/react-router"
import ChatDetails from "../../components/ChatDetails"
import Layout from "../../components/layout"


export const Route = createFileRoute('/chat/$chatId')({
  component: ChatDetailsPage
})

function ChatDetailsPage() {
  return (
    <Layout>
      <ChatDetails />
    </Layout>
  )
}

