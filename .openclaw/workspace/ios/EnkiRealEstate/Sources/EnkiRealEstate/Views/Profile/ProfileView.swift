import SwiftUI
import PhotosUI

struct ProfileView: View {
    @EnvironmentObject var appState: AppState
    @StateObject private var viewModel = ProfileViewModel()
    @State private var showingLogoutConfirmation = false
    @State private var showingImagePicker = false
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Profile header
                    ProfileHeader(user: appState.user)
                    
                    // Stats (for agents)
                    if appState.user?.role == .agent {
                        AgentStatsView()
                    }
                    
                    // Menu sections
                    ProfileMenuSection(title: "Account", items: [
                        MenuItem(icon: "person", title: "Edit Profile", action: {}),
                        MenuItem(icon: "creditcard", title: "Payment Methods", action: {}),
                        MenuItem(icon: "bell", title: "Notifications", action: {}),
                    ])
                    
                    ProfileMenuSection(title: "Preferences", items: [
                        MenuItem(icon: "moon", title: "Dark Mode", isToggle: true),
                        MenuItem(icon: "globe", title: "Language", action: {}),
                        MenuItem(icon: "location", title: "Location Settings", action: {}),
                    ])
                    
                    ProfileMenuSection(title: "Support", items: [
                        MenuItem(icon: "questionmark.circle", title: "Help Center", action: {}),
                        MenuItem(icon: "message", title: "Contact Support", action: {}),
                        MenuItem(icon: "star", title: "Rate the App", action: {}),
                    ])
                    
                    // Logout button
                    Button(action: { showingLogoutConfirmation = true }) {
                        HStack {
                            Image(systemName: "arrow.left.square.fill")
                            Text("Log Out")
                        }
                        .foregroundColor(.red)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.red.opacity(0.1))
                        .cornerRadius(12)
                    }
                    .padding(.horizontal)
                    
                    // Version info
                    Text("Enki Real Estate v1.0.0")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .padding(.vertical)
            }
            .navigationTitle("Profile")
            .confirmationDialog("Log Out", isPresented: $showingLogoutConfirmation) {
                Button("Log Out", role: .destructive) {
                    appState.logout()
                }
                Button("Cancel", role: .cancel) {}
            } message: {
                Text("Are you sure you want to log out?")
            }
        }
    }
}

struct ProfileHeader: View {
    let user: User?
    @State private var showingImagePicker = false
    @State private var selectedItem: PhotosPickerItem?
    
    var body: some View {
        VStack(spacing: 16) {
            // Avatar
            PhotosPicker(selection: $selectedItem, matching: .images) {
                ZStack {
                    Circle()
                        .fill(Color.enkiPrimary.opacity(0.1))
                        .frame(width: 100, height: 100)
                    
                    if let avatar = user?.avatar, let url = URL(string: avatar) {
                        AsyncImage(url: url) { image in
                            image.resizable().aspectRatio(contentMode: .fill)
                        } placeholder: {
                            Text(initials)
                                .font(.title.weight(.bold))
                                .foregroundColor(.enkiPrimary)
                        }
                        .frame(width: 100, height: 100)
                        .clipShape(Circle())
                    } else {
                        Text(initials)
                            .font(.title.weight(.bold))
                            .foregroundColor(.enkiPrimary)
                    }
                    
                    // Edit indicator
                    Circle()
                        .fill(.ultraThinMaterial)
                        .frame(width: 32, height: 32)
                        .overlay(
                            Image(systemName: "camera")
                                .font(.caption)
                                .foregroundColor(.primary)
                        )
                        .offset(x: 35, y: 35)
                }
            }
            
            // User info
            VStack(spacing: 4) {
                Text(user?.fullName ?? "Guest")
                    .font(.title2.weight(.bold))
                
                Text(user?.email ?? "")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                
                if let role = user?.role {
                    Text(role.rawValue.capitalized)
                        .font(.caption.weight(.medium))
                        .padding(.horizontal, 12)
                        .padding(.vertical, 4)
                        .background(Color.enkiPrimary.opacity(0.1))
                        .foregroundColor(.enkiPrimary)
                        .cornerRadius(12)
                }
            }
        }
        .padding()
        .frame(maxWidth: .infinity)
        .background(Color(.secondarySystemBackground))
        .cornerRadius(16)
        .padding(.horizontal)
    }
    
    private var initials: String {
        guard let user = user else { return "?" }
        let first = String(user.firstName.prefix(1))
        let last = String(user.lastName.prefix(1))
        return first + last
    }
}

struct AgentStatsView: View {
    var body: some View {
        HStack(spacing: 0) {
            StatColumn(value: "24", label: "Listings")
            Divider()
            StatColumn(value: "156", label: "Sales")
            Divider()
            StatColumn(value: "4.9", label: "Rating")
        }
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(16)
        .padding(.horizontal)
    }
}

struct StatColumn: View {
    let value: String
    let label: String
    
    var body: some View {
        VStack(spacing: 4) {
            Text(value)
                .font(.title2.weight(.bold))
            Text(label)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
    }
}

struct ProfileMenuSection: View {
    let title: String
    let items: [MenuItem]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text(title)
                .font(.headline)
                .padding(.horizontal)
            
            VStack(spacing: 0) {
                ForEach(items.indices, id: \.self) { index in
                    MenuRow(item: items[index])
                    if index < items.count - 1 {
                        Divider()
                            .padding(.leading, 50)
                    }
                }
            }
            .background(Color(.secondarySystemBackground))
            .cornerRadius(12)
            .padding(.horizontal)
        }
    }
}

struct MenuItem {
    let icon: String
    let title: String
    var action: (() -> Void)? = nil
    var isToggle: Bool = false
}

struct MenuRow: View {
    let item: MenuItem
    @State private var isOn = false
    
    var body: some View {
        if item.isToggle {
            Toggle(isOn: $isOn) {
                Label(item.title, systemImage: item.icon)
            }
            .padding()
        } else if let action = item.action {
            Button(action: action) {
                HStack {
                    Image(systemName: item.icon)
                        .font(.body)
                        .foregroundColor(.enkiPrimary)
                        .frame(width: 30)
                    
                    Text(item.title)
                        .foregroundColor(.primary)
                    
                    Spacer()
                    
                    Image(systemName: "chevron.right")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                .padding()
            }
        } else {
            HStack {
                Image(systemName: item.icon)
                    .font(.body)
                    .foregroundColor(.enkiPrimary)
                    .frame(width: 30)
                
                Text(item.title)
                
                Spacer()
            }
            .padding()
        }
    }
}

@MainActor
class ProfileViewModel: ObservableObject {
    // Profile-specific view logic
}
