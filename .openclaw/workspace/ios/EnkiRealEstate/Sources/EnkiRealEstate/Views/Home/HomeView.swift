import SwiftUI

struct HomeView: View {
    @StateObject private var viewModel = HomeViewModel()
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Welcome header
                    WelcomeHeader(userName: appState.user?.firstName ?? "Guest")
                    
                    // Quick actions
                    QuickActionsGrid()
                    
                    // AI Assistant section
                    AIAssistantCard()
                    
                    // Featured properties
                    FeaturedPropertiesSection(properties: viewModel.featuredProperties)
                    
                    // Recent activity (for agents)
                    if appState.user?.role == .agent {
                        AgentActivitySection()
                    }
                    
                    // Market insights
                    MarketInsightsSection()
                }
                .padding(.vertical)
            }
            .navigationTitle("Home")
            .refreshable {
                await viewModel.loadData()
            }
        }
    }
}

struct WelcomeHeader: View {
    let userName: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Good \(timeOfDay),")
                .font(.title3)
                .foregroundColor(.secondary)
            
            Text(userName)
                .font(.largeTitle.weight(.bold))
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(.horizontal)
    }
    
    private var timeOfDay: String {
        let hour = Calendar.current.component(.hour, from: Date())
        switch hour {
        case 5..<12: return "morning"
        case 12..<17: return "afternoon"
        case 17..<21: return "evening"
        default: return "night"
        }
    }
}

struct QuickActionsGrid: View {
    var body: some View {
        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 16) {
            QuickActionButton(
                title: "Search Properties",
                icon: "magnifyingglass",
                color: .blue
            )
            
            QuickActionButton(
                title: "AI Valuation",
                icon: "chart.line.uptrend.xyaxis",
                color: .green
            )
            
            QuickActionButton(
                title: "Saved Homes",
                icon: "heart.fill",
                color: .red
            )
            
            QuickActionButton(
                title: "AI Chat",
                icon: "message.fill",
                color: .purple
            )
        }
        .padding(.horizontal)
    }
}

struct QuickActionButton: View {
    let title: String
    let icon: String
    let color: Color
    
    var body: some View {
        Button(action: {}) {
            VStack(spacing: 12) {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                
                Text(title)
                    .font(.subheadline.weight(.medium))
                    .foregroundColor(.primary)
                    .multilineTextAlignment(.center)
            }
            .frame(maxWidth: .infinity, minHeight: 100)
            .background(Color(.secondarySystemBackground))
            .cornerRadius(16)
        }
    }
}

struct AIAssistantCard: View {
    @State private var showingChat = false
    
    var body: some View {
        Button(action: { showingChat = true }) {
            HStack(spacing: 16) {
                Image(systemName: "brain.head.profile")
                    .font(.system(size: 40))
                    .foregroundColor(.enkiPrimary)
                
                VStack(alignment: .leading, spacing: 4) {
                    Text("Ask Enki AI")
                        .font(.headline)
                    
                    Text("Get personalized property recommendations and answers")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .lineLimit(2)
                }
                
                Spacer()
                
                Image(systemName: "chevron.right")
                    .foregroundColor(.secondary)
            }
            .padding()
            .background(
                LinearGradient(
                    colors: [.enkiPrimary.opacity(0.1), .enkiSecondary.opacity(0.1)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            )
            .cornerRadius(16)
            .overlay(
                RoundedRectangle(cornerRadius: 16)
                    .stroke(Color.enkiPrimary.opacity(0.2), lineWidth: 1)
            )
        }
        .buttonStyle(PlainButtonStyle())
        .padding(.horizontal)
        .sheet(isPresented: $showingChat) {
            AIChatView()
        }
    }
}

struct FeaturedPropertiesSection: View {
    let properties: [Property]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Text("Featured Properties")
                    .font(.title2.weight(.bold))
                
                Spacer()
                
                NavigationLink("See All") {
                    SearchView()
                }
                .font(.subheadline)
                .foregroundColor(.enkiPrimary)
            }
            .padding(.horizontal)
            
            if properties.isEmpty {
                ProgressView()
                    .frame(maxWidth: .infinity, minHeight: 200)
            } else {
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 16) {
                        ForEach(properties) { property in
                            NavigationLink(destination: PropertyDetailView(property: property)) {
                                PropertyCard(property: property)
                            }
                            .buttonStyle(PlainButtonStyle())
                        }
                    }
                    .padding(.horizontal)
                }
            }
        }
    }
}

struct PropertyCard: View {
    let property: Property
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Property image
            ZStack(alignment: .topTrailing) {
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color.gray.opacity(0.2))
                    .frame(width: 280, height: 180)
                
                // Placeholder for actual image
                Image(systemName: "photo")
                    .font(.largeTitle)
                    .foregroundColor(.gray)
                    .frame(width: 280, height: 180)
                
                // Favorite button
                Button(action: {}) {
                    Image(systemName: "heart")
                        .font(.title3)
                        .foregroundColor(.white)
                        .padding(8)
                        .background(.ultraThinMaterial)
                        .clipShape(Circle())
                }
                .padding(8)
            }
            
            // Property info
            VStack(alignment: .leading, spacing: 8) {
                Text(property.formattedPrice)
                    .font(.title3.weight(.bold))
                
                Text(property.address.fullAddress)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .lineLimit(1)
                
                HStack(spacing: 16) {
                    PropertyFeature(icon: "bed.double.fill", value: "\(property.bedrooms)")
                    PropertyFeature(icon: "shower.fill", value: "\(property.bathrooms)")
                    PropertyFeature(icon: "ruler.fill", value: "\(Int(property.squareFeet))")
                }
            }
            .padding(12)
        }
        .background(Color(.secondarySystemBackground))
        .cornerRadius(12)
    }
}

struct PropertyFeature: View {
    let icon: String
    let value: String
    
    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: icon)
                .font(.caption)
                .foregroundColor(.secondary)
            Text(value)
                .font(.caption.weight(.medium))
        }
    }
}

struct AgentActivitySection: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Recent Activity")
                .font(.title2.weight(.bold))
                .padding(.horizontal)
            
            VStack(spacing: 12) {
                ActivityItemView(
                    icon: "person.badge.plus",
                    title: "New Lead",
                    description: "Sarah Johnson requested a viewing",
                    time: "2 min ago"
                )
                
                ActivityItemView(
                    icon: "envelope.fill",
                    title: "Message Received",
                    description: "Reply from property inquiry #2341",
                    time: "15 min ago"
                )
                
                ActivityItemView(
                    icon: "checkmark.circle.fill",
                    title: "Deal Closed",
                    description: "123 Main St - $850,000",
                    time: "1 hour ago"
                )
            }
            .padding(.horizontal)
        }
    }
}

struct ActivityItemView: View {
    let icon: String
    let title: String
    let description: String
    let time: String
    
    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.title3)
                .foregroundColor(.enkiPrimary)
                .frame(width: 40, height: 40)
                .background(Color.enkiPrimary.opacity(0.1))
                .cornerRadius(10)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.subheadline.weight(.semibold))
                Text(description)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Text(time)
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(12)
    }
}

struct MarketInsightsSection: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Market Insights")
                .font(.title2.weight(.bold))
                .padding(.horizontal)
            
            HStack(spacing: 16) {
                MarketStatCard(
                    title: "Avg. Price",
                    value: "$685K",
                    trend: "+5.2%",
                    isPositive: true
                )
                
                MarketStatCard(
                    title: "Days on Market",
                    value: "24",
                    trend: "-3 days",
                    isPositive: true
                )
            }
            .padding(.horizontal)
        }
    }
}

struct MarketStatCard: View {
    let title: String
    let value: String
    let trend: String
    let isPositive: Bool
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
            
            Text(value)
                .font(.title2.weight(.bold))
            
            Text(trend)
                .font(.caption.weight(.medium))
                .foregroundColor(isPositive ? .green : .red)
                .padding(.horizontal, 8)
                .padding(.vertical, 4)
                .background((isPositive ? Color.green : Color.red).opacity(0.1))
                .cornerRadius(6)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(12)
    }
}

@MainActor
class HomeViewModel: ObservableObject {
    @Published var featuredProperties: [Property] = []
    @Published var isLoading = false
    
    init() {
        Task {
            await loadData()
        }
    }
    
    func loadData() async {
        isLoading = true
        
        do {
            let filters = SearchFilters(
                minPrice: nil,
                maxPrice: nil,
                bedrooms: nil,
                bathrooms: nil,
                propertyTypes: [],
                listingType: nil,
                location: nil,
                radius: nil
            )
            let result = try await NetworkManager.shared.searchProperties(filters: filters, pageSize: 5)
            featuredProperties = result.properties
        } catch {
            print("Failed to load featured properties: \(error)")
        }
        
        isLoading = false
    }
}