import SwiftUI

struct FavoritesView: View {
    @StateObject private var viewModel = FavoritesViewModel()
    
    var body: some View {
        NavigationView {
            Group {
                if viewModel.favorites.isEmpty {
                    EmptyFavoritesView()
                } else {
                    List {
                        ForEach(viewModel.favorites) { property in
                            NavigationLink(destination: PropertyDetailView(property: property)) {
                                FavoriteRow(property: property)
                            }
                        }
                        .onDelete(perform: delete)
                    }
                    .listStyle(.plain)
                }
            }
            .navigationTitle("Saved Properties")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    EditButton()
                }
            }
        }
        .onAppear {
            Task { await viewModel.loadFavorites() }
        }
    }
    
    private func delete(at offsets: IndexSet) {
        for index in offsets {
            let property = viewModel.favorites[index]
            Task {
                do {
                    try await NetworkManager.shared.removeFromFavorites(propertyId: property.id)
                    await viewModel.loadFavorites()
                } catch {
                    print("Failed to remove favorite: \(error)")
                }
            }
        }
    }
}

struct FavoriteRow: View {
    let property: Property
    
    var body: some View {
        HStack(spacing: 12) {
            // Thumbnail
            RoundedRectangle(cornerRadius: 8)
                .fill(Color.gray.opacity(0.2))
                .frame(width: 100, height: 80)
                .overlay(
                    Image(systemName: "photo")
                        .foregroundColor(.gray)
                )
            
            VStack(alignment: .leading, spacing: 4) {
                Text(property.formattedPrice)
                    .font(.headline)
                
                Text(property.address.fullAddress)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .lineLimit(1)
                
                HStack(spacing: 12) {
                    Label("\(property.bedrooms)", systemImage: "bed.double.fill")
                    Label("\(property.bathrooms)", systemImage: "shower.fill")
                }
                .font(.caption)
                .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

struct EmptyFavoritesView: View {
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "heart.slash")
                .font(.system(size: 60))
                .foregroundColor(.secondary)
            
            Text("No saved properties")
                .font(.title3.weight(.semibold))
            
            Text("Tap the heart icon on any property to save it here")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
            
            NavigationLink("Browse Properties") {
                SearchView()
            }
            .buttonStyle(.borderedProminent)
            .tint(.enkiPrimary)
            .padding(.top, 10)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

@MainActor
class FavoritesViewModel: ObservableObject {
    @Published var favorites: [Property] = []
    
    func loadFavorites() async {
        do {
            favorites = try await NetworkManager.shared.getFavorites()
        } catch {
            print("Failed to load favorites: \(error)")
        }
    }
}