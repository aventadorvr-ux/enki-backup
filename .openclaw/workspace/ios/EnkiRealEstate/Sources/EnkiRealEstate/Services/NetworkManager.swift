import Foundation
import Network

@MainActor
class NetworkManager: ObservableObject {
    static let shared = NetworkManager()
    
    @Published var isOffline: Bool = false
    @Published var lastError: NetworkError?
    
    private let baseURL = "https://api.enkirealestate.com/v1"
    private let urlSession: URLSession
    private let monitor: NWPathMonitor
    
    private init() {
        let config = URLSessionConfiguration.default
        config.timeoutIntervalForRequest = 30
        config.timeoutIntervalForResource = 300
        config.waitsForConnectivity = true
        self.urlSession = URLSession(configuration: config)
        
        self.monitor = NWPathMonitor()
        setupNetworkMonitoring()
    }
    
    private func setupNetworkMonitoring() {
        monitor.pathUpdateHandler = { [weak self] path in
            Task { @MainActor in
                self?.isOffline = path.status != .satisfied
            }
        }
        monitor.start(queue: DispatchQueue.global(qos: .background))
    }
    
    // MARK: - Authentication
    
    func login(email: String, password: String) async throws -> AuthResponse {
        let request = AuthRequest(email: email, password: password)
        return try await performRequest(
            endpoint: "/auth/login",
            method: .post,
            body: request
        )
    }
    
    func register(email: String, password: String, firstName: String, lastName: String, phone: String?) async throws -> AuthResponse {
        let request = RegisterRequest(
            email: email,
            password: password,
            firstName: firstName,
            lastName: lastName,
            phone: phone
        )
        return try await performRequest(
            endpoint: "/auth/register",
            method: .post,
            body: request
        )
    }
    
    func refreshToken() async throws -> AuthResponse {
        return try await performRequest(
            endpoint: "/auth/refresh",
            method: .post
        )
    }
    
    // MARK: - User
    
    func getUserProfile() async throws -> User {
        return try await performAuthenticatedRequest(
            endpoint: "/users/me",
            method: .get
        )
    }
    
    func updateUserProfile(user: UserUpdateRequest) async throws -> User {
        return try await performAuthenticatedRequest(
            endpoint: "/users/me",
            method: .put,
            body: user
        )
    }
    
    // MARK: - Properties
    
    func searchProperties(filters: SearchFilters, page: Int = 1, pageSize: Int = 20) async throws -> SearchResult {
        var queryParams: [String: String] = [
            "page": String(page),
            "page_size": String(pageSize)
        ]
        
        if let minPrice = filters.minPrice {
            queryParams["min_price"] = String(minPrice)
        }
        if let maxPrice = filters.maxPrice {
            queryParams["max_price"] = String(maxPrice)
        }
        if let bedrooms = filters.bedrooms {
            queryParams["bedrooms"] = String(bedrooms)
        }
        if let location = filters.location {
            queryParams["location"] = location
        }
        if let listingType = filters.listingType {
            queryParams["listing_type"] = listingType.rawValue
        }
        
        return try await performAuthenticatedRequest(
            endpoint: "/properties/search",
            method: .get,
            queryParams: queryParams
        )
    }
    
    func getProperty(id: String) async throws -> Property {
        return try await performAuthenticatedRequest(
            endpoint: "/properties/\(id)",
            method: .get
        )
    }
    
    func getPropertiesNearby(latitude: Double, longitude: Double, radius: Double = 10.0) async throws -> [Property] {
        let queryParams: [String: String] = [
            "lat": String(latitude),
            "lon": String(longitude),
            "radius": String(radius)
        ]
        
        return try await performAuthenticatedRequest(
            endpoint: "/properties/nearby",
            method: .get,
            queryParams: queryParams
        )
    }
    
    // MARK: - Favorites
    
    func getFavorites() async throws -> [Property] {
        return try await performAuthenticatedRequest(
            endpoint: "/users/me/favorites",
            method: .get
        )
    }
    
    func addToFavorites(propertyId: String) async throws {
        _ = try await performAuthenticatedRequest(
            endpoint: "/users/me/favorites",
            method: .post,
            body: ["property_id": propertyId]
        ) as EmptyResponse
    }
    
    func removeFromFavorites(propertyId: String) async throws {
        _ = try await performAuthenticatedRequest(
            endpoint: "/users/me/favorites/\(propertyId)",
            method: .delete
        ) as EmptyResponse
    }
    
    // MARK: - AI Features
    
    func getPropertyValuation(request: ValuationRequest) async throws -> ValuationResult {
        return try await performAuthenticatedRequest(
            endpoint: "/ai/valuation",
            method: .post,
            body: request
        )
    }
    
    func submitLeadQualification(lead: LeadQualificationRequest) async throws -> LeadQualificationResponse {
        return try await performAuthenticatedRequest(
            endpoint: "/leads/qualify",
            method: .post,
            body: lead
        )
    }
    
    func chatWithAI(message: String, context: String?) async throws -> ChatResponse {
        let request = ChatRequest(message: message, context: context)
        return try await performAuthenticatedRequest(
            endpoint: "/ai/chat",
            method: .post,
            body: request
        )
    }
    
    // MARK: - Agent Tools
    
    func getLeads(status: LeadStatus? = nil, assignedToMe: Bool = false) async throws -> [Lead] {
        var queryParams: [String: String] = [:]
        if let status = status {
            queryParams["status"] = status.rawValue
        }
        if assignedToMe {
            queryParams["assigned_to_me"] = "true"
        }
        
        return try await performAuthenticatedRequest(
            endpoint: "/leads",
            method: .get,
            queryParams: queryParams
        )
    }
    
    func updateLeadStatus(id: String, status: LeadStatus) async throws -> Lead {
        return try await performAuthenticatedRequest(
            endpoint: "/leads/\(id)/status",
            method: .patch,
            body: ["status": status.rawValue]
        )
    }
    
    func getAgentDashboard() async throws -> DashboardData {
        return try await performAuthenticatedRequest(
            endpoint: "/agents/dashboard",
            method: .get
        )
    }
    
    // MARK: - Request Helpers
    
    private func performRequest<T: Decodable>(
        endpoint: String,
        method: HTTPMethod,
        body: Encodable? = nil,
        queryParams: [String: String]? = nil
    ) async throws -> T {
        guard let url = buildURL(endpoint: endpoint, queryParams: queryParams) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        let (data, response) = try await urlSession.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        switch httpResponse.statusCode {
        case 200...299:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            return try decoder.decode(T.self, from: data)
        case 401:
            throw NetworkError.unauthorized
        case 404:
            throw NetworkError.notFound
        default:
            if let errorResponse = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                throw NetworkError.serverError(errorResponse.message)
            }
            throw NetworkError.serverError("Unknown error")
        }
    }
    
    private func performAuthenticatedRequest<T: Decodable>(
        endpoint: String,
        method: HTTPMethod,
        body: Encodable? = nil,
        queryParams: [String: String]? = nil
    ) async throws -> T {
        guard let token = KeychainManager.shared.getToken() else {
            throw NetworkError.unauthorized
        }
        
        guard let url = buildURL(endpoint: endpoint, queryParams: queryParams) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }
        
        let (data, response) = try await urlSession.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        switch httpResponse.statusCode {
        case 200...299:
            let decoder = JSONDecoder()
            decoder.dateDecodingStrategy = .iso8601
            return try decoder.decode(T.self, from: data)
        case 401:
            try await refreshAndRetry(endpoint: endpoint, method: method, body: body)
            return try await performAuthenticatedRequest(endpoint: endpoint, method: method, body: body)
        case 404:
            throw NetworkError.notFound
        default:
            if let errorResponse = try? JSONDecoder().decode(ErrorResponse.self, from: data) {
                throw NetworkError.serverError(errorResponse.message)
            }
            throw NetworkError.serverError("Unknown error")
        }
    }
    
    private func refreshAndRetry(endpoint: String, method: HTTPMethod, body: Encodable?) async throws {
        do {
            let authResponse = try await refreshToken()
            KeychainManager.shared.saveToken(authResponse.token)
        } catch {
            throw NetworkError.unauthorized
        }
    }
    
    private func buildURL(endpoint: String, queryParams: [String: String]?) -> URL? {
        var components = URLComponents(string: baseURL + endpoint)
        if let params = queryParams {
            components?.queryItems = params.map { URLQueryItem(name: $0.key, value: $0.value) }
        }
        return components?.url
    }
}

// MARK: - Supporting Types

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case patch = "PATCH"
    case delete = "DELETE"
}

enum NetworkError: Error, LocalizedError {
    case invalidURL
    case invalidResponse
    case unauthorized
    case notFound
    case serverError(String)
    case offline
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .unauthorized:
            return "Please log in again"
        case .notFound:
            return "Not found"
        case .serverError(let message):
            return message
        case .offline:
            return "No internet connection"
        }
    }
}

struct AuthRequest: Codable {
    let email: String
    let password: String
}

struct RegisterRequest: Codable {
    let email: String
    let password: String
    let firstName: String
    let lastName: String
    let phone: String?
}

struct AuthResponse: Codable {
    let token: String
    let user: User
    let expiresIn: Int
}

struct UserUpdateRequest: Codable {
    let firstName: String?
    let lastName: String?
    let phone: String?
    let avatar: String?
}

struct ChatRequest: Codable {
    let message: String
    let context: String?
}

struct ChatResponse: Codable {
    let message: String
    let suggestions: [String]?
    let relatedProperties: [Property]?
}

struct LeadQualificationRequest: Codable {
    let name: String
    let email: String
    let phone: String?
    let budget: Double?
    let timeline: String?
    let propertyType: PropertyType?
    let location: String?
    let notes: String?
}

struct LeadQualificationResponse: Codable {
    let leadId: String
    let qualificationScore: Double
    let recommendedProperties: [Property]
    let nextSteps: [String]
}

struct DashboardData: Codable {
    let totalLeads: Int
    let newLeadsThisWeek: Int
    let activeListings: Int
    let closedDealsThisMonth: Int
    let pipelineValue: Double
    let recentActivity: [ActivityItem]
}

struct ActivityItem: Codable {
    let type: String
    let description: String
    let timestamp: Date
}

struct ErrorResponse: Codable {
    let message: String
    let code: String?
}

struct EmptyResponse: Codable {}