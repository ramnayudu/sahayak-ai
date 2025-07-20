function Dashboard() {
  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Teacher Dashboard</h1>
        <p className="text-gray-600 mt-2">Manage your multi-grade classroom efficiently</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Quick Stats */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Classroom Overview</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded">
                <div className="text-2xl font-bold text-blue-600">24</div>
                <div className="text-sm text-gray-600">Total Students</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded">
                <div className="text-2xl font-bold text-green-600">3</div>
                <div className="text-sm text-gray-600">Grade Levels</div>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded">
                <div className="text-2xl font-bold text-yellow-600">12</div>
                <div className="text-sm text-gray-600">Lesson Plans</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded">
                <div className="text-2xl font-bold text-purple-600">89%</div>
                <div className="text-sm text-gray-600">Avg. Progress</div>
              </div>
            </div>
          </div>

          {/* Recent Activities */}
          <div className="bg-white rounded-lg shadow p-6 mt-6">
            <h2 className="text-xl font-semibold mb-4">Recent Activities</h2>
            <div className="space-y-3">
              <div className="flex items-center p-3 bg-gray-50 rounded">
                <div className="text-green-600 mr-3">✅</div>
                <div>
                  <div className="font-medium">Math lesson for Grade 3 completed</div>
                  <div className="text-sm text-gray-600">2 hours ago</div>
                </div>
              </div>
              <div className="flex items-center p-3 bg-gray-50 rounded">
                <div className="text-blue-600 mr-3">📝</div>
                <div>
                  <div className="font-medium">Science worksheet generated for Grade 5</div>
                  <div className="text-sm text-gray-600">4 hours ago</div>
                </div>
              </div>
              <div className="flex items-center p-3 bg-gray-50 rounded">
                <div className="text-yellow-600 mr-3">⭐</div>
                <div>
                  <div className="font-medium">Student assessment completed</div>
                  <div className="text-sm text-gray-600">1 day ago</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <button className="w-full bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700">
                Create Lesson Plan
              </button>
              <button className="w-full bg-green-600 text-white py-2 px-4 rounded hover:bg-green-700">
                Generate Worksheet
              </button>
              <button className="w-full bg-yellow-600 text-white py-2 px-4 rounded hover:bg-yellow-700">
                Student Assessment
              </button>
              <button className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700">
                Visual Aids
              </button>
            </div>
          </div>

          {/* Mode Status */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Connection Status</h2>
            <div className="flex items-center mb-3">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
              <span className="text-sm">Online - Sahayak Setu</span>
            </div>
            <p className="text-xs text-gray-600">
              Connected to Vertex AI. Switch to offline mode if needed.
            </p>
            <button className="mt-3 text-sm text-indigo-600 hover:text-indigo-800">
              Switch to Offline Mode
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
