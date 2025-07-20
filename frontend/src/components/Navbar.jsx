import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

function Navbar() {
  const location = useLocation()
  const { user, logout } = useAuth()

  const isActive = (path) => location.pathname === path

  return (
    <nav className="bg-indigo-600 shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="text-white text-xl font-bold">
            🎓 Sahayak AI
          </Link>
          
          <div className="hidden md:flex space-x-4">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/') 
                  ? 'bg-indigo-700 text-white' 
                  : 'text-indigo-100 hover:bg-indigo-500'
              }`}
            >
              Home
            </Link>
            
            {user && (
              <>
                <Link
                  to="/dashboard"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    isActive('/dashboard') 
                      ? 'bg-indigo-700 text-white' 
                      : 'text-indigo-100 hover:bg-indigo-500'
                  }`}
                >
                  Dashboard
                </Link>
                
                <Link
                  to="/lesson-plan"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    isActive('/lesson-plan') 
                      ? 'bg-indigo-700 text-white' 
                      : 'text-indigo-100 hover:bg-indigo-500'
                  }`}
                >
                  Lesson Plans
                </Link>
                
                <Link
                  to="/settings"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    isActive('/settings') 
                      ? 'bg-indigo-700 text-white' 
                      : 'text-indigo-100 hover:bg-indigo-500'
                  }`}
                >
                  Settings
                </Link>
              </>
            )}
          </div>

          <div className="flex items-center space-x-4">
            {user ? (
              <div className="flex items-center space-x-2">
                <span className="text-white text-sm">
                  Welcome, {user.displayName || user.email}
                </span>
                <button
                  onClick={logout}
                  className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
                >
                  Logout
                </button>
              </div>
            ) : (
              <button className="bg-white text-indigo-600 px-4 py-2 rounded font-medium hover:bg-gray-100">
                Login
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
