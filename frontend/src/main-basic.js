console.log('Starting React app...')

const rootElement = document.getElementById('root')
console.log('Root element:', rootElement)

if (rootElement) {
  rootElement.innerHTML = `
    <div style="padding: 20px; font-family: Arial;">
      <h1 style="color: green;">✅ AI Sahayak is Working!</h1>
      <p>This is a basic HTML test without React dependencies.</p>
      <div style="background: #f0f0f0; padding: 10px; margin: 10px 0;">
        <h3>Status:</h3>
        <ul>
          <li>✅ HTML is loading</li>
          <li>✅ JavaScript is running</li>
          <li>✅ Root element found</li>
          <li>🔄 Ready for React</li>
        </ul>
      </div>
    </div>
  `
} else {
  console.error('Root element not found!')
}
