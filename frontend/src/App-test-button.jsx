import React, { useState } from 'react'

function App() {
  const [apiStatus, setApiStatus] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  
  const checkApiHealth = async () => {
    setIsLoading(true)
    setApiStatus('Checking...')
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/health`)
      const data = await response.json()
      
      if (response.ok) {
        setApiStatus(`✅ API Health: ${data.status} - ${data.service}`)
      } else {
        setApiStatus(`❌ API Error: ${response.status}`)
      }
    } catch (error) {
      setApiStatus(`❌ Connection Failed: ${error.message}`)
    } finally {
      setIsLoading(false)
    }
  }
  
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial', maxWidth: '800px' }}>
      <h1>🎉 AI Sahayak Frontend</h1>
      <p>React app is running successfully!</p>
      
      {/* API Health Check Section */}
      <div style={{ 
        marginTop: '30px', 
        padding: '20px', 
        background: '#f8f9fa', 
        border: '2px solid #007bff',
        borderRadius: '8px'
      }}>
        <h2>🔧 API Health Check</h2>
        
        <button 
          onClick={checkApiHealth}
          disabled={isLoading}
          style={{
            background: isLoading ? '#6c757d' : '#007bff',
            color: 'white',
            border: 'none',
            padding: '12px 24px',
            borderRadius: '6px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            fontWeight: 'bold',
            marginBottom: '15px'
          }}
        >
          {isLoading ? '⏳ Checking...' : '🩺 Check API Health'}
        </button>
        
        {apiStatus && (
          <div style={{ 
            padding: '15px', 
            background: apiStatus.includes('✅') ? '#d4edda' : '#f8d7da',
            border: `2px solid ${apiStatus.includes('✅') ? '#28a745' : '#dc3545'}`,
            borderRadius: '6px',
            fontFamily: 'monospace',
            fontSize: '14px',
            marginTop: '10px'
          }}>
            <strong>{apiStatus}</strong>
          </div>
        )}
      </div>
      
      {/* Environment Info */}
      <div style={{ marginTop: '30px', padding: '15px', background: '#e9ecef', borderRadius: '6px' }}>
        <h3>Environment Info:</h3>
        <ul>
          <li>API Base URL: <code>{import.meta.env.VITE_API_BASE_URL || 'Not configured'}</code></li>
          <li>Mode: <code>{import.meta.env.MODE}</code></li>
          <li>Firebase configured: {import.meta.env.VITE_FIREBASE_API_KEY ? '✅ Yes' : '❌ No'}</li>
        </ul>
      </div>
    </div>
  )
}

export default App
