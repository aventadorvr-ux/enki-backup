import SwiftUI
import MapKit

struct SearchView: View {
    @StateObject private var viewModel = SearchViewModel()
    @State private var showingFilters = false
    @State private var showingMap = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Search bar
                SearchBar(text: $viewModel.searchText, onSearch: {
                    Task { await viewModel.performSearch() }
                })
                .padding()
                
                // Filter chips
                FilterChips(filters: $viewModel.filters)
                    .padding(.horizontal)
                
                // Results count
                HStack {
                    Text("\(viewModel.properties.count) properties found")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                    
                    Spacer()
                    
                    Button(action: { showingFilters = true }) {
                        Label("Filters", systemImage: "line.3.horizontal.decrease.circle")
                    }
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
                
                // Toggle between list and map
                Picker("View", selection: $showingMap) {
                    Text("List").tag(false)
                    Text("Map").tag(true)
                }
                .pickerStyle(.segmented)
                .padding(.horizontal)
                
                // Results
                if showingMap {
                    MapSearchView(properties: viewModel.properties, selectedProperty: $viewModel.selectedProperty)
                } else {
                    ListSearchView(properties: viewModel.properties, isLoading: viewModel.isLoading)
                }
            }
            .navigationTitle("Search Properties")
            .sheet(isPresented: $showingFilters) {
                FilterView(filters: $viewModel.filters, onApply: {
                    Task { await viewModel.performSearch() }
                })
            }
            .sheet(item: $viewModel.selectedProperty) { property in
                PropertyDetailView(property: property)
            }
        }
    }
}

struct SearchBar: View {
    @Binding var text: String
    var onSearch: () -> Void
    
    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: "magnifyingglass")
                .foregroundColor(.secondary)
            
            TextField("Search by location, property type...", text: $text)
                .submitLabel(.search)
                .onSubmit(onSearch)
            
            if !text.isEmpty {
                Button(action: { text = "" }) {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding()
        .background(Color(.secondarySystemBackground))
        .cornerRadius(10)
    }
}

struct FilterChips: View {
    @Binding var filters: SearchFilters
    
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                if let minPrice = filters.minPrice {
                    FilterChip(label: "\(Int(minPrice / 1000))k+", isActive: true) {
                        filters.minPrice = nil
                    }
                }
                
                if let bedrooms = filters.bedrooms {
                    FilterChip(label: "\(bedrooms)+ bed", isActive: true) {
                        filters.bedrooms = nil
                    }
                }
                
                if let listingType = filters.listingType {
                    FilterChip(label: listingType.displayName, isActive: true) {
                        filters.listingType = nil
                    }
                }
                
                if !filters.propertyTypes.isEmpty {
                    FilterChip(label: filters.propertyTypes.first!.displayName, isActive: true) {
                        filters.propertyTypes = []
                    }
                }
            }
        }
    }
}

struct FilterChip: View {
    let label: String
    let isActive: Bool
    let onRemove: () -> Void
    
    var body: some View {
        HStack(spacing: 4) {
            Text(label)
                .font(.caption.weight(.medium))
            
            Button(action: onRemove) {
                Image(systemName: "xmark")
                    .font(.caption2)
            }
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 6)
        .background(isActive ? Color.enkiPrimary : Color.gray.opacity(0.2))
        .foregroundColor(isActive ? .white : .primary)
        .cornerRadius(16)
    }
}

struct ListSearchView: View {
    let properties: [Property]
    let isLoading: Bool
    
    var body: some View {
        Group {
            if isLoading {
                ProgressView()
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if properties.isEmpty {
                EmptySearchView()
            } else {
                List(properties) { property in
                    NavigationLink(destination: PropertyDetailView(property: property)) {
                        SearchResultRow(property: property)
                    }
                }
                .listStyle(.plain)
            }
        }
    }
}

struct SearchResultRow: View {
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
            
            // Info
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
                    Label("\(Int(property.squareFeet))", systemImage: "ruler.fill")
                }
                .font(.caption)
                .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

struct MapSearchView: View {
    let properties: [Property]
    @Binding var selectedProperty: Property?
    
    @State private var position = MapCameraPosition.automatic
    
    var body: some View {
        Map(position: $position) {
            ForEach(properties) { property in
                Annotation(property.formattedPrice, coordinate: CLLocationCoordinate2D(
                    latitude: property.latitude,
                    longitude: property.longitude
                )) {
                    PropertyMapAnnotation(price: property.formattedPrice) {
                        selectedProperty = property
                    }
                }
            }
        }
        .mapStyle(.standard)
        .mapControls {
            MapCompass()
            MapUserLocationButton()
        }
    }
}

struct PropertyMapAnnotation: View {
    let price: String
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            VStack(spacing: 0) {
                Text(price)
                    .font(.caption.weight(.bold))
                    .foregroundColor(.white)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color.enkiPrimary)
                    .cornerRadius(8)
                
                Triangle()
                    .fill(Color.enkiPrimary)
                    .frame(width: 10, height: 6)
            }
        }
    }
}

struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.move(to: CGPoint(x: rect.midX, y: rect.maxY))
        path.addLine(to: CGPoint(x: rect.maxX, y: rect.minY))
        path.addLine(to: CGPoint(x: rect.minX, y: rect.minY))
        path.closeSubpath()
        return path
    }
}

struct FilterView: View {
    @Binding var filters: SearchFilters
    let onApply: () -> Void
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            Form {
                Section("Price Range") {
                    VStack(spacing: 16) {
                        HStack {
                            Text("Min: \(filters.minPrice?.formatted(.currency(code: "USD")) ?? "Any")")
                            Spacer()
                            Text("Max: \(filters.maxPrice?.formatted(.currency(code: "USD")) ?? "Any")")
                        }
                        .font(.subheadline)
                        
                        Slider(value: Binding(
                            get: { filters.minPrice ?? 0 },
                            set: { filters.minPrice = $0 }
                        ), in: 0...2000000, step: 50000)
                        
                        Slider(value: Binding(
                            get: { filters.maxPrice ?? 5000000 },
                            set: { filters.maxPrice = $0 }
                        ), in: 100000...5000000, step: 50000)
                    }
                }
                
                Section("Bedrooms & Bathrooms") {
                    Picker("Bedrooms", selection: $filters.bedrooms) {
                        Text("Any").tag(nil as Int?)
                        ForEach(1...6, id: \.self) { num in
                            Text("\(num)+").tag(num as Int?)
                        }
                    }
                    
                    Picker("Bathrooms", selection: $filters.bathrooms) {
                        Text("Any").tag(nil as Double?)
                        ForEach([1, 1.5, 2, 2.5, 3, 3.5, 4], id: \.self) { num in
                            Text(String(format: "%.1f+", num)).tag(num as Double?)
                        }
                    }
                }
                
                Section("Property Type") {
                    Picker("Type", selection: $filters.propertyTypes) {
                        Text("Any").tag([] as [PropertyType])
                        ForEach(PropertyType.allCases, id: \.self) { type in
                            Text(type.displayName).tag([type] as [PropertyType])
                        }
                    }
                }
                
                Section("Listing Type") {
                    Picker("Type", selection: $filters.listingType) {
                        Text("Any").tag(nil as ListingType?)
                        ForEach([ListingType.sale, ListingType.rent], id: \.self) { type in
                            Text(type.displayName).tag(type as ListingType?)
                        }
                    }
                }
            }
            .navigationTitle("Filters")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Reset") {
                        filters = SearchFilters()
                    }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Apply") {
                        onApply()
                        dismiss()
                    }
                }
            }
        }
    }
}

struct EmptySearchView: View {
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "magnifyingglass.circle")
                .font(.system(size: 60))
                .foregroundColor(.secondary)
            
            Text("No properties found")
                .font(.headline)
            
            Text("Try adjusting your filters or search for a different location")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

@MainActor
class SearchViewModel: ObservableObject {
    @Published var searchText = ""
    @Published var properties: [Property] = []
    @Published var filters = SearchFilters()
    @Published var isLoading = false
    @Published var selectedProperty: Property?
    
    func performSearch() async {
        isLoading = true
        
        var searchFilters = filters
        if !searchText.isEmpty {
            searchFilters.location = searchText
        }
        
        do {
            let result = try await NetworkManager.shared.searchProperties(
                filters: searchFilters,
                page: 1
            )
            properties = result.properties
        } catch {
            print("Search failed: \(error)")
        }
        
        isLoading = false
    }
}