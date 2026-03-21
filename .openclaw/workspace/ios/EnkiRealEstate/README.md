# Enki Real Estate iOS App

A native iOS application for the Enki Real Estate AI platform, built with Swift and SwiftUI.

## Features

### Property Search
- Map-based search using MapKit
- List view with advanced filters
- Property detail view with image galleries
- Location-based property discovery

### AI Features
- **AI Property Valuation**: Get instant property value estimates using AI-powered comparable analysis
- **Lead Qualification**: Smart forms with AI-powered lead scoring
- **AI Chat**: Conversational interface for property queries and recommendations

### Agent Tools
- **Dashboard**: KPI metrics and real-time analytics
- **Lead Management**: Track and manage leads with status pipelines
- **Calendar Integration**: Schedule viewings and meetings

### User Features
- Favorites/Saved properties
- Push notifications
- User profiles with avatar upload

## Requirements

- iOS 16.0+
- Xcode 15.0+
- Swift 5.9+

## Project Structure

```
EnkiRealEstate/
├── Sources/
│   └── EnkiRealEstate/
│       ├── EnkiRealEstateApp.swift          # App entry point
│       ├── Models/
│       │   └── Models.swift                  # Data models
│       ├── Services/
│       │   ├── NetworkManager.swift          # API integration
│       │   └── KeychainManager.swift         # Secure storage
│       ├── Utils/
│       │   └── Theme.swift                   # UI theme/colors
│       └── Views/
│           ├── ContentView.swift             # Main tab view
│           ├── Auth/
│           │   └── AuthView.swift            # Login/Register
│           ├── Home/
│           │   └── HomeView.swift            # Home dashboard
│           ├── Search/
│           │   └── SearchView.swift          # Property search
│           ├── Property/
│           │   └── PropertyDetailView.swift  # Property details
│           ├── AI/
│           │   └── AIFeaturesView.swift      # AI chat & valuation
│           ├── Agent/
│           │   └── AgentToolsView.swift      # Agent dashboard
│           ├── Favorites/
│           │   └── FavoritesView.swift       # Saved properties
│           └── Profile/
│               └── ProfileView.swift         # User profile
├── Info.plist
└── Package.swift
```

## Setup

1. **Clone the project**
   ```bash
   cd ios/EnkiRealEstate
   ```

2. **Open in Xcode**
   ```bash
   open EnkiRealEstate.xcodeproj
   ```

3. **Configure API Endpoint**
   Update `NetworkManager.swift` with your backend URL:
   ```swift
   private let baseURL = "https://api.enkirealestate.com/v1"
   ```

4. **Build and Run**
   Select a simulator or connected device and press Cmd+R

## API Integration

The app connects to a FastAPI backend with JWT authentication:

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/refresh` - Token refresh

### Properties
- `GET /properties/search` - Search properties
- `GET /properties/{id}` - Get property details
- `GET /properties/nearby` - Nearby properties

### User
- `GET /users/me` - Get profile
- `PUT /users/me` - Update profile
- `GET /users/me/favorites` - Get favorites
- `POST /users/me/favorites` - Add favorite
- `DELETE /users/me/favorites/{id}` - Remove favorite

### AI Features
- `POST /ai/valuation` - Property valuation
- `POST /ai/chat` - AI chat
- `POST /leads/qualify` - Lead qualification

### Agent
- `GET /agents/dashboard` - Dashboard data
- `GET /leads` - Get leads
- `PATCH /leads/{id}/status` - Update lead status

## Offline Support

The app includes offline data caching:
- Network monitoring with `NWPathMonitor`
- Offline banner indicator
- Cached property data for offline viewing

## Architecture

- **MVVM**: Model-View-ViewModel pattern
- **SwiftUI**: Declarative UI framework
- **Combine**: Reactive programming for state management
- **JWT**: Secure token-based authentication
- **Keychain**: Secure credential storage

## Design

- Follows Apple Human Interface Guidelines
- Supports Dark Mode
- Responsive iPad split-view support
- Dynamic Type support
- Accessibility features

## License

© 2026 Enki Real Estate. All rights reserved.