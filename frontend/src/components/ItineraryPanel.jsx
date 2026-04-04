import './ItineraryPanel.css'

const BADGE_COLORS = ['badge--blue', 'badge--lav', 'badge--pink', 'badge--aqua', 'badge--green']

function ScoreBadge({ label, value, index }) {
  const pct = typeof value === 'number' ? value : parseFloat(value) || 0
  const color = BADGE_COLORS[index % BADGE_COLORS.length]
  return (
    <div className={`score-badge ${color}`}>
      <span className="badge-label">{label}</span>
      <span className="badge-value">{Math.round(pct)}</span>
    </div>
  )
}

function TransportLeg({ leg }) {
  const icons = { walking: '🚶', driving: '🚗', transit: '🚇', auto: '🛺', metro: '🚇' }
  const icon = icons[leg.mode?.toLowerCase()] || '→'
  return (
    <div className="transport-leg">
      <span className="leg-icon">{icon}</span>
      <span className="leg-text">{leg.mode || 'Walk'} · {leg.duration || leg.time || '—'}</span>
      {leg.distance && <span className="leg-dist">{leg.distance}</span>}
    </div>
  )
}

function StopCard({ stop, index }) {
  return (
    <div className="stop-card">
      <div className="stop-index">{index + 1}</div>
      <div className="stop-body">
        <div className="stop-time">{stop.time || stop.start_time || ''}</div>
        <div className="stop-name">{stop.name || stop.venue}</div>
        {stop.address && <div className="stop-address">{stop.address}</div>}
        {stop.activity && <div className="stop-activity">{stop.activity}</div>}
        {stop.estimated_cost && <div className="stop-cost">~{stop.estimated_cost}</div>}
      </div>
    </div>
  )
}

function parseStops(it) {
  if (!it) return []
  if (Array.isArray(it.stops)) return it.stops
  if (Array.isArray(it.itinerary)) return it.itinerary
  if (Array.isArray(it.places)) return it.places
  return []
}

function parseLegs(it) {
  if (!it) return []
  if (Array.isArray(it.transportation)) return it.transportation
  if (Array.isArray(it.transport_legs)) return it.transport_legs
  if (Array.isArray(it.legs)) return it.legs
  return []
}

function parseScores(it) {
  if (!it) return {}
  return it.scores || it.score || {}
}

export default function ItineraryPanel({ itinerary, onSaveCalendar, onRegenerate }) {
  const stops = parseStops(itinerary)
  const legs = parseLegs(itinerary)
  const scores = parseScores(itinerary)
  const hasScores = Object.keys(scores).length > 0

  if (!itinerary) {
    return (
      <div className="itinerary-panel itinerary-empty">
        <div className="empty-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" opacity="0.2">
            <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
        </div>
        <p className="empty-title">Your itinerary will appear here</p>
        <p className="empty-sub">Ask Itinera to plan something and watch the magic happen</p>
      </div>
    )
  }

  return (
    <div className="itinerary-panel">
      <div className="itinerary-header">
        <div>
          <h2 className="itinerary-title">{itinerary.title || itinerary.summary || 'Your Plan'}</h2>
          {itinerary.total_cost && <p className="itinerary-meta">Est. total · {itinerary.total_cost}</p>}
        </div>
        <div className="itinerary-actions">
          <button className="action-btn action-btn--ghost" onClick={onRegenerate}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/>
              <path d="M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15"/>
            </svg>
            Regenerate
          </button>
          <button className="action-btn action-btn--accent" onClick={onSaveCalendar}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
              <line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/>
              <line x1="3" y1="10" x2="21" y2="10"/>
            </svg>
            Save to Calendar
          </button>
        </div>
      </div>

      {hasScores && (
        <div className="scores-row">
          {Object.entries(scores).map(([k, v], i) => (
            <ScoreBadge key={k} label={k} value={v} index={i} />
          ))}
        </div>
      )}

      <div className="itinerary-timeline">
        {stops.map((stop, i) => (
          <div key={i}>
            <StopCard stop={stop} index={i} />
            {legs[i] && <TransportLeg leg={legs[i]} />}
          </div>
        ))}
        {stops.length === 0 && (
          <p className="no-stops">Plan received — check the chat for your full itinerary.</p>
        )}
      </div>
    </div>
  )
}
