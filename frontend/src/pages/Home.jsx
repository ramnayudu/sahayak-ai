import PWAStatus from '../components/PWAStatus'

function Home() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center py-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to Sahayak AI
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Your AI-powered assistant for multi-grade classroom management
        </p>
        
        <div className="grid md:grid-cols-2 gap-8 mt-12">
          {/* Online Mode */}
          <div className="bg-white p-6 rounded-lg shadow-md border border-blue-200">
            <div className="text-blue-600 text-3xl mb-4">🌐</div>
            <h3 className="text-xl font-semibold mb-2">Sahayak Setu</h3>
            <p className="text-gray-600 mb-4">
              Online mode powered by Gemini and Gemma via Vertex AI
            </p>
            <ul className="text-sm text-gray-500 space-y-1">
              <li>• Advanced AI capabilities</li>
              <li>• Real-time collaboration</li>
              <li>• Cloud-based storage</li>
              <li>• Latest model updates</li>
            </ul>
            <button className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
              Use Online Mode
            </button>
          </div>

          {/* Offline Mode */}
          <div className="bg-white p-6 rounded-lg shadow-md border border-green-200">
            <div className="text-green-600 text-3xl mb-4">🏠</div>
            <h3 className="text-xl font-semibold mb-2">Sahayak Nivaas</h3>
            <p className="text-gray-600 mb-4">
              Offline mode using quantized Gemma models via Ollama
            </p>
            <ul className="text-sm text-gray-500 space-y-1">
              <li>• Works without internet</li>
              <li>• Privacy-focused</li>
              <li>• Local data storage</li>
              <li>• Faster response times</li>
            </ul>
            <button className="mt-4 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
              Use Offline Mode
            </button>
          </div>
        </div>

        {/* Features */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold text-gray-900 mb-8">Key Features</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-4xl mb-3">📚</div>
              <h3 className="font-semibold mb-2">Lesson Planning</h3>
              <p className="text-gray-600 text-sm">
                Generate age-appropriate lesson plans for multiple grade levels
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-3">📊</div>
              <h3 className="font-semibold mb-2">Progress Tracking</h3>
              <p className="text-gray-600 text-sm">
                Monitor student progress and adapt teaching strategies
              </p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-3">🎨</div>
              <h3 className="font-semibold mb-2">Visual Aids</h3>
              <p className="text-gray-600 text-sm">
                Create engaging visual content and interactive materials
              </p>
            </div>
          </div>
        </div>
        
        {/* PWA Status Section */}
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            Progressive Web App Status
          </h2>
          <div className="max-w-md mx-auto">
            <PWAStatus />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
