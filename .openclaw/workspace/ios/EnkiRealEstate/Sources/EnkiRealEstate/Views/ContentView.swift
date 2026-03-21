import SwiftUI

struct ContentView: View {
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        Group {
            if appState.isAuthenticated {
                MainTabView()
            } else {
                AuthView()
            }
        }
        .overlay(OfflineBanner())
    }
}

struct MainTabView: View {
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        TabView(selection: $appState.currentTab) {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house.fill")
                }
                .tag(AppState.Tab.home)
            
            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
                .tag(AppState.Tab.search)
            
            FavoritesView()
                .tabItem {
                    Label("Saved", systemImage: "heart.fill")
                }
                .tag(AppState.Tab.favorites)
            
            AgentToolsView()
                .tabItem {
                    Label("Tools", systemImage: "briefcase.fill")
                }
                .tag(AppState.Tab.tools)
            
            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person.fill")
                }
                .tag(AppState.Tab.profile)
        }
        .accentColor(.enkiPrimary)
    }
}

struct OfflineBanner: View {
    @EnvironmentObject var networkManager: NetworkManager
    
    var body: some View {
        VStack {
            if networkManager.isOffline {
                HStack {
                    Image(systemName: "wifi.slash")
                    Text("Offline Mode")
                        .font(.subheadline.weight(.medium))
                }
                .foregroundColor(.white)
                .padding(.vertical, 8)
                .padding(.horizontal, 16)
                .background(Color.orange)
                .cornerRadius(20)
                .padding(.top, 8)
                
                Spacer()
            }
        }
    }
}