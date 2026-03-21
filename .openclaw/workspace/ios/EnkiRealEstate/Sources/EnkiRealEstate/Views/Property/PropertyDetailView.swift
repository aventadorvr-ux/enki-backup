import SwiftUI
import MapKit

struct PropertyDetailView: View {
    let property: Property
    @StateObject private var viewModel = PropertyDetailViewModel()
    @Environment(\\.dismiss) private var dismiss
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 0) {
                // Image gallery
                ImageGalleryView(images: property.images)
                    .frame(height: 300)
                
                // Property info
                VStack(alignment: .leading, spacing: 16) {
                    // Price and status
                    HStack {
                        Text(property.formattedPrice)
                            .font(.title.weight(.bold))
                        
                        Spacer()
                        
                        StatusBadge(status: property.status)
                    }
                    
                    // Address
                    Text(property.address.fullAddress)
                        .font(.title3)
                        .foregroundColor(.secondary)
                    
                    // Key stats
                    HStack(spacing: 24) {
                        StatItem(icon: "bed.double.fill", value: "\(property.bedrooms)", label: "Beds")
                        StatItem(icon: "shower.fill", value: "\(property.bathrooms)", label: "Baths")
                        StatItem(icon: "ruler.fill", value: "\(Int(property.squareFeet))", label: "Sq Ft")
                        if let year = property.yearBuilt {
                            StatItem(icon: "calendar", value: "\(year)", label: "Built")
                        }
                    }
                    .padding(.vertical, 8)
                }
                .padding()
                
                Divider()
                    .padding(.horizontal)
                
                // Description
                VStack(alignment: .leading, spacing: 8) {
                    Text("About this property")
                        .font(.headline)
                    
                    Text(property.description)
                        .font(.body)
                        .foregroundColor(.secondary)
                }
                .padding()
                
                Divider()
                    .padding(.horizontal)
                
                // Features
                VStack(alignment: .leading, spacing: 8) {
                    Text("Features")
                        .font(.headline)
                    
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 8) {
                        ForEach(property.features, id: \.self) { feature in
                            FeatureRow(feature: feature)
                        }
                    }
                }
                .padding()
                
                Divider()
                    .padding(.horizontal)
                
                // Map
                VStack(alignment: .leading, spacing: 8) {
                    Text("Location")
                        .font(.headline)
                    
                    Map(position: .region(MKCoordinateRegion(
                        center: CLLocationCoordinate2D(latitude: property.latitude, longitude: property.longitude),
                        span: MKCoordinateSpan(latitudeDelta: 0.01, longitudeDelta: 0.01)
                    ))) {
                        Marker(property.title, coordinate: CLLocationCoordinate2D(
                            latitude: property.latitude,
                            longitude: property.longitude
                        ))
                    }
                    .frame(height: 200)
                    .cornerRadius(12)
                }
                .padding()
                
                // Action buttons
                HStack(spacing: 16) {
                    Button(action: { viewModel.toggleFavorite(propertyId: property.id) }) {
                        HStack {
                            Image(systemName: viewModel.isFavorite ? "heart.fill" : "heart")
                            Text(viewModel.isFavorite ? "Saved" : "Save")
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(viewModel.isFavorite ? Color.red.opacity(0.1) : Color(.secondarySystemBackground))
                        .foregroundColor(viewModel.isFavorite ? .red : .primary)
                        .cornerRadius(10)
                    }
                    
                    Button(action: {}) {
                        HStack {
                            Image(systemName: "calendar.badge.plus")
                            Text("Schedule Tour")
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.enkiPrimary)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                    }
                }
                .padding()
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                Menu {
                    Button(action: {}) {
                        Label("Share", systemImage: "square.and.arrow.up")
                    }
                    Button(action: {}) {
                        Label("Contact Agent", systemImage: "phone")
                    }
                } label: {
                    Image(systemName: "ellipsis.circle")
                }
            }
        }
        .onAppear {
            viewModel.checkFavoriteStatus(propertyId: property.id)
        }
    }
}

struct ImageGalleryView: View {
    let images: [PropertyImage]
    @State private var currentIndex = 0
    
    var body: some View {
        TabView(selection: $currentIndex) {
            ForEach(Array(images.enumerated()), id: \.offset) { index, image in
                AsyncImage(url: URL(string: image.url)) { phase in
                    switch phase {
                    case .empty:
                        ProgressView()
                    case .success(let image):
                        image
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                    case .failure:
                        Image(systemName: "photo")
                            .font(.largeTitle)
                            .foregroundColor(.secondary)
                    @unknown default:
                        EmptyView()
                    }
                }
                .tag(index)
            }
            
            if images.isEmpty {
                Color.gray.opacity(0.2)
                    .overlay(
                        Image(systemName: "photo")
                            .font(.largeTitle)
                            .foregroundColor(.gray)
                    )
                    .tag(0)
            }
        }
        .tabViewStyle(.page(indexDisplayMode: .always))
    }
}

struct StatusBadge: View {
    let status: PropertyStatus
    
    var color: Color {
        switch status {
        case .active: return .green
        case .pending: return .orange
        case .sold: return .red
        case .offMarket: return .gray
        }
    }
    
    var body: some View {
        Text(status.rawValue.capitalized)
            .font(.caption.weight(.medium))
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(color.opacity(0.1))
            .foregroundColor(color)
            .cornerRadius(6)
    }
}

struct StatItem: View {
    let icon: String
    let value: String
    let label: String
    
    var body: some View {
        VStack(spacing: 4) {
            Image(systemName: icon)
                .font(.title3)
                .foregroundColor(.enkiPrimary)
            
            Text(value)
                .font(.headline)
            
            Text(label)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
    }
}

struct FeatureRow: View {
    let feature: String
    
    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: "checkmark.circle.fill")
                .foregroundColor(.green)
                .font(.caption)
            
            Text(feature)
                .font(.subheadline)
            
            Spacer()
        }
    }
}

@MainActor
class PropertyDetailViewModel: ObservableObject {
    @Published var isFavorite = false
    
    func checkFavoriteStatus(propertyId: String) {
        Task {
            do {
                let favorites = try await NetworkManager.shared.getFavorites()
                isFavorite = favorites.contains { $0.id == propertyId }
            } catch {
                print("Failed to check favorite status: \(error)")
            }
        }
    }
    
    func toggleFavorite(propertyId: String) {
        Task {
            do {
                if isFavorite {
                    try await NetworkManager.shared.removeFromFavorites(propertyId: propertyId)
                } else {
                    try await NetworkManager.shared.addToFavorites(propertyId: propertyId)
                }
                isFavorite.toggle()
            } catch {
                print("Failed to toggle favorite: \(error)")
            }
        }
    }
}