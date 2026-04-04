import { useState, useRef } from 'react'
import ChatPanel from './components/ChatPanel.jsx'
import ItineraryPanel from './components/ItineraryPanel.jsx'
import './App.css'

const BACKEND = import.meta.env.VITE_BACKEND_URL || ''

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: "Hello! I'm Itinera — your AI activity planner. Tell me where you're headed, what vibe you're after, and I'll craft the perfect plan. Try something like:\n\n\"Plan a romantic dinner date in Bandra, Mumbai, budget ₹3000 for two.\""
    }
  ])
  const [itinerary, setItinerary] = useState(null)
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const userId = useRef('user_' + Math.random().toString(36).slice(2, 9))

  async function sendMessage(text) {
    if (!text.trim() || loading) return
    setMessages(prev => [...prev, { role: 'user', text }])
    setLoading(true)
    try {
      const res = await fetch(`${BACKEND}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, user_id: userId.current, session_id: sessionId })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Server error')
      setSessionId(data.session_id)
      setMessages(prev => [...prev, { role: 'assistant', text: data.response }])
      if (data.itinerary) setItinerary(data.itinerary)
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', text: `Something went wrong: ${err.message}`, error: true }])
    } finally {
      setLoading(false)
    }
  }

  async function saveToCalendar() {
    if (!itinerary) return
    try {
      const res = await fetch(`${BACKEND}/calendar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(itinerary)
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: 'assistant', text: data.message || 'Events saved to your calendar!' }])
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', text: 'Calendar save failed. Please try again.' }])
    }
  }

  function regenerate() {
    const last = messages.filter(m => m.role === 'user').pop()
    if (last) sendMessage(last.text + ' (please regenerate with a fresh variation)')
  }

  return (
    <div className="app-layout">
      <div className="app-header">
        <span className="logo-text">Itinera</span>
        <span className="logo-sub">AI Activity Planner</span>
      </div>
      <div className="panels">
        <ChatPanel messages={messages} loading={loading} onSend={sendMessage} />
        <ItineraryPanel itinerary={itinerary} onSaveCalendar={saveToCalendar} onRegenerate={regenerate} />
      </div>
    </div>
  )
}
