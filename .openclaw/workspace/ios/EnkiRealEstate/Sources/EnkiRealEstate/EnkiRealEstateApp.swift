import SwiftUI

@main
struct EnkiRealEstateApp: App {
    @StateObject private var appState = AppState()
    @StateObject private var networkManager = NetworkManager.shared
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
                .environmentObject(networkManager)
        }
    }
}

class AppState: ObservableObject {
    @Published var isAuthenticated: Bool = false
    @Published var user: User?
    @Published var currentTab: Tab = .home
    @Published var isOffline: Bool = false
    
    enum Tab {
        case home
        case search
        case favorites
        case tools
        case profile
    }
    
    init() {
        checkAuthentication()
    }
    
    func checkAuthentication() {
        if let token = KeychainManager.shared.getToken() {
            isAuthenticated = true
            Task {
                await fetchUserProfile()
            }
        }
    }
    
    func logout() {
        KeychainManager.shared.deleteToken()
        user = nil
        isAuthenticated = false
    }
    
    @MainActor
    func fetchUserProfile() async {
        do {
            let profile = try await NetworkManager.shared.getUserProfile()
            self.user = profile
        } catch {
            print("Failed to fetch user: \(error)")
        }
    }
}