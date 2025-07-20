function Settings() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-2">Configure your Sahayak AI experience</p>
      </div>

      <div className="space-y-6">
        {/* AI Mode Settings */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">AI Mode Configuration</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Preferred Mode
              </label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input type="radio" name="mode" className="mr-3" defaultChecked />
                  <div>
                    <div className="font-medium">Sahayak Setu (Online)</div>
                    <div className="text-sm text-gray-600">Uses Vertex AI with Gemini/Gemma models</div>
                  </div>
                </label>
                <label className="flex items-center">
                  <input type="radio" name="mode" className="mr-3" />
                  <div>
                    <div className="font-medium">Sahayak Nivaas (Offline)</div>
                    <div className="text-sm text-gray-600">Uses local Ollama with quantized models</div>
                  </div>
                </label>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Model Selection (Online Mode)
              </label>
              <select className="w-full border border-gray-300 rounded-md px-3 py-2">
                <option>Gemini Pro</option>
                <option>Gemma 7B</option>
                <option>Gemma 2B</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Offline Model (Offline Mode)
              </label>
              <select className="w-full border border-gray-300 rounded-md px-3 py-2">
                <option>Gemma 7B Quantized</option>
                <option>Gemma 2B Quantized</option>
              </select>
            </div>
          </div>
        </div>

        {/* Language Settings */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Language Preferences</h2>
          
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Primary Language
              </label>
              <select className="w-full border border-gray-300 rounded-md px-3 py-2">
                <option>English</option>
                <option>Hindi</option>
                <option>Marathi</option>
                <option>Tamil</option>
                <option>Telugu</option>
                <option>Bengali</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Secondary Language
              </label>
              <select className="w-full border border-gray-300 rounded-md px-3 py-2">
                <option>None</option>
                <option>English</option>
                <option>Hindi</option>
                <option>Local Language</option>
              </select>
            </div>
          </div>
        </div>

        {/* Classroom Settings */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Classroom Configuration</h2>
          
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                School Name
              </label>
              <input
                type="text"
                placeholder="Enter your school name"
                className="w-full border border-gray-300 rounded-md px-3 py-2"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Grade Levels You Teach
              </label>
              <div className="flex flex-wrap gap-2 mt-2">
                {[1, 2, 3, 4, 5, 6, 7, 8].map(grade => (
                  <label key={grade} className="flex items-center">
                    <input type="checkbox" className="mr-1" />
                    <span className="text-sm">Grade {grade}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Average Class Size
            </label>
            <select className="w-full md:w-1/3 border border-gray-300 rounded-md px-3 py-2">
              <option>1-10 students</option>
              <option>11-20 students</option>
              <option>21-30 students</option>
              <option>31-40 students</option>
              <option>40+ students</option>
            </select>
          </div>
        </div>

        {/* Data & Privacy */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Data & Privacy</h2>
          
          <div className="space-y-4">
            <label className="flex items-center">
              <input type="checkbox" className="mr-3" defaultChecked />
              <div>
                <div className="font-medium">Enable offline data sync</div>
                <div className="text-sm text-gray-600">Sync data when connection is available</div>
              </div>
            </label>
            
            <label className="flex items-center">
              <input type="checkbox" className="mr-3" defaultChecked />
              <div>
                <div className="font-medium">Anonymous usage analytics</div>
                <div className="text-sm text-gray-600">Help improve Sahayak AI with anonymous data</div>
              </div>
            </label>
            
            <label className="flex items-center">
              <input type="checkbox" className="mr-3" />
              <div>
                <div className="font-medium">Share lesson plans with community</div>
                <div className="text-sm text-gray-600">Help other teachers with your successful lesson plans</div>
              </div>
            </label>
          </div>
        </div>

        {/* Save Settings */}
        <div className="flex justify-end space-x-4">
          <button className="px-6 py-2 border border-gray-300 rounded-md hover:bg-gray-50">
            Reset to Defaults
          </button>
          <button className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
            Save Settings
          </button>
        </div>
      </div>
    </div>
  )
}

export default Settings
