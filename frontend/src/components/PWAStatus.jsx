import { useState, useEffect } from 'react'

export default function PWAStatus() {
  const [isInstallable, setIsInstallable] = useState(false)
  const [isInstalled, setIsInstalled] = useState(false)
  const [swStatus, setSWStatus] = useState('checking')
  const [deferredPrompt, setDeferredPrompt] = useState(null)

  useEffect(() => {
    // Check if app is already installed
    if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true)
    }

    // Check service worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.getRegistration()
        .then(registration => {
          setSWStatus(registration ? 'active' : 'inactive')
        })
        .catch(() => setSWStatus('error'))
    } else {
      setSWStatus('unsupported')
    }

    // Listen for install prompt
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault()
      setDeferredPrompt(e)
      setIsInstallable(true)
    }

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
    }
  }, [])

  const handleInstallClick = async () => {
    if (!deferredPrompt) return

    deferredPrompt.prompt()
    const { outcome } = await deferredPrompt.userChoice
    
    if (outcome === 'accepted') {
      setIsInstalled(true)
    }
    
    setDeferredPrompt(null)
    setIsInstallable(false)
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'text-green-600'
      case 'inactive': return 'text-yellow-600'
      case 'error': return 'text-red-600'
      case 'unsupported': return 'text-gray-600'
      default: return 'text-blue-600'
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return '✅ Service Worker Active'
      case 'inactive': return '⚠️ Service Worker Inactive'
      case 'error': return '❌ Service Worker Error'
      case 'unsupported': return '❌ Service Worker Unsupported'
      default: return '🔄 Checking Service Worker...'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-4 border">
      <h3 className="text-lg font-semibold mb-3 flex items-center">
        📱 PWA Status
      </h3>
      
      <div className="space-y-2 text-sm">
        {/* Installation Status */}
        <div className="flex items-center justify-between">
          <span>Installation:</span>
          <span className={isInstalled ? 'text-green-600' : 'text-gray-600'}>
            {isInstalled ? '✅ Installed' : '📱 Web App'}
          </span>
        </div>

        {/* Service Worker Status */}
        <div className="flex items-center justify-between">
          <span>Service Worker:</span>
          <span className={getStatusColor(swStatus)}>
            {getStatusText(swStatus)}
          </span>
        </div>

        {/* HTTPS Status */}
        <div className="flex items-center justify-between">
          <span>Secure Context:</span>
          <span className={location.protocol === 'https:' || location.hostname === 'localhost' ? 'text-green-600' : 'text-red-600'}>
            {location.protocol === 'https:' || location.hostname === 'localhost' ? '✅ Secure' : '❌ Insecure'}
          </span>
        </div>

        {/* Offline Capability */}
        <div className="flex items-center justify-between">
          <span>Offline Ready:</span>
          <span className={swStatus === 'active' ? 'text-green-600' : 'text-yellow-600'}>
            {swStatus === 'active' ? '✅ Yes' : '⚠️ Limited'}
          </span>
        </div>
      </div>

      {/* Install Button */}
      {isInstallable && !isInstalled && (
        <button
          onClick={handleInstallClick}
          className="mt-3 w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
        >
          📱 Install App
        </button>
      )}

      {/* PWA Validation Link */}
      <div className="mt-3 pt-3 border-t">
        <a
          href="/pwa-validation.html"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 hover:text-blue-800 text-sm underline"
        >
          🔍 Open PWA Validation Dashboard
        </a>
      </div>
    </div>
  )
}
