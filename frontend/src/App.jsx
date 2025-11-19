import { useState } from 'react'
import './App.css'

function App() {
  const [tweet, setTweet] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!tweet.trim()) {
      setError('Please enter a tweet')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const res = await fetch('http://localhost:8000/reply', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tweet }),
      })

      if (!res.ok) {
        throw new Error('Failed to get response from server')
      }

      const data = await res.json()
      setResult(data)
      setTweet('') // Clear input after successful submission
    } catch (err) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const getClassificationColor = (classification) => {
    const colors = {
      'COMPLIMENT': '#4ade80',
      'SUPPORT': '#60a5fa',
      'TROLL': '#f87171'
    }
    return colors[classification] || '#9ca3af'
  }

  const getClassificationEmoji = (classification) => {
    const emojis = {
      'COMPLIMENT': '💚',
      'SUPPORT': '🤝',
      'TROLL': '🛡️'
    }
    return emojis[classification] || '📝'
  }

  return (
    <div className="App">
      <h1>🤖 AI Tweet Reply Bot</h1>
      <p className="subtitle">Multi-Agent System powered by LangGraph</p>
      
      <form onSubmit={handleSubmit} className="chat-form">
        <div className="input-group">
          <textarea
            value={tweet}
            onChange={(e) => setTweet(e.target.value)}
            placeholder="Paste a tweet here to generate a reply..."
            disabled={loading}
            className="tweet-input"
            rows="3"
          />
          <button 
            type="submit" 
            disabled={loading}
            className="send-button"
          >
            {loading ? 'Analyzing...' : 'Generate Reply'}
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="result-container">
          <div className="classification-badge" style={{ backgroundColor: getClassificationColor(result.classification) }}>
            <span className="classification-emoji">{getClassificationEmoji(result.classification)}</span>
            <span className="classification-text">{result.classification}</span>
          </div>
          
          <div className="tweet-box">
            <h3>Original Tweet:</h3>
            <p className="tweet-text">{result.tweet}</p>
          </div>

          <div className="response-box">
            <h3>Generated Reply:</h3>
            <p className="response-text">{result.response}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default App

