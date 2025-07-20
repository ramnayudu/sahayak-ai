import React from 'react'

function App() {
  console.log('App component is rendering')
  console.log('Firebase API Key:', import.meta.env.VITE_FIREBASE_API_KEY)
  console.log('All env vars:', import.meta.env)
  
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>🎉 AI Sahayak Frontend is Working!</h1>
      <p>If you see this, React is loading properly.</p>
      <div style={{ marginTop: '20px', padding: '10px', background: '#f0f0f0' }}>
        <h3>Environment Check:</h3>
        <p>Node ENV: {import.meta.env.MODE}</p>
        <p>Firebase API Key: {import.meta.env.VITE_FIREBASE_API_KEY ? '✅ Set' : '❌ Missing'}</p>
        <p>Project ID: {import.meta.env.VITE_FIREBASE_PROJECT_ID || 'Not set'}</p>
      </div>
      <div style={{ marginTop: '20px' }}>
        <h3>🚀 Next Steps:</h3>
        <ul>
          <li>✅ React is working</li>
          <li>✅ Vite dev server is running</li>
          <li>✅ Environment variables loaded</li>
          <li>🔄 Ready for Firebase integration</li>
        </ul>
      </div>
    </div>
  )
}

export default App


