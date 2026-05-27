import { useState, useRef, useEffect } from 'react'
import axios from "axios"

function App() {

  // =========================================================
  // États
  // =========================================================

  // Historique des messages affichés dans le chat
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Bonjour, comment puis-je vous aider ?" }
  ])

  // Contenu de l'input utilisateur
  const [query, setQuery] = useState("")

  // Vrai pendant qu'on attend la réponse d'Ollama
  const [isLoading, setIsLoading] = useState(false)

  // Changement de thème light ou dark
  const [darkMode, setDarkMode] = useState(false)
  
  // Référence vers le bas de la liste de messages (pour le scroll auto)
  const bottomRef = useRef(null)


  // =========================================================
  // Scroll automatique vers le dernier message
  // =========================================================

  // S'exécute à chaque fois que `messages` change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

// Changement de thème light ou dark
  useEffect(() => {
  if (darkMode) {
    document.documentElement.classList.add("dark")
  } else {
    document.documentElement.classList.remove("dark")
  }
}, [darkMode])

  // =========================================================
  // Envoi d'un message
  // =========================================================

  async function handleSend() {

    // Nettoyage de l'input (supprime les espaces en début/fin)
    const trimmed = query.trim()

    // Bloque l'envoi si le message est vide ou si une réponse est déjà en cours
    if (!trimmed || isLoading) return

    // Ajout du message utilisateur à l'historique local
    const newMessages = [...messages, { role: "user", content: trimmed }]
    setMessages(newMessages)

    // Réinitialise l'input immédiatement (ne pas attendre la réponse)
    setQuery("")

    // Active l'indicateur de chargement
    setIsLoading(true)

    try {

      // Envoi de l'historique complet au backend FastAPI
      const response = await axios.post("http://localhost:8000/chat", {
        messages: newMessages
      })

      // Ajout de la réponse de l'assistant à l'historique
      setMessages([...newMessages, { role: "assistant", content: response.data.reply }])

    } catch (err) {

      // En cas d'erreur réseau ou serveur, on affiche un message d'erreur
      console.error("Erreur:", err)
      setMessages([...newMessages, { role: "assistant", content: "⚠️ Erreur de connexion." }])

    } finally {

      // Désactive le chargement dans tous les cas (succès ou erreur)
      setIsLoading(false)

    }
  }


  // =========================================================
  // Rendu
  // =========================================================

  return (
    <div className="h-screen flex flex-col bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-white">

      {/* Barre du haut avec le nom et le statut */}
      <div className="flex items-center gap-3 px-4 py-3 border-b border-gray-200 dark:border-gray-800">
        <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center text-blue-600 dark:text-blue-300 text-sm">
          🤖
        </div>
        <span className="text-sm font-medium">Assistant</span>

        {/* Point vert = connecté */}
        <span className="ml-auto text-xs text-gray-400 flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-green-500 inline-block" />
          En ligne
        </span>
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="px-3 py-1 rounded-lg bg-gray-200 dark:bg-gray-700 text-sm"
        >
          {darkMode ? "☀️ Light" : "🌙 Dark"}
        </button>
      </div>

      {/* Zone de messages avec scroll */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-3">
        {messages.map((msg, i) => (

          // Aligne à droite pour l'utilisateur, à gauche pour l'assistant
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`
              max-w-[72%] px-4 py-2.5 text-sm leading-relaxed
              ${msg.role === "user"
                // Bulle bleue pour l'utilisateur, coin haut-droit aplati
                ? "bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100 rounded-xl rounded-tr-sm"
                // Bulle blanche pour l'assistant, coin haut-gauche aplati
                : "bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100 rounded-xl rounded-tl-sm"
              }
            `}>
              {msg.content}
            </div>
          </div>
        ))}

        {/* Indicateur "en train d'écrire..." affiché pendant le chargement */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl rounded-tl-sm px-4 py-3 flex gap-1">
              {/* 3 points qui pulsent avec un délai décalé */}
              {[0, 1, 2].map(i => (
                <span key={i} className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-pulse"
                  style={{ animationDelay: `${i * 0.15}s` }} />
              ))}
            </div>
          </div>
        )}

        {/* Ancre invisible en bas pour le scroll automatique */}
        <div ref={bottomRef} />
      </div>

      {/* Zone de saisie */}
      <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-800 flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          // Envoi avec la touche Entrée
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          // Bloqué pendant le chargement
          disabled={isLoading}
          className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 px-4 py-2 rounded-xl text-sm outline-none focus:border-blue-400 disabled:opacity-50"
          placeholder="Écris un message..."
        />

        {/* Bouton d'envoi, désactivé pendant le chargement */}
        <button
          onClick={handleSend}
          disabled={isLoading}
          className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 flex items-center justify-center hover:bg-blue-200 dark:hover:bg-blue-800 transition disabled:opacity-50"
        >
          ➤
        </button>
      </div>

    </div>
  )
}

export default App