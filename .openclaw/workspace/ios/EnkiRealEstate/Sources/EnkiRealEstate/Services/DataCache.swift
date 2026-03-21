import Foundation

actor DataCache {
    static let shared = DataCache()
    
    private var cache: [String: CacheEntry] = [:]
    private let fileManager = FileManager.default
    private let cacheDirectory: URL
    
    private struct CacheEntry {
        let data: Data
        let timestamp: Date
        let expiration: TimeInterval
        
        var isExpired: Bool {
            Date().timeIntervalSince(timestamp) > expiration
        }
    }
    
    private init() {
        let urls = fileManager.urls(for: .cachesDirectory, in: .userDomainMask)
        cacheDirectory = urls[0].appendingPathComponent("EnkiCache")
        
        try? fileManager.createDirectory(at: cacheDirectory, withIntermediateDirectories: true)
    }
    
    func get<T: Decodable>(key: String, as type: T.Type) -> T? {
        // Check memory cache first
        if let entry = cache[key], !entry.isExpired {
            return try? JSONDecoder().decode(type, from: entry.data)
        }
        
        // Check file cache
        let fileURL = cacheDirectory.appendingPathComponent(key.md5)
        guard let data = try? Data(contentsOf: fileURL) else { return nil }
        
        return try? JSONDecoder().decode(type, from: data)
    }
    
    func set<T: Encodable>(_ value: T, forKey key: String, expiration: TimeInterval = 3600) {
        guard let data = try? JSONEncoder().encode(value) else { return }
        
        // Store in memory
        cache[key] = CacheEntry(data: data, timestamp: Date(), expiration: expiration)
        
        // Store in file
        let fileURL = cacheDirectory.appendingPathComponent(key.md5)
        try? data.write(to: fileURL)
    }
    
    func remove(key: String) {
        cache.removeValue(forKey: key)
        let fileURL = cacheDirectory.appendingPathComponent(key.md5)
        try? fileManager.removeItem(at: fileURL)
    }
    
    func clear() {
        cache.removeAll()
        try? fileManager.removeItem(at: cacheDirectory)
        try? fileManager.createDirectory(at: cacheDirectory, withIntermediateDirectories: true)
    }
    
    // MARK: - Property-specific caching
    
    func cacheProperties(_ properties: [Property], for searchKey: String) {
        set(properties, forKey: "properties_\(searchKey)", expiration: 300) // 5 minutes
    }
    
    func getCachedProperties(for searchKey: String) -> [Property]? {
        return get(key: "properties_\(searchKey)", as: [Property].self)
    }
    
    func cacheProperty(_ property: Property) {
        set(property, forKey: "property_\(property.id)", expiration: 600) // 10 minutes
    }
    
    func getCachedProperty(id: String) -> Property? {
        return get(key: "property_\(id)", as: Property.self)
    }
    
    func cacheFavorites(_ favorites: [Property]) {
        set(favorites, forKey: "favorites", expiration: 60) // 1 minute
    }
    
    func getCachedFavorites() -> [Property]? {
        return get(key: "favorites", as: [Property].self)
    }
}

// MARK: - String Extension for MD5

import CryptoKit

extension String {
    var md5: String {
        let data = Data(self.utf8)
        let hash = Insecure.MD5.hash(data: data)
        return hash.map { String(format: "%02hhx", $0) }.joined()
    }
}