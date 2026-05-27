import { useState } from 'react'
import axios from "axios"
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [query, setQuery] = useState("")

  async function handleSend() {

    const newMessages = [
      ...messages,
      {
        role: "user",
        content: query
      }
    ]

    setMessages(newMessages)

    const response = await axios.post(
      "http://localhost:8000/chat",
      {
        messages: newMessages
      }
    )

    setMessages([
      ...newMessages,
      {
        role: "assistant",
        content: response.data.reply
      }
    ])

    setQuery("")

  }

  return (
    <div className="h-screen flex flex-col bg-gray-950 text-white">

      {/* messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`
                max-w-[75%] px-3 py-2 rounded-xl text-sm
                ${msg.role === "user"
                  ? "bg-blue-600"
                  : "bg-gray-800"
                }
              `}
            >
              {msg.content}
            </div>
          </div>
        ))}
      </div>

      {/* input */}
      <div className="p-3 border-t border-gray-800 flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          className="flex-1 bg-gray-900 px-3 py-2 rounded-lg outline-none"
          placeholder="Écris un message..."
        />

        <button
          onClick={handleSend}
          className="bg-blue-600 px-4 rounded-lg hover:bg-blue-500 transition"
        >
          Envoyer
        </button>
      </div>

    </div>
  )
}

export default App
