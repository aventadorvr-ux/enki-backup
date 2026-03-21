import Foundation

// MARK: - Property Models

struct Property: Identifiable, Codable {
    let id: String
    let title: String
    let description: String
    let price: Double
    let address: Address
    let bedrooms: Int
    let bathrooms: Int
    let squareFeet: Double
    let yearBuilt: Int?
    let propertyType: PropertyType
    let listingType: ListingType
    let status: PropertyStatus
    let images: [PropertyImage]
    let features: [String]
    let agentId: String?
    let createdAt: Date
    let updatedAt: Date
    let latitude: Double
    let longitude: Double
    
    var formattedPrice: String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = "USD"
        formatter.maximumFractionDigits = 0
        return formatter.string(from: NSNumber(value: price)) ?? "\(price)"
    }
    
    var formattedSquareFeet: String {
        return "\(Int(squareFeet)) sq ft"
    }
}

struct Address: Codable {
    let street: String
    let city: String
    let state: String
    let zipCode: String
    let country: String
    
    var fullAddress: String {
        return "\(street), \(city), \(state) \(zipCode)"
    }
}

struct PropertyImage: Codable {
    let id: String
    let url: String
    let caption: String?
    let isPrimary: Bool
}

enum PropertyType: String, Codable, CaseIterable {
    case house = "house"
    case apartment = "apartment"
    case condo = "condo"
    case townhouse = "townhouse"
    case land = "land"
    case commercial = "commercial"
    
    var displayName: String {
        switch self {
        case .house: return "House"
        case .apartment: return "Apartment"
        case .condo: return "Condo"
        case .townhouse: return "Townhouse"
        case .land: return "Land"
        case .commercial: return "Commercial"
        }
    }
}

enum ListingType: String, Codable {
    case sale = "sale"
    case rent = "rent"
    
    var displayName: String {
        switch self {
        case .sale: return "For Sale"
        case .rent: return "For Rent"
        }
    }
}

enum PropertyStatus: String, Codable {
    case active = "active"
    case pending = "pending"
    case sold = "sold"
    case offMarket = "off_market"
}

// MARK: - User Models

struct User: Identifiable, Codable {
    let id: String
    let email: String
    let firstName: String
    let lastName: String
    let phone: String?
    let role: UserRole
    let avatar: String?
    let createdAt: Date
    let updatedAt: Date
    
    var fullName: String {
        return "\(firstName) \(lastName)"
    }
}

enum UserRole: String, Codable {
    case buyer = "buyer"
    case seller = "seller"
    case agent = "agent"
    case admin = "admin"
}

// MARK: - Lead Models

struct Lead: Identifiable, Codable {
    let id: String
    let firstName: String
    let lastName: String
    let email: String
    let phone: String?
    let source: String
    let status: LeadStatus
    let notes: String?
    let assignedTo: String?
    let propertyId: String?
    let createdAt: Date
    let updatedAt: Date
}

enum LeadStatus: String, Codable {
    case new = "new"
    case contacted = "contacted"
    case qualified = "qualified"
    case negotiation = "negotiation"
    case closed = "closed"
    case lost = "lost"
}

// MARK: - Valuation Models

struct ValuationRequest: Codable {
    let address: String
    let propertyType: PropertyType
    let bedrooms: Int
    let bathrooms: Int
    let squareFeet: Double
    let yearBuilt: Int?
}

struct ValuationResult: Codable {
    let estimatedValue: Double
    let confidenceScore: Double
    let comparableProperties: [Property]
    let valueRange: ValueRange
    let marketTrends: MarketTrends
}

struct ValueRange: Codable {
    let low: Double
    let high: Double
}

struct MarketTrends: Codable {
    let appreciationRate: Double
    let daysOnMarket: Int
    let inventoryLevel: String
}

// MARK: - Search Models

struct SearchFilters: Codable {
    var minPrice: Double?
    var maxPrice: Double?
    var bedrooms: Int?
    var bathrooms: Double?
    var propertyTypes: [PropertyType]
    var listingType: ListingType?
    var location: String?
    var radius: Double?
}

struct SearchResult: Codable {
    let properties: [Property]
    let totalCount: Int
    let page: Int
    let pageSize: Int
    let hasMore: Bool
}