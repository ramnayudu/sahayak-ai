function LessonPlan() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">AI Lesson Plan Generator</h1>
        <p className="text-gray-600 mt-2">Create customized lesson plans for multi-grade classrooms</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <form className="space-y-6">
          {/* Subject Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Subject
            </label>
            <select className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option>Mathematics</option>
              <option>Science</option>
              <option>English</option>
              <option>Hindi</option>
              <option>Social Studies</option>
              <option>Environmental Studies</option>
            </select>
          </div>

          {/* Grade Levels */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Grade Levels (Select multiple)
            </label>
            <div className="grid grid-cols-3 gap-2">
              {[1, 2, 3, 4, 5, 6, 7, 8].map(grade => (
                <label key={grade} className="flex items-center">
                  <input type="checkbox" className="mr-2" />
                  <span className="text-sm">Grade {grade}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Topic */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Topic/Chapter
            </label>
            <input
              type="text"
              placeholder="e.g., Fractions, Photosynthesis, Grammar"
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          {/* Duration */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Class Duration (minutes)
            </label>
            <select className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option>30 minutes</option>
              <option>45 minutes</option>
              <option>60 minutes</option>
              <option>90 minutes</option>
            </select>
          </div>

          {/* Learning Objectives */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Learning Objectives (Optional)
            </label>
            <textarea
              rows="3"
              placeholder="What should students learn from this lesson?"
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            ></textarea>
          </div>

          {/* Additional Requirements */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Special Requirements
            </label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input type="checkbox" className="mr-2" />
                <span className="text-sm">Include visual aids</span>
              </label>
              <label className="flex items-center">
                <input type="checkbox" className="mr-2" />
                <span className="text-sm">Hands-on activities</span>
              </label>
              <label className="flex items-center">
                <input type="checkbox" className="mr-2" />
                <span className="text-sm">Group work</span>
              </label>
              <label className="flex items-center">
                <input type="checkbox" className="mr-2" />
                <span className="text-sm">Assessment questions</span>
              </label>
            </div>
          </div>

          {/* Generate Button */}
          <div className="flex space-x-4">
            <button
              type="submit"
              className="flex-1 bg-indigo-600 text-white py-3 px-6 rounded-md hover:bg-indigo-700 font-medium"
            >
              🤖 Generate Lesson Plan
            </button>
            <button
              type="button"
              className="px-6 py-3 border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Save as Template
            </button>
          </div>
        </form>
      </div>

      {/* Generated Lesson Plan Preview */}
      <div className="mt-8 bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Generated Lesson Plan Preview</h2>
        <div className="text-center text-gray-500 py-8">
          <div className="text-4xl mb-4">📄</div>
          <p>Your AI-generated lesson plan will appear here</p>
          <p className="text-sm mt-2">Fill out the form above and click "Generate Lesson Plan"</p>
        </div>
      </div>
    </div>
  )
}

export default LessonPlan
