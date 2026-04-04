import { useEffect, useRef, useState } from 'react'
import './ChatPanel.css'

export default function ChatPanel({ messages, loading, onSend }) {
  const [input, setInput] = useState('')
  const bottomRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  function submit() {
    if (!input.trim()) return
    onSend(input.trim())
    setInput('')
    textareaRef.current?.focus()
  }

  const suggestions = [
    'Romantic dinner in Bandra, ₹3000 for two',
    'Sunday brunch with friends in Hauz Khas',
    'Adventure day in Rishikesh, solo traveller',
    'Family day out in Pune, kids friendly'
  ]

  return (
    <div className="chat-panel">
      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`message message--${m.role}${m.error ? ' message--error' : ''}`}>
            {m.role === 'assistant' && <div className="message-avatar">I</div>}
            <div className="message-bubble">
              {m.text.split('\n').map((line, j) =>
                line ? <p key={j}>{line}</p> : <br key={j} />
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message message--assistant">
            <div className="message-avatar">I</div>
            <div className="message-bubble typing">
              <span /><span /><span />
            </div>
          </div>
        )}

        {messages.length === 1 && !loading && (
          <div className="suggestions">
            {suggestions.map((s, i) => (
              <button key={i} className="suggestion-chip" onClick={() => onSend(s)}>{s}</button>
            ))}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="chat-input-row">
        <textarea
          ref={textareaRef}
          className="chat-input"
          rows={2}
          placeholder="Describe your perfect outing…"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
        />
        <button className="send-btn" onClick={submit} disabled={!input.trim() || loading}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
    </div>
  )
}
