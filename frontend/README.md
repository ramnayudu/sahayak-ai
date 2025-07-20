# Sahayak Frontend

React PWA application for the Sahayak AI multi-grade classroom assistant.

## Features

- **Progressive Web App (PWA)** - Works offline and can be installed on mobile devices
- **Dual Mode Support** - Online (Vertex AI) and Offline (Ollama) modes
- **Firebase Integration** - Authentication, Firestore, and hosting
- **Responsive Design** - Optimized for mobile and desktop
- **Offline-First** - IndexedDB caching for seamless offline experience

## Tech Stack

- React 18
- Vite (build tool)
- React Router (navigation)
- Firebase (auth, storage, hosting)
- Workbox (PWA features)
- Tailwind CSS (styling)

## Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Firebase configuration
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

## PWA Features

- Service worker for offline functionality
- App manifest for installation
- Background sync for data
- Push notifications (coming soon)

## Firebase Setup

1. Create a new Firebase project
2. Enable Authentication with Email/Password
3. Create Firestore database
4. Enable Storage
5. Configure hosting (optional)
6. Update .env with your Firebase config

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Contributing

Please read the main project README for contribution guidelines.
