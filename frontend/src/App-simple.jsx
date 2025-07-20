import React, { useState } from 'react'

function App() {
  const [apiStatus, setApiStatus] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  
  console.log('App component is rendering')
  console.log('Firebase API Key:', import.meta.env.VITE_FIREBASE_API_KEY)
  console.log('All env vars:', import.meta.env)
  
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
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>🎉 AI Sahayak Frontend is Working!</h1>
      <p>If you see this, React is loading properly.</p>
      <div style={{ marginTop: '20px', padding: '10px', background: '#f0f0f0' }}>
        <h3>Environment Check:</h3>
        <p>Node ENV: {import.meta.env.MODE}</p>
        <p>Firebase API Key: {import.meta.env.VITE_FIREBASE_API_KEY ? '✅ Set' : '❌ Missing'}</p>
        <p>Project ID: {import.meta.env.VITE_FIREBASE_PROJECT_ID || 'Not set'}</p>
        <p>API Base URL: {import.meta.env.VITE_API_BASE_URL || 'Not set'}</p>
      </div>
      
      <div style={{ marginTop: '20px', padding: '10px', background: '#e8f4f8', border: '1px solid #4f46e5' }}>
        <h3>🔧 API Health Check:</h3>
        <button 
          onClick={checkApiHealth}
          disabled={isLoading}
          style={{
            background: isLoading ? '#ccc' : '#4f46e5',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '5px',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            marginBottom: '10px'
          }}
        >
          {isLoading ? 'Checking...' : 'Check API Health'}
        </button>
        {apiStatus && (
          <div style={{ 
            marginTop: '10px', 
            padding: '10px', 
            background: apiStatus.includes('✅') ? '#d4edda' : '#f8d7da',
            border: `1px solid ${apiStatus.includes('✅') ? '#c3e6cb' : '#f5c6cb'}`,
            borderRadius: '5px',
            fontFamily: 'monospace'
          }}>
            {apiStatus}
          </div>
        )}
      </div>
      
      <div style={{ marginTop: '20px' }}>
        <h3>🚀 Next Steps:</h3>
        <ul>
          <li>✅ React is working</li>
          <li>✅ Vite dev server is running</li>
          <li>✅ Environment variables loaded</li>
          <li>✅ API health check button added</li>
          <li>🔄 Ready for Firebase integration</li>
        </ul>
      </div>
    </div>
  )
}

export default App
